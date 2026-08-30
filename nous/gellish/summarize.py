"""Structural summary: select the rows that carry the document's thesis, by the reasoner's thesis stratum.

The summary is a SELECTION of stated rows (never new claims), assembled in this order until the budget is spent:
  1. the problem and its coverage — for each addressed component, the rows on the shortest explanatory path from
     the component's entity to the best hub (the document's own concept that addresses most components);
  2. definitions of the hubs and of the concepts on those paths (intention `definition`);
  3. the author's explicit salience rows (`is qualified as`) and the claims they qualify;
  4. foils: `rebutted-claim` rows with their `is raised to rebut` counter-claims;
  5. the most central remaining assertions about the hubs (by section spread).
Output: a ```gellish-summary``` block (rows keep their global ids) plus a short header of the structural facts
(problem, coverage, hubs) — ready for a shell-less decode into an abstract.
"""
import collections, csv, pathlib, re

FACT_REF = re.compile(r"^[A-Za-z0-9_.-]+:F\d+$")


def tsv(p):
    p = pathlib.Path(p)
    return list(csv.reader(p.open(newline=""), delimiter="\t")) if p.exists() else []


def build(out_dir, facts_dir, budget=80):
    out, fd = pathlib.Path(out_dir), pathlib.Path(facts_dir)
    facts = {r[0]: r for r in tsv(fd / "fact.facts")}
    coverage = tsv(out / "coverage.csv")
    degree = collections.Counter()
    for f, r in facts.items():
        degree[r[1]] += 1; degree[r[4]] += 1
    hubs = sorted(tsv(out / "hub.csv"), key=lambda x: (-int(x[1]), -int(x[2]), -degree[x[0]], x[0]))
    comp_entity = collections.defaultdict(set)
    for x, c in tsv(out / "comp_entity.csv"):
        comp_entity[c].add(x)
    # explanatory graph with row provenance, plus identity edges
    adj = collections.defaultdict(list)
    for x, y, f in tsv(out / "expl_f.csv"):
        adj[x].append((y, f)); adj[y].append((x, f))
    for l, rel, r, lv, origin in tsv(out / "kb.csv"):
        if rel == "is identical to":
            adj[l].append((r, None)); adj[r].append((l, None))

    def path_rows(src, dst, maxd=2):
        best = None
        for s in src:
            frontier = [(s, [])]; seen = {s}
            for _ in range(maxd):
                nxt = []
                for node, rows in frontier:
                    for y, f in adj.get(node, []):
                        if y in seen:
                            continue
                        rr = rows + ([f] if f else [])
                        if y == dst:
                            if best is None or len(rr) < len(best):
                                best = rr
                        seen.add(y); nxt.append((y, rr))
                frontier = nxt
        return best or []

    chosen, order, why = set(), [], {}

    def take(f, reason):
        if f in facts and f not in chosen and len(order) < budget:
            chosen.add(f); order.append(f); why[f] = reason

    anchors = tsv(out / "anchor.csv"); aside = tsv(out / "set_aside.csv")
    cname = {c: cn for _, _, c, cn, _, _ in coverage}
    header = []
    for c, x, m, f in anchors:
        take(f, f"anchor: {cname.get(c, c)} ↔ {m}")
    for c, x, f in aside:
        take(f, f"set aside: {cname.get(c, c)}")
    for p_, pn, c, cn, st, via in coverage:
        header.append((pn, cn, st, via))
        if st != "addressed":
            continue
        for f in path_rows(comp_entity.get(c, set()), via):
            take(f, f"{cn} → {via}")
    hub_names = [h[0] for h in hubs[:5]]
    on_paths = {facts[f][1] for f in order} | {facts[f][4] for f in order} | set(hub_names)
    for f, r in facts.items():                                           # 2. definitions
        if r[6] == "definition" and r[1] in on_paths and not FACT_REF.match(r[1]):
            take(f, "definition")
    strong = re.compile(r"most|central|crucial|key|fundamental|core|consequential|essential|primary|decisive|main", re.I)
    sal = [(0 if strong.search(r[4]) else 1, f) for f, r in facts.items() if r[3] == "is qualified as" and r[1] in facts]
    for _, f in sorted(sal)[:10]:                                          # 3. explicit salience (strong markers first, capped)
        take(facts[f][1], f"qualified as {facts[f][4]}"); take(f, "salience")
    foils = 0
    for f, r in facts.items():                                           # 4. foils and their rebuttals (capped)
        if r[6] == "rebutted-claim" and foils < 6:
            take(f, "foil"); foils += 1
            for g, q in facts.items():
                if q[3] == "is raised to rebut" and q[4] == f:
                    take(q[1], "rebuts a foil"); take(g, "rebuttal")
    spread = collections.defaultdict(set)                                # 5. central assertions about hubs
    for f, r in facts.items():
        for c_ in (r[1], r[4]):
            spread[c_].add(f.split(":")[0])
    cands = [(len(spread[r[1]]) + len(spread[r[4]]), f) for f, r in facts.items()
             if r[6] in ("assertion", "definition") and (r[1] in hub_names or r[4] in hub_names) and not FACT_REF.match(r[1])]
    for _, f in sorted(cands, reverse=True):
        take(f, "central claim about a hub")
    extras = {"anchors": sorted({(x, m) for c, x, m, f in anchors}), "set_aside": sorted({x for c, x, f in aside})}
    return header, hubs, order, why, facts, extras


def render(header, hubs, order, why, facts, extras=None):
    lines = ["# Structural summary", ""]
    probs = collections.defaultdict(list)
    for pn, cn, st, via in header:
        probs[pn].append((cn, st, via))
    for pn, items in probs.items():
        done = [i for i in items if i[1] == "addressed"]
        lines.append(f"**Problem:** {pn} — {len(done)}/{len(items)} components addressed by the document's own apparatus.")
        lines.append("Addressed: " + "; ".join(f"{cn} (via {via})" for cn, st, via in done) + ".")
        rest = [cn for cn, st, _ in items if st != "addressed"]
        if rest:
            lines.append("Not addressed: " + ", ".join(rest) + ".")
    lines.append("**Hubs:** " + ", ".join(f"{m} ({n})" for m, n, d1 in hubs[:5]) + ".")
    if extras:
        if extras["anchors"]:
            lines.append("**Anchor (the phenomenon reduced directly to the hub — the entry point the author chose):** " + "; ".join(f"{c} ↔ {m}" for c, m in extras["anchors"]) + ". The solution is particular to this choice; another anchor would give another argument.")
        if extras["set_aside"]:
            lines.append("**Set aside (named only to be rejected as the anchor):** " + ", ".join(extras["set_aside"]) + ".")
    lines += ["", f"```gellish-summary", "# selected {0} rows; reason in the last column".format(len(order))]
    for f in order:
        r = facts[f]
        lines.append(f"{f} | {r[1]} | {r[3]} | {r[4]} | {r[5] or '-'} | {r[6]} | {why[f]}")
    lines.append("```")
    return "\n".join(lines) + "\n"


def main(out_dir, facts_dir, budget=80, path=None):
    text = render(*build(out_dir, facts_dir, budget))
    if path:
        pathlib.Path(path).write_text(text, encoding="utf-8")
    return text
