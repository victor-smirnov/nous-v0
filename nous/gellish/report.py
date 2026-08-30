#!/usr/bin/env python3
"""Summarise the reasoner's outputs as markdown."""
import collections, csv, io, pathlib, sys

OUT = FACTS = None
facts = {}
_buf = None


def print(*a, **k):                       # module-local: everything goes to the buffer
    import builtins
    builtins.print(*a, file=_buf, **k)


def rows(name):
    p = OUT / f"{name}.csv"
    if not p.exists():
        return []
    with p.open(newline="") as f:
        return list(csv.reader(f, delimiter="\t"))


def load_facts():
    facts.clear()
    with (FACTS / "fact.facts").open(newline="") as f:
        for r in csv.reader(f, delimiter="\t"):
            facts[r[0]] = r


def show(x, width=70):
    """Render a symbol; fact refs expand to their triple."""
    if x in facts:
        _, l, rel, ph, r, val, it, _, _, _ = facts[x]
        obj = f"{show(l, 30)} {ph} {show(r, 30)}" if rel != "other" else f"{l} {ph} {r}"
        if val:
            obj += f" [{val}]"
        s = f"{x} ⟨{obj}⟩ ({it})"
    else:
        s = x
    return s if len(s) <= width else s[: width - 1] + "…"


def section(title):
    print(f"\n## {title}\n")


def render(out_dir, facts_dir):
    """Return the markdown report for a finished run."""
    global OUT, FACTS, _buf
    OUT, FACTS, _buf = pathlib.Path(out_dir), pathlib.Path(facts_dir), io.StringIO()
    load_facts()
    print("# Gellish reasoner report\n")
    section("Stats")
    print("| metric | n |\n|---|---:|")
    for k, n in rows("stat"):
        print(f"| {k} | {n} |")

    section("Contradictions")
    c = rows("contradiction")
    if not c:
        print("none")
    by = collections.defaultdict(list)
    for kind, a, b, w, lv in c:
        by[kind].append((a, b, w, lv))
    for kind, items in by.items():
        print(f"\n### {kind} ({len(items)})\n")
        for a, b, w, lv in items[:25]:
            print(f"- {show(a)} ⟂ {show(b)}" + (f" — witness {show(w)}" if w else "") + f" (level {lv})")

    section("Commitment tensions (stated weaker than what committed premises entail)")
    t = rows("commitment_tension")
    if not t:
        print("none")
    for b, st, dv, via in t[:40]:
        print(f"- {show(b)}: stated **{st}**, entailed **{dv}** via {show(via, 60)}")

    section("Cap tensions (`has commitment` disagrees with intention)")
    t = rows("cap_tension")
    if not t:
        print("none")
    for f, st, cap in t[:40]:
        print(f"- {show(f)}: intention {st}, declared {cap}")

    section("Spec violations")
    v = rows("violation")
    cnt = collections.Counter(k for k, _, _ in v)
    print("| kind | n |\n|---|---:|")
    for k, n in cnt.most_common():
        print(f"| {k} | {n} |")
    for k, _ in cnt.most_common():
        ex = [(f, d) for kk, f, d in v if kk == k][:6]
        print(f"\n**{k}**")
        for f, d in ex:
            print(f"- {show(f)}" + (f" — {d}" if d else ""))

    section("Residual relation phrases (extension backlog)")
    r = sorted(rows("residual_phrase"), key=lambda x: -int(x[1]))
    print("| phrase | n |\n|---|---:|")
    for p, n in r[:40]:
        print(f"| {p} | {n} |")
    if len(r) > 40:
        print(f"| … {len(r) - 40} more | |")

    section("Structural abstract (thesis stratum)")
    ts = dict(rows("thesis_stat"))
    cov = rows("coverage"); hubs = sorted(rows("hub"), key=lambda x: (-int(x[1]), -int(x[2])))
    if not cov:
        print("no problem schema in the dictionaries (declare `X | is a part of | <problem>` in an extension)")
    else:
        probs = {}
        for p_, pn, c, cn, st, via in cov:
            probs.setdefault(pn, []).append((cn, st, via))
        for pn, items in probs.items():
            done = sum(1 for _, st, _ in items if st == "addressed")
            print(f"**{pn}** — {done}/{len(items)} components addressed by the document's own concepts\n")
            print("| component | status | via |\n|---|---|---|")
            for cn, st, via in sorted(items, key=lambda x: ("addressed", "mentioned", "absent").index(x[1])):
                print(f"| {cn} | {st} | {via} |")
            print()
        print(f"Novel concepts (defined here, unknown outside the document's own theory): {ts.get('novel concepts', '?')}. Hubs — novel concepts by components addressed (at distance 1):\n")
        for m, n, d1 in hubs[:8]:
            print(f"- {m}: {n} ({d1})")

    section("Subject views (subject stratum)")
    ss = rows("subject_stat")
    if not ss:
        print("no subject profiles loaded (add ext/subject/profiles.txt or a document with subject rows)")
    else:
        subs = sorted({s_ for s_, _, _ in ss})
        keys = ["facts visible", "facts seen under a guise", "facts invisible", "concepts unrecognizable", "referents seen as", "facts indexed to it", "perspectival differences"]
        vals = {(s_, k): n for s_, k, n in ss}
        print("| | " + " | ".join(subs) + " |\n|---|" + "---:|" * len(subs))
        for k in keys:
            print(f"| {k} | " + " | ".join(vals.get((s_, k), "0") for s_ in subs) + " |")
        print()
        unrec = rows("unrecognizable")
        by = collections.defaultdict(set)
        for x, s_, d, need, has in unrec:
            by[s_].add(f"{x} (needs {d} {need}, has {has})")
        for s_ in subs:
            if by[s_]:
                print(f"**Unrecognizable for {s_}:** " + "; ".join(sorted(by[s_])[:12]) + ("…" if len(by[s_]) > 12 else ""))
        vw = [r for r in rows("view") if r[2] == "as"]
        if vw:
            byv = collections.defaultdict(list)
            for x, s_, st, y in vw:
                byv[s_].append(f"{x} → {y}")
            for s_ in subs:
                if byv[s_]:
                    print(f"**Seen as, for {s_}:** " + "; ".join(sorted(byv[s_])[:10]))
        pd = rows("perspectival_difference")
        if pd:
            print(f"\n**Perspectival differences** ({len(pd)}): first 10\n")
            for f, s1, s2 in pd[:10]:
                print(f"- {show(f)} — holds for {s1}, not for {s2}")

    section("Declared residual (what the encoder refused to encode)")
    dr = sorted(rows("declared_residual"), key=lambda x: -int(x[2]))
    if not dr:
        print("none")
    else:
        print("| category | needed relation | n |\n|---|---|---:|")
        for c, need, n in dr[:40]:
            print(f"| {c} | {need} | {n} |")

    section("Truncated entailment chains (depth budget exhausted)")
    tr = rows("truncated")
    if not tr:
        print("none")
    for a, b, cc in tr[:20]:
        print(f"- {show(a, 50)} ⇒ … ⇒ {show(b, 50)} ⇒ {show(cc, 50)}")

    section("Role tensions (grounded players vs. dictionary role kinds)")
    rt = rows("role_tension")
    print(f"{len(rt)} total; first 20:\n")
    for f, pos, player, exp, got in rt[:20]:
        print(f"- {show(f)}: role {pos} player `{player}` grounded as *{got}*, expected *{exp}*")

    section("Grounded entities (sample)")
    gr = rows("ground")
    print(f"{len(gr)} groundings; first 25:\n")
    for x, u in gr[:25]:
        print(f"- {x} → {u}")

    section("Derived taxonomy (sample)")
    kb = rows("kb")
    der = [r for r in kb if r[4] in ("derived", "dictionary") and ("kind of" in r[1] or "classified" in r[1] or "specializ" in r[1])]
    print(f"{len(der)} derived classification/specialization facts; first 30:\n")
    for l, rel, r_, lv, _ in der[:30]:
        print(f"- {l} —{rel}→ {r_} (level {lv})")

    section("Longest entailment chains")
    eb = sorted(rows("entails_best"), key=lambda x: -int(x[3]))[:10]
    for a, b, lv, d in eb:
        print(f"- depth {d}, level {lv}: {show(a, 60)} ⇒ {show(b, 60)}")

    section("Cross-table entities (sample)")
    es = sorted(rows("entity_span"), key=lambda x: -int(x[1]))[:20]
    for x, n in es:
        print(f"- {x}: {n} tables")
    return _buf.getvalue()


if __name__ == "__main__":
    sys.stdout.write(render(sys.argv[1], sys.argv[2]))
