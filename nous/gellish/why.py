#!/usr/bin/env python3
"""Explain derivations: why does the reasoner believe a tuple?

Runs Soufflé in provenance mode (-t explain) on the last run's facts and renders the proof
tree with the noise removed: source rows of the tables and dictionary facts are the leaves,
rules are the nodes.

  nous gellish why contradiction                     every contradiction
  nous gellish why contradiction entailment          contradictions of one kind (substring match on columns)
  nous gellish why role_tension
  nous gellish why commitment_tension C02:F0123
  nous gellish why kb "freedom of B" "is classified as a" "causal break"
  nous gellish why 'entails_best("C01:F0058","C01:F0059",4,2)'      raw atom

Needs work/ from the last `nous gellish check`. Each call re-evaluates the program once (~1 s).
"""
import csv, json, pathlib, re, subprocess, sys

FACTS = OUT = PROV = REASONER = None
NUMERIC = {"lv", "n", "d"}
BORING = re.compile(r'^(!?\w+\(.*\)|[-\d]+ (=|!=|>|<|>=|<=) [-\d]+)$')
HIDE = {"intent_level", "level_name", "param", "minlevel", "maxdepth", "theory_level", "dict_level", "fact_level",
        "cap_level", "author", "rel_type", "d_relname", "rel_label", "d_concept", "d_name_lc", "entity_lc",
        "theory_coll", "theory_concept", "up", "rel_sub", "kind_ok", "entity", "less_specific", "dict_edge"}

facts, relname, concept = {}, {}, {}


def load(ws):
    global FACTS, OUT, PROV, REASONER
    FACTS, OUT, PROV, REASONER = ws.facts, ws.out, ws.prov, ws.reasoner
    with (FACTS / "fact.facts").open(newline="") as f:
        for r in csv.reader(f, delimiter="\t"):
            facts[r[0]] = r
    p = FACTS / "d_relname.facts"
    if p.exists():
        for line in p.read_text().splitlines():
            u, n = line.split("\t"); relname[u] = n
    for line in (FACTS / "d_concept.facts").read_text(encoding="utf-8").splitlines():
        u, n = line.split("\t", 1); concept[u] = n


def show_fact(fid, width=110):
    if fid not in facts:
        return fid
    _, l, rel, ph, r, val, it, ctx, tbl, _ = facts[fid]
    l2 = show_fact(l, 40) if l in facts else l
    r2 = show_fact(r, 40) if r in facts else r
    s = f"{fid} ⟨{l2} {ph} {r2}" + (f" [{val}]" if val else "") + f"⟩ ({it})"
    return s if len(s) <= width else s[: width - 1] + "…"


def parse_atom(s):
    m = re.match(r'^(!?)(\w+)\((.*)\)$', s.strip())
    if not m:
        return None, None, None
    neg, name, body = m.groups()
    args = next(csv.reader([body], skipinitialspace=True))
    return neg, name, [a.strip() for a in args]


def render_leaf(s):
    neg, name, args = parse_atom(s)
    if name is None or name in HIDE or (neg and name):
        return None
    if name == "fact":
        return "row  " + show_fact(args[0])
    if name.startswith("d_"):
        a = [concept.get(x, x) for x in args]
        return f"dict {name[2:]}: " + " · ".join(a)
    if name in ("sem", "disjoint_rel", "rel_prop"):
        a = [relname.get(x, concept.get(x, x)) for x in args]
        return f"dict {name}: " + " · ".join(a)
    if name == "subproof":
        return None
    return f"{name}(" + ", ".join(args) + ")"


def render_node(s):
    neg, name, args = parse_atom(s)
    if name is None:
        return s
    if name in ("commit", "committed", "usable"):
        return f"{name} {show_fact(args[0], 80)} → level {args[1]}" + (f" pol {args[2]}" if len(args) > 2 else "")
    if name in ("holds", "holds_best"):
        return f"{name}: {args[0]} —{relname.get(args[1], args[1])}→ {args[2]} (level {args[3]})"
    if name in ("entails", "entails_best"):
        return f"{name}: {show_fact(args[0], 50)} ⇒ {show_fact(args[1], 50)} (level {args[2]}, depth {args[3]})"
    if name == "rf":
        return f"rf: {show_fact(args[0], 90)} as {args[2]}"
    if name == "ground":
        return f"ground: {args[0]} ↦ {concept.get(args[1], args[1])} ({args[1]})"
    if name in ("same", "same_lv", "same_best"):
        return f"{name}: {args[0]} ≡ {args[1]}" + (f" (level {args[2]})" if len(args) > 2 else "")
    return f"{name}(" + ", ".join(args) + ")"


def render(node, depth=0, out=None):
    out = out if out is not None else []
    pad = "  " * depth
    if "axiom" in node:
        t = render_leaf(node["axiom"])
        if t:
            out.append(pad + t)
        return out
    prem = node["premises"]
    neg, name, args = parse_atom(prem)
    # collapse the trivial commitment chain commit ← committed ← row into one line
    if name in ("commit", "committed", "usable") and args:
        out.append(pad + render_node(prem))
        for c in node.get("children", []):
            if "axiom" in c and c["axiom"].startswith("fact("):
                continue
            if "premises" in c and parse_atom(c["premises"])[1] in ("commit", "committed"):
                continue
            render(c, depth + 1, out)
        return out
    out.append(pad + render_node(prem) + "   " + node.get("rule-number", ""))
    for c in node.get("children", []):
        render(c, depth + 1, out)
    return out


def souffle_explain(commands):
    proc = subprocess.run(["souffle", "-t", "explain", "-F", str(FACTS), "-D", str(PROV), str(REASONER)],
                          input="format json\nsetdepth 40\n" + "\n".join(commands) + "\nexit\n",
                          capture_output=True, text=True)
    txt = proc.stdout
    dec, pos, objs = json.JSONDecoder(), 0, []
    while True:                                    # decode only the "proof" objects, skipping the "rules" dumps
        i = txt.find('"proof"', pos)
        if i < 0:
            break
        j = txt.find("{", i)
        try:
            obj, end = dec.raw_decode(txt, j)
            objs.append({"proof": obj}); pos = end
        except json.JSONDecodeError:
            pos = j + 1
    return objs, proc.stderr


def atom_from_row(rel, row):
    header = HEADERS.get(rel)
    parts = []
    for i, v in enumerate(row):
        col = header[i] if header and i < len(header) else ""
        parts.append(v if col in NUMERIC or re.fullmatch(r"-?\d+", v) and col in NUMERIC else json.dumps(v))
    return f"{rel}(" + ", ".join(parts) + ")"


HEADERS = {
    "contradiction": ["kind", "a", "b", "witness", "lv"],
    "commitment_tension": ["b", "stated", "derived", "via"],
    "cap_tension": ["f", "stated", "cap"],
    "violation": ["kind", "f", "detail"],
    "role_tension": ["f", "pos", "player", "expected", "grounded_as"],
    "kb": ["l", "rel", "r", "lv", "origin"],
    "entails_best": ["a", "b", "lv", "d"],
    "truncated": ["a", "b", "c"],
    "ground": ["x", "u"],
    "residual_phrase": ["phrase", "n"],
    "entity_span": ["x", "n"],
    "stat": ["k", "n"],
}


def main(a, ws):
    load(ws)
    PROV.mkdir(parents=True, exist_ok=True)
    if not a:
        sys.exit(__doc__)
    if "(" in a[0]:
        commands = ["explain " + a[0]]
    else:
        rel, filters = a[0], [x.lower() for x in a[1:]]
        p = OUT / f"{rel}.csv"
        if not p.exists():
            sys.exit(f"no {p}; relations with output: {', '.join(HEADERS)}")
        rows = [r for r in csv.reader(p.open(newline=""), delimiter="\t")
                if all(any(f in c.lower() for c in r) for f in filters)]
        if not rows:
            sys.exit("no matching rows")
        if len(rows) > 25:
            print(f"{len(rows)} rows match; explaining the first 25", file=sys.stderr)
            rows = rows[:25]
        commands = ["explain " + atom_from_row(rel, r) for r in rows]
    objs, err = souffle_explain(commands)
    if not objs:
        sys.exit("no proofs returned\n" + err[-2000:])
    for cmd, obj in zip(commands, objs):
        print("\n" + "═" * 100)
        print("\n".join(render(obj["proof"])))


if __name__ == "__main__":
    from .paths import Workspace
    main(sys.argv[1:], Workspace())
