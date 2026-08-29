"""Semantic diff of two closures: edges added, removed, or re-levelled between two runs."""
import csv, pathlib

LEVEL = {"4": "asserted", "3": "hedged", "2": "conjectured", "1": "contested", "0": "none"}


def load_kb(out_dir):
    kb = {}
    p = pathlib.Path(out_dir) / "kb.csv"
    with p.open(newline="") as f:
        for l, rel, r, lv, origin in csv.reader(f, delimiter="\t"):
            key = (l, rel, r)
            if key not in kb or int(lv) > int(kb[key][0]):
                kb[key] = (lv, origin)
    return kb


def load_set(out_dir, name):
    p = pathlib.Path(out_dir) / f"{name}.csv"
    if not p.exists():
        return set()
    with p.open(newline="") as f:
        return {tuple(r) for r in csv.reader(f, delimiter="\t")}


def render(a_out, b_out, label_a="A", label_b="B", stated_only=False):
    ka, kb = load_kb(a_out), load_kb(b_out)
    if stated_only:
        ka = {k: v for k, v in ka.items() if v[1] == "stated"}
        kb = {k: v for k, v in kb.items() if v[1] == "stated"}
    added = sorted(k for k in kb if k not in ka)
    removed = sorted(k for k in ka if k not in kb)
    relev = sorted((k, ka[k][0], kb[k][0]) for k in ka if k in kb and ka[k][0] != kb[k][0])
    out = [f"# Semantic diff: {label_a} → {label_b}", "",
           f"| | {label_a} | {label_b} |", "|---|---:|---:|",
           f"| edges | {len(ka)} | {len(kb)} |",
           f"| added | | {len(added)} |", f"| removed | {len(removed)} | |", f"| re-levelled | | {len(relev)} |", ""]
    for name in ("contradiction", "commitment_tension", "role_tension", "violation"):
        sa, sb = load_set(a_out, name), load_set(b_out, name)
        out.append(f"| {name} | {len(sa)} | {len(sb)} | new {len(sb - sa)}, gone {len(sa - sb)} |")
    out.append("")

    def edge(k, lv):
        l, rel, r = k
        return f"- [{LEVEL.get(lv, lv)}] {l} —{rel}→ {r}"
    out += ["## Added", ""] + [edge(k, kb[k][0]) + ("" if kb[k][1] == "stated" else f"  ({kb[k][1]})") for k in added[:200]]
    if len(added) > 200:
        out.append(f"- … {len(added) - 200} more")
    out += ["", "## Removed", ""] + [edge(k, ka[k][0]) + ("" if ka[k][1] == "stated" else f"  ({ka[k][1]})") for k in removed[:200]]
    if len(removed) > 200:
        out.append(f"- … {len(removed) - 200} more")
    out += ["", "## Re-levelled", ""] + [f"- {k[0]} —{k[1]}→ {k[2]}: {LEVEL.get(a, a)} → {LEVEL.get(b, b)}" for k, a, b in relev[:200]]
    return "\n".join(out) + "\n"
