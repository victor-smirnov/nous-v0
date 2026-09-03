"""The deterministic part of the state processor: stages 2–6 of PROCESSOR.md as a program.

The LLM does stage 1 (which signals the chunk names, and what each costs in words) and stage 7 (which cost
relations the chunk installs). Everything between is arithmetic over the profile and the prior state, and
arithmetic is better done by something that cannot round creatively. This is also the boundary phase 2 unloads
across: what this file computes is what hot.dl will compute.

Usage:
    python -m processor.engine [--target target.txt] <profile.txt> <candidates.tsv> <out.txt> [prior-state.txt]
    python -m processor.engine validate <target.txt> <state-1.txt> ... <state-N.txt>

candidates.tsv — one line per sensory candidate: item<TAB>cost in words[<TAB>stimulus<TAB>need<TAB>delta]
    (the optional trailing three columns install a path, stage 7).
"""
import re, sys, pathlib

ROW = re.compile(r"^(F\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*)$")


def rows(path):
    for line in pathlib.Path(path).read_text().splitlines():
        m = ROW.match(line.strip())
        if m:
            yield m.groups()


def load_profile(path):
    p = {"params": {}, "needs": {}, "paths": {}, "assoc": {}}
    for _, l, rel, r, v, _, _ in rows(path):
        if rel == "has parameter":
            p["params"][r] = float(v); p["reader"] = l
        elif rel == "is a need of":
            p["needs"][l] = float(v)
        elif rel == "has satisfaction delta":
            p["paths"][(l, r)] = float(v)
        elif rel == "is associated with":
            p["assoc"].setdefault(l, []).append((r, float(v)))
    return p


def load_state(path, p):
    """Field, memory, and installed paths from a prior state file. Costs ride in the note as `cost N`."""
    field, memory = {}, {}
    for _, l, rel, r, v, _, note in rows(path):
        m = re.search(r"cost (\d+)", note)
        cost = int(m.group(1)) if m else int(p["params"]["default cost"])
        if rel == "is in the field of":
            field[l] = (float(v), cost)
        elif rel == "is in memory of":
            memory[l] = (float(v), cost)
        elif rel == "has satisfaction delta":
            p["paths"][(l, r)] = float(v)
    return field, memory


def load_target(path):
    """The target state: what must reach memory, in what order, what must never be named, what must be felt."""
    t = {"reach": {}, "requires": {}, "forbidden": set(), "induced": {}, "feel": {}}
    if not path:
        return t
    for _, l, rel, r, v, _, _ in rows(path):
        if rel == "must reach":
            t["reach"][l] = float(r)
        elif rel == "requires":
            t["requires"].setdefault(l, []).append(r)
        elif rel == "must not be named":
            t["forbidden"].add(l)
        elif rel == "is induced by":
            t["induced"].setdefault(l, []).append((r, float(v)))
        elif rel == "must feel":
            t["feel"][l] = float(r)
    return t


def own_c(item, p):
    """A plain entity scores the strongest cost signal it is the stimulus of, or the floor."""
    best = [abs(d) * p["needs"].get(n, 0.0) for (x, n), d in p["paths"].items() if x == item]
    return max(best) if best else p["params"]["floor"]


def step(p, prior_field, memory, sensory, new_paths, t=None):
    P = p["params"]; k = P["k"]; B = P["budget"]
    t = t or load_target(None)
    for (x, n), d in new_paths:
        p["paths"][(x, n)] = d

    # against the target: prerequisites, forbidden names, and the confusion a missing prerequisite costs
    notes, confusion = [], []
    named_so_far = {i for i, _ in sensory}          # a chunk is one batch: no order inside it
    for item, _ in sensory:
        if item in t["forbidden"]:
            notes.append(f"forbidden named: {item}")
        missing = [q for q in t["requires"].get(item, [])
                   if q not in prior_field and q not in memory and q not in named_so_far]
        for q in missing:
            notes.append(f"prerequisite missing: {item} needs {q}")
            confusion.append(-P.get("confusion", 0.0) * p["needs"].get("understanding", 0.0))
        if item in t["reach"] and not missing and (item, "understanding") not in p["paths"]:
            # named on its ground: the concept now satisfies understanding, and that is what keeps it
            p["paths"][(item, "understanding")] = P.get("comprehension", 0.0)
            notes.append(f"understood: {item}")

    # candidates: item -> (C, cost, source, order)
    cand = {}
    order = 0
    for item, cost in sensory:                                     # stage 1 (given)
        cand[item] = (min(own_c(item, p), 0.999), cost, "sensory", order); order += 1
    for item, (c, cost) in prior_field.items():                    # carried over
        cc = min(c * P["persistence"], 0.999)
        if item not in cand or cc > cand[item][0]:
            cand[item] = (cc, cost, "carried", cand[item][3] if item in cand else order); order += 1
    cues = [i for i, _ in sensory] + list(prior_field)             # stage 2: one hop
    for cue in cues:
        for item, w in p["assoc"].get(cue, []):
            cc = min(own_c(item, p) * w, 0.999)
            cost = memory[item][1] if item in memory else int(P["default cost"])
            if item not in cand or cc > cand[item][0]:
                keep_order = cand[item][3] if item in cand else order
                cand[item] = (cc, cost, f"associative via {cue}", keep_order); order += 1

    rank = {"sensory": 0, "carried": 1}
    ordered = sorted(cand.items(), key=lambda kv: (-kv[1][0], rank.get(kv[1][2], 2), kv[1][3]))

    field, evicted, spent, blocker = {}, [], 0, None            # stage 4
    for item, (c, cost, src, _) in ordered:
        if c < k:
            evicted.append((item, c, "below k")); continue
        if blocker is None and spent + cost <= B:
            field[item] = (c, cost, src); spent += cost
        else:
            if blocker is None:
                blocker = next(reversed(field), None)
            evicted.append((item, c, f"displaced by {blocker}"))

    present = set(field) | set(memory) | {i for i, _ in sensory}   # stage 5
    tail = [abs(d) * p["needs"].get(n, 0.0) * (1 if d > 0 else -1)
            for (x, n), d in p["paths"].items() if x in present and x not in field]
    tail += confusion                                              # what a word without its ground costs
    intensity = sum(abs(x) for x in tail)
    stats = {"intensity": intensity, "valence": sum(tail), "count": len(tail),
             "spread": 1.0 - sum((abs(x) / intensity) ** 2 for x in tail) if intensity else 0.0}

    new_memory = {i: (c, cost) for i, (c, cost, _) in field.items()}   # stage 6
    for item, (c, cost) in memory.items():
        if item not in field and c * P["decay"] >= k:
            new_memory[item] = (c * P["decay"], cost)
    for fb, proxies in t["induced"].items():                        # felt without a name
        v = sum(new_memory[q][0] * w for q, w in proxies if q in new_memory)
        notes.append(f"felt {fb}: {v:.2f}")
    return field, evicted, stats, new_memory, spent, notes


def render(reader, n, field, evicted, stats, memory, spent, new_paths, notes=()):
    out = [f"# state after step {n}   (field {spent} words)"]
    i = 1
    for item, (c, cost, src) in field.items():
        out.append(f"F{i:04d} | {item} | is in the field of | {reader} | {c:.2f} | assertion | {src}; cost {cost}"); i += 1
    for key in ("intensity", "valence", "count", "spread"):
        out.append(f"F{i:04d} | {reader} | has tail statistic | {key} | {stats[key]:.2f} | assertion | -"); i += 1
    for item, (c, cost) in memory.items():
        out.append(f"F{i:04d} | {item} | is in memory of | {reader} | {c:.2f} | assertion | cost {cost}"); i += 1
    for (x, nd), d in new_paths:
        out.append(f"F{i:04d} | {x} | has satisfaction delta | {nd} | {d} | assertion | established by the chunk"); i += 1
    out.append("")
    out.append("# trace — the analyst's view, not the reader's")
    for item, c, why in evicted:
        out.append(f"#   evicted {item} ({c:.2f}): {why}")
    for line in notes:
        out.append(f"#   {line}")
    return "\n".join(out) + "\n"


def validate(target, states):
    """The whole trajectory against the target: reached, felt, never named, named in order."""
    t = load_target(target)
    final = {l: float(v) for _, l, rel, r, v, _, _ in rows(states[-1]) if rel == "is in memory of"}
    text = "\n".join(pathlib.Path(s).read_text() for s in states)
    last = pathlib.Path(states[-1]).read_text()
    report = []
    for c, need in t["reach"].items():
        got = final.get(c, 0.0)
        report.append(("PASS" if got >= need else "FAIL", f"reach {c}: {got:.2f} (needs {need})"))
    for fb, need in t["feel"].items():
        m = re.findall(rf"felt {re.escape(fb)}: ([\d.]+)", last)
        got = float(m[-1]) if m else 0.0
        report.append(("PASS" if got >= need else "FAIL", f"feel {fb}: {got:.2f} (needs {need})"))
    bad = re.findall(r"forbidden named: (.*)", text)
    report.append(("FAIL" if bad else "PASS", "never named: " + (", ".join(bad) if bad else "clean")))
    miss = re.findall(r"prerequisite missing: (.*)", text)
    report.append(("FAIL" if miss else "PASS", "in order: " + ("; ".join(miss) if miss else "clean")))
    return report


def ceiling(profile, target):
    """What the profile can reach at all: the most a concept can score, and the most a forbidden idea can be felt."""
    p = load_profile(profile); t = load_target(target)
    top = p["params"].get("comprehension", 0.0) * p["needs"].get("understanding", 0.0)
    out = [f"a concept named on its ground reaches {top:.2f}; a proxy with no need sits at the floor {p['params']['floor']}"]
    for fb, proxies in t["induced"].items():
        best = sum((top if q in t["reach"] else own_c(q, p)) * w for q, w in proxies)
        need = t["feel"].get(fb)
        out.append(f"{'PASS' if need is None or best >= need else 'INFEASIBLE'}  feel {fb}: ceiling {best:.2f}" + (f" (needs {need})" if need is not None else ""))
    return out


def main(argv):
    if argv and argv[0] == "validate":
        for verdict, line in validate(argv[1], argv[2:]):
            print(f"{verdict}  {line}")
        return
    if argv and argv[0] == "ceiling":
        print("\n".join(ceiling(argv[1], argv[2])))
        return
    target = None
    if argv and argv[0] == "--target":
        target, argv = argv[1], argv[2:]
    profile, candidates, out, *priors = argv
    p = load_profile(profile)
    t = load_target(target)
    field, memory = {}, {}
    for prior in priors:
        field, memory = load_state(prior, p)
    sensory, new_paths = [], []
    for line in pathlib.Path(candidates).read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.split("\t")
        sensory.append((cols[0].strip(), int(cols[1])))
        if len(cols) >= 5:
            new_paths.append(((cols[2].strip(), cols[3].strip()), float(cols[4])))
    n = 1
    if priors:
        import re as _re
        m = _re.search(r"# state after step (\d+)", pathlib.Path(priors[-1]).read_text())
        n = int(m.group(1)) + 1 if m else len(priors) + 1
    f, e, s, m, spent, notes = step(p, field, memory, sensory, new_paths, t)
    pathlib.Path(out).write_text(render(p["reader"], n, f, e, s, m, spent, new_paths, notes))
    print(pathlib.Path(out).read_text())


if __name__ == "__main__":
    main(sys.argv[1:])
