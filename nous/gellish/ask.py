#!/usr/bin/env python3
"""Query the closed knowledge base: nous gellish ask "<entity or fact id>"

Prints everything kb.csv knows about the node (stated and derived, with commitment level),
plus contradictions/violations/tensions that mention it.
"""
import csv, pathlib, signal, sys
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

LEVEL = {"4": "asserted", "3": "hedged", "2": "conjectured", "1": "contested", "0": "none"}


def main(query, out_dir):
    q = query.lower()
    out = pathlib.Path(out_dir)

    def rows(name):
        p = out / f"{name}.csv"
        return list(csv.reader(p.open(newline=""), delimiter="\t")) if p.exists() else []

    hit = lambda *cells: any(q in c.lower() for c in cells)
    print(f"# {query}\n")
    print("## knowledge base")
    for l, rel, r, lv, origin in sorted(rows("kb"), key=lambda x: (x[4], x[1])):
        if hit(l, r):
            arrow = "⇒" if origin == "derived" else "→"
            print(f"  [{LEVEL[lv]:11}] {l} —{rel}{arrow} {r}" + (f"   ({origin})" if origin != "stated" else ""))
    for name, cols in (("contradiction", (1, 2, 3)), ("commitment_tension", (0, 3)), ("violation", (1, 2)), ("role_tension", (2,)), ("truncated", (0, 1, 2))):
        hits = [r for r in rows(name) if hit(*(r[i] for i in cols))]
        if hits:
            print(f"\n## {name}")
            for r in hits:
                print("  " + " | ".join(r))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "work/out")
