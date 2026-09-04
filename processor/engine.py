"""The deterministic part of the state processor: stages 2–6 of PROCESSOR.md as a program.

The LLM does stage 1 (which signals the chunk names, and what each costs in words) and stage 7 (which cost
relations the chunk installs). Everything between is arithmetic over the profile and the prior state, and
arithmetic is better done by something that cannot round creatively. This is also the boundary phase 2 unloads
across: what this file computes is what hot.dl will compute.

Usage:
    python -m processor.engine [--target target.txt] <profile.txt> <candidates.tsv> <out.txt> [prior-state.txt]
    python -m processor.engine validate <target.txt> <state-1.txt> ... <state-N.txt>

candidates.tsv — one line per sensory candidate: item<TAB>cost in words[<TAB>stimulus<TAB>need<TAB>delta]
    (the optional trailing three columns install a path, stage 7), or item<TAB>cost<TAB>short for a short form
    that re-names a concept the reader already holds; if memory does not hold it, it is an unknown token.
"""
import re, sys, pathlib

ROW = re.compile(r"^(F\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*)$")


def rows(path):
    for line in pathlib.Path(path).read_text().splitlines():
        m = ROW.match(line.strip())
        if m:
            yield m.groups()


def load_profile(path):
    p = {"params": {}, "needs": {}, "paths": {}, "assoc": {}, "memory": {},
         "klass": {}, "level": {}, "baseline": {}}
    for _, l, rel, r, v, _, note in rows(path):
        if rel == "is in memory of":                                # what the reader brings: prior knowledge
            m = re.search(r"cost (\d+)", note)
            p["memory"][l] = (float(v), int(m.group(1)) if m else 2)
        elif rel == "has parameter":
            p["params"][r] = float(v); p["reader"] = l
        elif rel == "is a need of":
            p["needs"][l] = float(v)
        elif rel == "is classified as a":                          # basal | psychophysiological | psychological
            p["klass"][l] = r
        elif rel == "has satisfaction level":                       # s in [0, 1]; the deficit 1 - s is what drives
            p["level"][l] = float(r); p["baseline"][l] = float(v) if v not in ("", "-") else float(r)
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
        elif rel == "has satisfaction level":
            p["level"][l] = float(r)
        elif rel == "has dominant need":
            p["program"] = r; p["switches"] = int(v) if v not in ("", "-") else 0
        elif rel == "attends to":
            p["reality yield"] = float(v) if v not in ("", "-") else None
            m = re.search(r"fantasy yield ([\d.]+)", note)
            p["fantasy yield"] = float(m.group(1)) if m else 0.0
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


def weight(n, p):
    """The need portrait: a need's weight is its class priority times its deficit, and only while the need is
    active — necessary now, or reachable now. Without a portrait it is the static weight the profile gave it."""
    if n in p["level"]:
        if "active" in p and n not in p["active"]:
            return 0.0
        prio = p["params"].get(p["klass"].get(n, "psychological"), 1.0)
        return prio * (1.0 - p["level"][n])
    return p["needs"].get(n, 0.0)


def activate(p, present):
    """The portrait is the whole space of goals; the active needs are those that must or can be pursued now."""
    if not p["level"]:
        return
    theta = p["params"].get("necessity", 0.5)
    reachable = {n for (x, n) in p["paths"] if x in present}
    p["active"] = {n for n in p["level"] if (1.0 - p["level"][n]) >= theta or n in reachable}


def own_c(item, p):
    """An entity's emotional response: what it does to the needs, weighted by the portrait; or the floor."""
    resp = sum(abs(d) * weight(n, p) for (x, n), d in p["paths"].items() if x == item)
    return resp if resp > 0.0 else p["params"]["floor"]


def step(p, prior_field, memory, sensory, new_paths, t=None):
    P = p["params"]; k = P["k"]; B = P["budget"]
    t = t or load_target(None)
    # the motor field: one program has the channel. The scenario's program is the need the target serves;
    # when another program leads, the reader's continuation is not reading, and this chunk is not received.
    scenario = P.get("scenario need", "understanding") if isinstance(P.get("scenario need", "understanding"), str) else "understanding"
    elsewhere = p.get("program", "-") not in ("-", scenario)
    fantasy_pays = p.get("fantasy yield", 0.0) >= (p.get("reality yield") or 0.0)
    if elsewhere and fantasy_pays and p.get("gate", True):
        sensory = []
        p["received"] = False
    else:
        p["received"] = True
    for (x, n), d in new_paths:
        p["paths"][(x, n)] = d

    activate(p, set(prior_field) | set(memory) | {i for i, _ in sensory})
    # against the target: prerequisites, forbidden names, and the confusion a missing prerequisite costs
    notes, confusion = [], []
    if "active" in p:
        notes.append("active needs: " + ", ".join(sorted(p["active"])))
    named_so_far = {i for i, _ in sensory}          # a chunk is one batch: no order inside it
    for item, _ in sensory:
        if item in t["forbidden"]:
            notes.append(f"forbidden named: {item}")
        missing = [q for q in t["requires"].get(item, [])
                   if q not in prior_field and q not in memory and q not in named_so_far]
        for q in missing:
            notes.append(f"prerequisite missing: {item} needs {q}")
            confusion.append(-P.get("confusion", 0.0) * weight("understanding", p))
        if item in t["reach"] and not missing and (item, "understanding") not in p["paths"]:
            # named on its ground: the concept now satisfies understanding, and that is what keeps it
            p["paths"][(item, "understanding")] = P.get("comprehension", 0.0)
            notes.append(f"understood: {item}")

    # candidates: item -> (C, cost, source, order)
    # Words buy cues; the Field holds items. A concept the reader has understood is held at the size of its
    # name, however many words introduced it — comprehension is compression. What is not understood is held at
    # the words it took, and what memory already holds is held at the size memory recorded.
    cand = {}
    order = 0
    for item, cost in sensory:                                     # stage 1 (given)
        c = max(own_c(item, p), memory[item][0] if item in memory else 0.0)
        if item in memory:
            cost = min(cost, memory[item][1])
        elif (item, "understanding") in p["paths"]:
            cost = min(cost, len(item.split()))
        cand[item] = (min(c, 0.999), cost, "sensory", order); order += 1
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

    field, evicted, spent = {}, [], 0                           # stage 4
    for item, (c, cost, src, _) in ordered:
        if c < k:
            evicted.append((item, c, "below k")); continue
        if spent + cost <= B:
            field[item] = (c, cost, src); spent += cost
        else:
            evicted.append((item, c, f"no room: {cost} words, {B - spent} left"))

    present = set(field) | set(memory) | {i for i, _ in sensory}   # stage 5
    tail = [abs(d) * weight(n, p) * (1 if d > 0 else -1)
            for (x, n), d in p["paths"].items() if x in present and x not in field]
    tail += confusion                                              # what a word without its ground costs
    intensity = sum(abs(x) for x in tail)
    stats = {"intensity": intensity, "valence": sum(tail), "count": len(tail),
             "spread": 1.0 - sum((abs(x) / intensity) ** 2 for x in tail) if intensity else 0.0}

    new_memory = {i: (c, cost) for i, (c, cost, _) in field.items()}   # stage 6
    stable = p.get("stable", {})
    for item, (c, cost) in memory.items():
        if item in field:
            continue
        cc = max(c * P["decay"], stable.get(item, 0.0))
        if cc >= k:
            new_memory[item] = (cc, cost)
    # the program: the need whose response holds most of the Field. A change of program brought about by a
    # sensory item that is not a target concept is a distraction — the girl walking past the chess game.
    mass = {}
    for (x, n), d in p["paths"].items():
        if x in field:
            mass[n] = mass.get(n, 0.0) + abs(d) * weight(n, p)
    program = max(mass, key=mass.get) if mass else "-"
    # conflict: only one program can have the motor channel, so the felt quantity is not the switch but how
    # nearly the runner-up matches the leader — 0 is one program alone, 1 is the channel contested every step
    comp = {}
    for x in field:
        best = max(((abs(d) * weight(n, p), n) for (y, n), d in p["paths"].items() if y == x), default=(0.0, "none"))
        comp[best[1]] = comp.get(best[1], 0) + 1
    p["components"] = comp
    ranked = sorted(mass.values(), reverse=True)
    p["conflict"] = (ranked[1] / ranked[0]) if len(ranked) > 1 and ranked[0] > 0 else 0.0
    if mass:
        notes.append("need mass in the Field: " + ", ".join(f"{n} {m:.2f}" for n, m in sorted(mass.items(), key=lambda kv: -kv[1])))
    prior_program = p.get("program", "-")
    p["switches"] = p.get("switches", 0)
    if program != prior_program and prior_program != "-":
        p["switches"] += 1
        culprit = [x for x, _ in sensory if x in field and x not in t["reach"]
                   and any(m == program for (y, m) in p["paths"] if y == x)]
        notes.append(f"program {prior_program} -> {program}" + (f": distraction by {', '.join(culprit)}" if culprit else ""))
    p["motor"] = "reads on" if program in ("-", scenario) else f"acts on {program}"
    p["program"] = program
    # two interfaces: the environment, and the model of it. Reality's yield is the response the received chunk
    # delivered (a running estimate of what the next one will); fantasy's is the best response the model can
    # produce from the Field by one more association. The mode is where the channel is; the yields are what a
    # switching rule would compare. Measured here, not yet acted on.
    got = [c for x, (c, _, src) in field.items() if src == "sensory" and any(x == y for y, _ in sensory)]
    if p.get("received", True) and got:
        prev = p.get("reality yield", None)
        now = sum(got) / len(got)
        p["reality yield"] = now if prev is None else 0.5 * prev + 0.5 * now
    fant = [min(own_c(i, p) * w, 0.999) for cue in field for i, w in p["assoc"].get(cue, []) if i not in field]
    p["fantasy yield"] = max(fant) if fant else 0.0
    p["mode"] = "reality" if p.get("received", True) else "fantasy"
    notes.append(f"mode {p['mode']}: reality yield {p.get('reality yield', 0.0):.2f}, fantasy yield {p['fantasy yield']:.2f}")

    if p["level"]:                                                  # the portrait moves
        rate = P.get("satiation", 0.5); home = P.get("homeostasis", 0.3)
        fresh = {i for i, _ in sensory} & set(field)                # only what is new this step moves a need;
        grasped = {ln.split(": ", 1)[1] for ln in notes if ln.startswith("understood: ")}
        for n in list(p["level"]):                                  # holding a thought does not feed twice,
            push = 0.0                                              # and understanding is fed once, when it happens
            for (x, m), d in p["paths"].items():
                if m != n or x not in fresh:
                    continue
                if x in t["reach"] and m == "understanding" and x not in grasped:
                    continue
                push += d
            lv = p["level"][n] + rate * push
            lv = lv + home * (p["baseline"][n] - lv)
            p["level"][n] = min(max(lv, 0.0), 0.999)
    for fb, proxies in t["induced"].items():                        # felt without a name
        v = sum(new_memory[q][0] * w for q, w in proxies if q in new_memory)
        notes.append(f"felt {fb}: {v:.2f}")
    return field, evicted, stats, new_memory, spent, notes


def render(reader, n, field, evicted, stats, memory, spent, new_paths, notes=(), levels=None, grasped=(), comprehension=0.0, program="-", switches=0, conflict=0.0, motor="reads on", components=None, received=True, mode="reality", ry=0.0, fy=0.0):
    levels = levels or {}; components = components or {}
    out = [f"# state after step {n}   (field {spent} words)", "",
           "# --- field of consciousness: what the reader can report" + ("" if received else "   [chunk not received: the motor field was elsewhere]")]
    i = 1
    for item, (c, cost, src) in field.items():
        out.append(f"F{i:04d} | {item} | is in the field of | {reader} | {c:.2f} | assertion | {src}; cost {cost}"); i += 1
    if components:
        out.append(f"F{i:04d} | {reader} | has consciousness components | " + ", ".join(f"{k} {v}" for k, v in sorted(components.items(), key=lambda kv: -kv[1])) + " | - | assertion | items by the need each answers to; more than one is a split"); i += 1
    for key in ("intensity", "valence", "count", "spread"):
        out.append(f"F{i:04d} | {reader} | has tail statistic | {key} | {stats[key]:.2f} | assertion | the field of mind, as it reaches consciousness: mass, no names"); i += 1
    out.append("")
    out.append("# --- motor field: the one continuation")
    out.append(f"F{i:04d} | {reader} | does | {motor} | - | assertion | the program that has the channel"); i += 1
    out.append(f"F{i:04d} | {reader} | attends to | {mode} | {ry:.2f} | assertion | the interface in use; value = reality yield so far; fantasy yield {fy:.2f}"); i += 1
    out.append("")
    out.append("# --- long-term memory")
    for item, (c, cost) in memory.items():
        out.append(f"F{i:04d} | {item} | is in memory of | {reader} | {c:.2f} | assertion | cost {cost}"); i += 1
    out.append("")
    out.append("# --- need portrait")
    for (x, nd), d in new_paths:
        out.append(f"F{i:04d} | {x} | has satisfaction delta | {nd} | {d} | assertion | established by the chunk"); i += 1
    for x in grasped:
        out.append(f"F{i:04d} | {x} | has satisfaction delta | understanding | {comprehension} | assertion | understood"); i += 1
    for n, lv in levels.items():
        out.append(f"F{i:04d} | {n} | has satisfaction level | {lv:.3f} | - | assertion | need state"); i += 1
    if program != "-":
        out.append(f"F{i:04d} | {reader} | has dominant need | {program} | {switches} | assertion | the program: an aggregate, no keys; value = switches so far"); i += 1
        out.append(f"F{i:04d} | {reader} | has conflict level | {conflict:.2f} | - | assertion | runner-up program's mass over the leader's: competition for the one motor channel"); i += 1
    out.append("")
    out.append("# --- field of mind (blackboard): represented, not conscious — the analyst's view, not the reader's")
    for item, c, why in evicted:
        out.append(f"#   {item} ({c:.2f}): {why}")
    out.append("")
    out.append("# --- trace")
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
    top = p["params"].get("comprehension", 0.0) * weight("understanding", p)
    out = [f"a concept named on its ground reaches {top:.2f}; a proxy with no need sits at the floor {p['params']['floor']}"]
    # the last Field: how many of the concepts that must be reached can be held at once, at the size of their
    # names, and what a concept one chunk old is worth — together they bound what any final chunk can leave
    B = p["params"]["budget"]; decay = p["params"]["decay"]
    names = sum(len(c.split()) for c in t["reach"])
    aged = top * decay
    strict = [c for c, need in t["reach"].items() if need > aged]
    out.append(f"the last Field holds {B} words; the {len(t['reach'])} concepts to reach cost {names} as names; "
               f"one chunk old a concept is worth {aged:.2f}")
    if names > B and strict:
        out.append(f"INFEASIBLE  {len(strict)} concepts need more than {aged:.2f} and cannot all be in the last Field: "
                   + ", ".join(strict))
    else:
        out.append("PASS  every concept to reach can be in the last Field or survive one chunk old")
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
    field, memory = {}, dict(p["memory"])
    p["stable"] = {i: c for i, (c, _) in p["memory"].items()}     # consolidated: never decays below this
    for prior in priors:
        field, memory = load_state(prior, p)
    sensory, new_paths, short_dropped = [], [], []
    for line in pathlib.Path(candidates).read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        cols = [c.strip() for c in line.split("\t")]
        if len(cols) >= 3 and cols[2] == "short":                  # a short form re-names only what memory holds
            if cols[0] in memory or cols[0] in field:
                sensory.append((cols[0], int(cols[1])))
            else:
                short_dropped.append(cols[0])
            continue
        sensory.append((cols[0], int(cols[1])))
        if len(cols) >= 5:
            new_paths.append(((cols[2], cols[3]), float(cols[4])))
    n = 1
    if priors:
        import re as _re
        m = _re.search(r"# state after step (\d+)", pathlib.Path(priors[-1]).read_text())
        n = int(m.group(1)) + 1 if m else len(priors) + 1
    f, e, s, m, spent, notes = step(p, field, memory, sensory, new_paths, t)
    notes += [f"short form of {x} with {x} not in memory: an unknown token, ignored" for x in short_dropped]
    grasped = [x for (x, nd) in p["paths"] if nd == "understanding" and x in t["reach"]]
    pathlib.Path(out).write_text(render(p["reader"], n, f, e, s, m, spent, new_paths, notes, p["level"],
                                        grasped, p["params"].get("comprehension", 0.0), p.get("program", "-"), p.get("switches", 0), p.get("conflict", 0.0),
                                        p.get("motor", "reads on"), p.get("components"), p.get("received", True), p.get("mode", "reality"), p.get("reality yield", 0.0), p.get("fantasy yield", 0.0)))
    print(pathlib.Path(out).read_text())


if __name__ == "__main__":
    main(sys.argv[1:])
