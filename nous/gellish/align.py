"""Entity alignment across independently encoded documents.

Two encoders describe the same thing in different words ("sender internal state" / "internal state of sender",
"phase 5 generation" / "response generation phase"). Without alignment, coverage cannot be measured and two
ontologies cannot be merged. This module produces a mapping between the entities of two documents, with a method
and a score for every pair, in four passes:

  1. **identical** — same name, lowercased.
  2. **grounded** — both names ground to the same dictionary concept (the strongest mechanical signal we have).
  3. **lexical** — token-set similarity above a threshold, after stripping articles and normalising plurals.
  4. **structural** — the pair shares neighbours that are already aligned: the same relations to the same things.
     Iterated twice, seeded by passes 1–3, so agreement propagates through the graph. A structural score is
     capped below the acceptance threshold by construction: sharing a position says "same role", not "same
     thing" — "an external observer" and "omniscient external observer" have identical neighbourhoods.

Everything above `--certain` is accepted mechanically (identity and shared grounding clear it; lexical and
structural rarely do). The band between `--uncertain` and `--certain` is written out for adjudication, which must
distinguish *same thing* from *narrower/broader* — a subsumption is not an identity, and merging on it would
silently generalise the document. Below `--uncertain` nothing is claimed. No pass ever aligns one entity to two
different entities: the best-scoring pair wins and the loser goes back to the uncertain band.
"""
import collections, csv, itertools, pathlib, re, sys

from . import parse

FACT_REF = re.compile(r"^[A-Za-z0-9_.-]+:F\d+$")
STOP = {"the", "a", "an", "of", "in", "to", "for", "and", "or", "its", "it", "is", "as", "by", "with", "on", "at"}


def norm(s):
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tokens(s):
    out = set()
    for w in re.findall(r"[a-z][a-z-]*", norm(s)):
        if w in STOP:
            continue
        out.add(w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith("ss") else w)
    return out


def load(doc):
    """entities → (degree, neighbours as (relation, other) pairs)"""
    rows, _, _ = parse.parse_paths([doc], {})
    deg, nb = collections.Counter(), collections.defaultdict(set)
    for r in rows:
        l, phrase, rt = r[1], r[3], r[4]
        if not l or not rt:
            continue
        if not FACT_REF.match(l) and not FACT_REF.match(rt):
            deg[norm(l)] += 1; deg[norm(rt)] += 1
            nb[norm(l)].add((phrase, norm(rt), "→")); nb[norm(rt)].add((phrase, norm(l), "←"))
        elif not FACT_REF.match(l):
            deg[norm(l)] += 1
        elif not FACT_REF.match(rt):
            deg[norm(rt)] += 1
    return deg, nb


def grounding(doc, ws_dir):
    from . import paths, run
    ws = paths.Workspace(ws_dir)
    run.check(ws, [doc], quiet=True)
    g = collections.defaultdict(set)
    for x, u in csv.reader((ws.out / "ground.csv").open(newline=""), delimiter="\t"):
        g[norm(x)].add(u)
    return g


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def align(doc_a, doc_b, tmp_a, tmp_b, certain=0.85, uncertain=0.42):
    (da, na), (db, nb) = load(doc_a), load(doc_b)
    ga, gb = grounding(doc_a, tmp_a), grounding(doc_b, tmp_b)
    ta = {e: tokens(e) for e in da}
    tb = {e: tokens(e) for e in db}

    scored = collections.defaultdict(dict)          # a → {b: (score, method)}

    def offer(a, b, s, m):
        if s > scored[a].get(b, (0, ""))[0]:
            scored[a][b] = (s, m)

    for e in set(da) & set(db):                     # 1. identical
        offer(e, e, 1.0, "identical")
    by_uid = collections.defaultdict(list)          # 2. grounded
    for e, us in gb.items():
        for u in us:
            by_uid[u].append(e)
    for e, us in ga.items():
        for u in us:
            for f in by_uid.get(u, []):
                offer(e, f, 0.95 if e != f else 1.0, "grounded")
    index = collections.defaultdict(set)            # 3. lexical
    for e, t in tb.items():
        for w in t:
            index[w].add(e)
    for e, t in ta.items():
        cands = set().union(*(index[w] for w in t if w in index)) if any(w in index for w in t) else set()
        for f in cands:
            j = jaccard(t, tb[f])
            if j >= uncertain:
                offer(e, f, j, "lexical")

    def best_map(sc):                                # one-to-one: best pair wins
        pairs = sorted(((a, b, v[0], v[1]) for a, bs in sc.items() for b, v in bs.items()),
                       key=lambda x: -x[2])
        used_a, used_b, out = set(), set(), []
        for a, b, s, m in pairs:
            if a in used_a or b in used_b:
                continue
            used_a.add(a); used_b.add(b); out.append((a, b, s, m))
        return out

    for _ in range(2):                               # 4. structural, seeded by what is already certain
        seed = {a: b for a, b, s, _ in best_map(scored) if s >= certain}
        if not seed:
            break
        for a, b, s, m in list((a, b) + v for a, bs in scored.items() for b, v in bs.items()):
            pass
        for a in da:
            if a in seed or not na[a]:
                continue
            cands = collections.Counter()
            for phrase, other, d in na[a]:
                if other in seed:
                    for phrase2, other2, d2 in nb.get(seed[other], ()):
                        if phrase2 == phrase and d2 != d:
                            cands[other2] += 1
            for f, k in cands.items():
                share = k / max(1, min(len(na[a]), len(nb[f])))
                if share >= 0.34 and jaccard(ta[a], tb.get(f, set())) > 0.0:
                    # structure says "same role in the graph", never "same thing": a narrower term occupies the
                    # same position as the broader one. So a structural score can never clear `certain` on its own.
                    offer(a, f, min(certain - 0.01, 0.5 + share / 2), "structural")

    final = best_map(scored)
    accepted = [(a, b, s, m) for a, b, s, m in final if s >= certain]
    band = [(a, b, s, m) for a, b, s, m in final if uncertain <= s < certain]
    return {"accepted": accepted, "uncertain": band, "a": da, "b": db}


def write(res, out):
    out = pathlib.Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for a, b, s, m in res["accepted"]:
            f.write(f"{a}\t{b}\t{s:.2f}\t{m}\n")
    u = out.with_suffix(".uncertain.tsv")
    with u.open("w") as f:
        for a, b, s, m in res["uncertain"]:
            f.write(f"{a}\t{b}\t{s:.2f}\t{m}\n")
    return out, u


def report(res, doc_a, doc_b):
    da, db = res["a"], res["b"]
    acc, band = res["accepted"], res["uncertain"]
    by = collections.Counter(m for _, _, _, m in acc)
    lines = [f"# Alignment: {pathlib.Path(doc_a).name} ↔ {pathlib.Path(doc_b).name}", "",
             f"| | count |", "|---|---:|",
             f"| entities in A | {len(da)} |", f"| entities in B | {len(db)} |",
             f"| aligned (accepted) | {len(acc)} |", f"| uncertain band | {len(band)} |",
             f"| B entities left unaligned | {len(db) - len(acc)} |", ""]
    lines += ["by method: " + ", ".join(f"{k} {v}" for k, v in by.most_common()), "",
              "## accepted, weakest first", ""]
    for a, b, s, m in sorted(acc, key=lambda x: x[2])[:40]:
        lines.append(f"- {a}  ≡  {b}   ({m} {s:.2f})")
    lines += ["", "## uncertain band (needs adjudication)", ""]
    for a, b, s, m in sorted(band, key=lambda x: -x[2])[:60]:
        lines.append(f"- {a}  ?  {b}   ({m} {s:.2f})")
    return "\n".join(lines) + "\n"
