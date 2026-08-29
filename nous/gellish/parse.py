#!/usr/bin/env python3
"""Gellish v2 fact tables -> Soufflé fact files.

Input : one or more 7-column pipe-separated tables
        fact-UID | left | relation phrase | right | value/UoM | intention | context
Output: <facts-dir>/fact.facts   (tab-separated, 10 columns)
        f  left  rel  phrase  right  value  intention  context  table  rel_uid
        <facts-dir>/entity_lc.facts  entity  lowercased-entity   (for dictionary grounding)
        <facts-dir>/param.facts, disjoint.facts

Relation resolution: <facts-dir>/d_phrase.facts (from gellish_dict.py, which includes the
Gellish dictionary AND the ext/ domain extensions): base phrase or inverse phrase of a relation
type -> rel = "g:<uid>", rel_uid = <uid>. Inverse phrases swap left/right so that left is
always the first-role player. Anything else -> rel = "other": the residual, an opaque edge.

Fact UIDs are namespaced by table id (C03:F0012); entities are not — a name shared across
tables is one node, which is what makes cross-chunk consistency checking possible.
"""
import argparse, collections, pathlib, re, sys

AUTHOR_ALIASES = {"author", "the author", "the authors", "authors", "this article", "the article",
                  "this paper", "the paper", "we"}
FACT_REF = re.compile(r"^F\d{3,5}$")


def load_dict_phrases(facts_dir):
    """phrase -> (uid, dir); ambiguous phrases resolve to a domain-extension UID if one exists, else the lowest UID."""
    p = pathlib.Path(facts_dir) / "d_phrase.facts"
    if not p.exists():
        return {}, {}
    cands = collections.defaultdict(set)
    for line in p.read_text(encoding="utf-8").splitlines():
        ph, uid, d = line.split("\t")
        cands[ph].add((uid, d))
    res, amb = {}, {}
    for ph, s in cands.items():
        uids = {u for u, _ in s}
        if len(uids) > 1:
            amb[ph] = sorted(uids, key=int)
        ext = [u for u in uids if int(u) >= 100700000]        # domain extension shadows the general dictionary
        u = min(ext or uids, key=int)
        d = "inv" if (u, "inv") in s and (u, "base") not in s else "base"
        res[ph] = (u, d)
    return res, amb


def norm_phrase(s):
    s = re.sub(r"^\s*\d+\s+", "", s)          # strip a leading Gellish UID
    return re.sub(r"\s+", " ", s).strip().lower()


def norm_obj(s, table):
    s = re.sub(r"\s+", " ", s).strip()
    if s in ("-", ""):
        return ""
    if FACT_REF.match(s):
        return f"{table}:{s}"
    if s.lower() in AUTHOR_ALIASES:
        return "the author"
    return s


def resolve(phrase, dphr):
    if phrase in dphr:
        uid, d = dphr[phrase]
        return "g:" + uid, d == "inv", uid
    return "other", False, ""


def parse_file(path, table, dphr, errors):
    rows = []
    for ln, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 6 or not FACT_REF.match(cells[0]):
            errors.append((table, ln, line[:120]))
            continue
        cells += [""] * (7 - len(cells))
        uid, left, phrase, right, value, intention, context = cells[:7]
        phrase_n = norm_phrase(phrase)
        rel, swap, ruid = resolve(phrase_n, dphr)
        l, r = norm_obj(left, table), norm_obj(right, table)
        if swap:
            l, r = r, l
        rows.append((f"{table}:{uid}", l, rel, phrase_n, r,
                     "" if value == "-" else value,
                     intention.strip().lower(),
                     "" if context == "-" else context,
                     table, ruid))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("tables", nargs="+", help="Gellish v2 .txt tables")
    ap.add_argument("-o", "--out", default="facts", help="facts directory (must already hold d_*.facts for dictionary resolution)")
    ap.add_argument("--minlevel", type=int, default=2,
                    help="minimum commitment level admitted into inference (4 assertion, 3 hedged, 2 hypothesis/prediction)")
    ap.add_argument("--maxdepth", type=int, default=8, help="entailment chain budget (depth cap)")
    ap.add_argument("--disjoint", help="optional TSV of disjoint kind pairs")
    ap.add_argument("--theory", choices=["off", "hypothesis", "doctrine"], default="hypothesis",
                    help="how the Synthea-bootstrap collection enters inference: excluded, at level 2, or at level 4")
    a = ap.parse_args(argv)

    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    dphr, amb = load_dict_phrases(out)
    errors, rows = [], []
    for t in a.tables:
        p = pathlib.Path(t)
        rows += parse_file(p, p.stem, dphr, errors)

    esc = lambda s: s.replace("\t", " ").replace("\n", " ")
    with (out / "fact.facts").open("w") as f:
        for r in rows:
            f.write("\t".join(esc(c) for c in r) + "\n")
    ents = {c for r in rows for c in (r[1], r[4]) if c and not re.match(r"^[A-Za-z0-9_.-]+:F\d+$", c)}
    with (out / "entity_lc.facts").open("w") as f:
        for e in sorted(ents):
            f.write(f"{esc(e)}\t{esc(e.lower())}\n")
    with (out / "param.facts").open("w") as f:
        f.write(f"minlevel\t{a.minlevel}\nmaxdepth\t{a.maxdepth}\ntheory\t{ {'off': 0, 'hypothesis': 2, 'doctrine': 4}[a.theory] }\n")
    dj = out / "disjoint.facts"
    dj.write_text(pathlib.Path(a.disjoint).read_text() if a.disjoint else "")

    kinds = collections.Counter(r[2].split(":")[0] for r in rows)
    used_amb = {r[3] for r in rows if r[3] in amb}
    print(f"{len(rows)} facts from {len(a.tables)} tables; resolved: {kinds['g']} dictionary+extension, "
          f"{kinds['other']} residual; {len(errors)} unparseable lines; dictionary phrases known: {len(dphr)}", file=sys.stderr)
    for ph in sorted(used_amb):
        print(f"  ambiguous phrase {ph!r} -> {dphr[ph][0]} (candidates {amb[ph]})", file=sys.stderr)
    for e in errors[:10]:
        print("  skip", *e, file=sys.stderr)


if __name__ == "__main__":
    main()
