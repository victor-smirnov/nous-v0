"""Render the bootstrap library's output: one block per case (spec/bootstrap-library.md)."""
import collections, csv, pathlib

ORDER = ["level", "missing condition", "valence", "conflict", "epistemic quale", "HOCP",
         "functional deficit", "silent need"]


def tsv(p):
    p = pathlib.Path(p)
    return list(csv.reader(p.open(newline=""), delimiter="\t")) if p.exists() else []


def render(out_dir):
    out = pathlib.Path(out_dir)
    rows = tsv(out / "case_state.csv")
    if not rows:
        return "no cases in the input (a case needs `X | is a case of | <kind>` and the theory layer on)\n"
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for s, k, v in rows:
        by[s][k].append(v)
    sig = collections.defaultdict(list)
    for s, x, n, v, lv in tsv(out / "emotional_signal.csv"):
        sig[s].append((x, n, float(v)))
    prof = {(s, x): float(t) for s, x, t in tsv(out / "emotional_profile.csv")}
    lines = ["# Observer states", ""]
    for s in sorted(by):
        lines.append(f"## {s}")
        for k in ORDER:
            for v in sorted(by[s].get(k, [])):
                lines.append(f"- **{k}**: {v}")
        for k in sorted(set(by[s]) - set(ORDER)):
            for v in sorted(by[s][k]):
                lines.append(f"- **{k}**: {v}")
        if sig[s]:
            lines.append("- **emotional profile**:")
            for x in sorted({x for x, _, _ in sig[s]}):
                parts = ", ".join(f"{n} {v:+.2f}" for xx, n, v in sorted(sig[s]) if xx == x)
                lines.append(f"    - {x}: {parts} → {prof.get((s, x), 0):+.2f}")
        lines.append("")
    return "\n".join(lines) + "\n"
