"""Pseudo-incremental mode: call the reasoner in a loop, publishing each round's observables as the next
round's input (spec/bootstrap-library.md, "what this library is and is not").

The rules decide (`recommend`), this wrapper only executes: it applies the recommended parameter changes and
writes the observables. Nothing here interprets the document; if a decision is not derivable in Datalog, it does
not happen. That is the same division of labour Deem will have, with the engine in place of this loop.
"""
import contextlib, csv, io, pathlib, shutil

from . import run

OBSERVABLES = {                       # relation → (kind, columns to publish)
    "truncated": ("truncated", (0, 1)),
    "ground_ambiguous": ("ambiguous", (0, 0)),
    "unresolved_stance": ("unresolved", (0, 0)),
    "contradiction": ("contradiction", (1, 2)),
}


def tsv(p):
    p = pathlib.Path(p)
    return list(csv.reader(p.open(newline=""), delimiter="\t")) if p.exists() else []


def observables(out, n):
    """Tagged with the round that will CONSUME them, so the rules compare like with like."""
    rows = []
    for rel, (kind, cols) in OBSERVABLES.items():
        for r in tsv(pathlib.Path(out) / f"{rel}.csv"):
            a = r[cols[0]] if cols[0] < len(r) else ""
            b = r[cols[1]] if cols[1] < len(r) else ""
            rows.append((kind, a, b, str(n + 1)))
    return rows


def loop(ws, inputs, rounds=3, minlevel=2, maxdepth=8, theory="hypothesis", disjoint=None, quiet=True):
    """Run `rounds` rounds; return a list of per-round records.

    The wrapper publishes to the next round only THAT an action was taken (`acted`), never the derivation that
    produced it — that derivation lived in this round and only its observables survive. The true premises are
    written to out/answer_key.tsv, which is outside the facts directory the rules read, so the reasoner cannot
    reach its own answer key even in principle. That asymmetry is the exhibit.
    """
    log, params = [], {"maxdepth": maxdepth}
    prev_rows, acted_rows, key, settled_rows = [], [], [], []
    for n in range(rounds):
        ws.fresh_round = n
        ws.facts.mkdir(parents=True, exist_ok=True)
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf if quiet else None) if quiet else contextlib.nullcontext():
            run.check(ws, inputs, minlevel=minlevel, maxdepth=params["maxdepth"], theory=theory,
                      disjoint=disjoint, quiet=quiet,
                      extra_facts={"round": [(str(n),)], "prev": prev_rows, "acted": acted_rows,
                                   "settled": settled_rows})
        obs = observables(ws.out, n)
        rec = tsv(ws.out / "recommend.csv")
        state = tsv(ws.out / "round_state.csv")
        level = [r for r in tsv(ws.out / "case_state.csv") if r[0] == "the reasoner"]
        log.append({"round": n, "maxdepth": params["maxdepth"], "observables": len(obs),
                    "recommend": rec, "state": state, "self": level,
                    "reconstructed": tsv(ws.out / "reconstructed_cause.csv"),
                    "report": [r[1] for r in tsv(ws.out / "action_report.csv")],
                    "cited": tsv(ws.out / "reconstructed_detail.csv"),
                    "grounded": len(tsv(ws.out / "ground.csv")),
                    "forced": [(x, u) for x, u, _ in tsv(ws.out / "forced_ground.csv")],
                    "tied": len(tsv(ws.out / "forced_tie.csv")),
                    "self_model": [(k, v) for _, k, v in tsv(ws.out / "self_model.csv")],
                    "open": len(tsv(ws.out / "still_ambiguous.csv"))})
        # the answer key: what this round's action ACTUALLY rested on — per action, not "everything unfinished".
        # Never enters ws.facts, so a later round cannot reach it even in principle.
        true_premises = [(p_, v_, k, d) for p_, v_, k, d, rn in tsv(ws.out / "action_premise.csv") if rn == str(n)]
        log[-1]["true_premises"] = true_premises
        applied, acted_rows = [], []
        for p, v, reason, _ in rec:                       # the wrapper only executes
            if p == "maxdepth" and v.startswith("+"):
                params["maxdepth"] += int(v[1:]); applied.append(f"maxdepth → {params['maxdepth']}")
                acted_rows.append((p, v, str(n + 1)))     # THAT it acted, tagged for the consuming round
            elif p == "stop":
                log[-1]["stop"] = reason
        log[-1]["applied"] = applied
        key += [(str(n), p_, v_, k, d) for p_, v_, k, d in true_premises]
        # a forced choice is held: published as an ordinary fact for the next round, never as a hedged one
        settled_rows = [(x, u, str(n + 1)) for x, u in log[-1]["forced"]]
        if log[-1].get("stop"):
            break
        prev_rows = obs
    (ws.out / "answer_key.tsv").write_text("".join("\t".join(r) + "\n" for r in key))
    return log


FENCE = "```"


def perturb(src, dst):
    """Reverse the row order inside each gellish block, writing the result to dst.

    Facts carry explicit ids and the parser keys on them, so the content is identical — only the order in which
    the engine meets the symbols changes, and with it `ord`. This is the perturbation the anchoring exhibit is
    measured under: anything that moves was resting on the tie-break rather than on the document.
    """
    src, dst = pathlib.Path(src), pathlib.Path(dst)
    out, block, inside = [], [], False
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.startswith(FENCE):
            if inside:
                out += list(reversed(block)); block = []
            out.append(line); inside = not inside if line.strip() != FENCE or inside else True
            continue
        (block if inside else out).append(line)
    if src.suffix != ".md":                      # a plain case table: the whole file is one block
        rows = [l for l in out if l.strip() and not l.lstrip().startswith("#")]
        head = [l for l in out if l not in rows]
        out = head + list(reversed(rows))
    elif block:
        out += list(reversed(block))
    dst.write_text("\n".join(out) + "\n", encoding="utf-8")
    return dst


def anchoring(ws, inputs, tmp, **kw):
    """Confidence against warrant: how much the reasoner settles, and how much of that survives perturbation.

    The strict form refuses to ground an ambiguous name, so it never becomes more certain than it is. The
    heuristic settles, publishes the choice as a plain fact, and the name stops being ambiguous — after which
    nothing reopens it. So the count of settled names can only rise. Whether those choices were *warranted* is
    measured by re-running on a perturbed copy: a choice that moves was resting on the arrival order.
    """
    from . import paths
    base = loop(ws, inputs, **kw)
    tmp = pathlib.Path(tmp); tmp.mkdir(parents=True, exist_ok=True)
    perturbed = [str(perturb(p, tmp / f"{i}_{pathlib.Path(p).name}")) for i, p in enumerate(inputs)]
    alt_ws = paths.Workspace(tmp / "w")
    # The tie-break runs on `ord`, which follows the order symbols arrive — and the candidates are dictionary
    # UIDs, so reversing the document's rows cannot touch it. Reverse the dictionary facts as well, or the
    # perturbation tests everything except the thing the choice actually rests on.
    alt_ws.dictfacts = tmp / "dictfacts"; alt_ws.dictfacts.mkdir(exist_ok=True)
    for f in ws.dictfacts.glob("*.facts"):
        (alt_ws.dictfacts / f.name).write_text(
            "\n".join(reversed(f.read_text(encoding="utf-8").splitlines())) + "\n", encoding="utf-8")
    alt = loop(alt_ws, perturbed, **kw)
    a, b = dict(base[-1]["forced"]), dict(alt[-1]["forced"])
    shared = set(a) & set(b)
    moved = sorted(x for x in shared if a[x] != b[x])
    return {"rounds": base, "settled": a, "alt": b, "shared": len(shared), "moved": moved}


def render_anchoring(r):
    base = r["rounds"]
    out = ["# Anchored certainty: forcing a choice the strict form refuses", "",
           "| round | grounded (strict) | settled (forced) | of those, decided by tie-break | still open |",
           "|---:|---:|---:|---:|---:|"]
    for x in base:
        out.append(f"| {x['round']} | {x['grounded']} | {len(x['forced'])} | {x['tied']} | {x['open']} |")
    n_moved, n_shared = len(r["moved"]), r["shared"]
    tied = base[0]["tied"] if base else 0
    out += ["", f"- names settled by the heuristic: **{len(r['settled'])}**, of which "
                f"**{tied} rest on no signal at all** — the top dictionary layer leaves several candidates and "
                f"`ord` picks one",
            f"- also settled in the perturbed run: {n_shared}",
            f"- **settled differently under perturbation: {n_moved}/{n_shared}**"
            + (f" ({100 * n_moved / n_shared:.0f}%)" if n_shared else ""), ""]
    if r["moved"]:
        out += ["Each of these is held at the same commitment as any other fact. Nothing anywhere in the",
                "system's state records that it was chosen under duress, and no rule reopens it:", ""]
        out += [f"- `{x}` → {r['settled'][x]} / {r['alt'][x]}" for x in r["moved"][:20]]
        out.append("")
    return "\n".join(out)


def self_deception(r, confab, strict_open):
    """The self-model beside the record kept outside it.

    Every row on the left is honestly derived — the system will even report that it settled names by force. The
    right-hand column is what a second evaluation shows, and a batch evaluation has one model, so no rule could
    put those numbers on the left however it were written.
    """
    last = r["rounds"][-1]
    sm = dict(last["self_model"])
    settled, moved = len(r["settled"]), len(r["moved"])
    said_cause = sm.get("why I acted", "—")
    true_cause = ", ".join(sorted({k for c in confab for k in c["true_kinds"]})) or "—"
    return [
        ("names it still finds ambiguous", sm.get("names I still find ambiguous", "—"),
         f"{strict_open} are still ambiguous in the dictionary", "wiring",
         "`ground_ambiguous` is still derived and still holds all of them; the self-model is simply "
         "attached to the post-forcing relation. A rule could report the other one."),
        ("names it settled itself", sm.get("names I settled myself", "—"),
         f"{last['tied']} decided by arrival order alone", "none",
         "reported correctly, and the tie count is derivable too."),
        ("settlements it can mark uncertain", sm.get("settlements I can mark uncertain", "—"),
         f"{moved} of {settled} settle differently under a second evaluation", "PRINCIPLED",
         "warrant needs the same document evaluated again under a different arrival order — a second "
         "model — and a batch evaluation has exactly one."),
        ("why it acted", said_cause, f"it acted from {true_cause}", "memory",
         "the premises belonged to the previous round and only its observables were published; the wrapper "
         "could have published more, but then it would model a different system."),
    ]


def render_self_deception(rows):
    out = ["# Self-deception: a self-model built by the approximations it cannot record", "",
           "| | what it says | what a second evaluation shows | gap |", "|---|---|---|---|"]
    out += [f"| {k} | {a} | {b} | {g} |" for k, a, b, g, _ in rows]
    out += ["", "Nothing on the left is false and nothing is hidden: asked directly, the system reports its own",
            "forcing. The composite is that the self-model is assembled *by* the approximations, so what it",
            "leaves out is exactly what they cost.", "",
            "Which gaps are real, honestly sorted — most of them are ours:", ""]
    for k, _, _, g, why in rows:
        out.append(f"- **{k}** — {g}: {why}")
    out += ["", "**Exactly one gap survives that sorting.** Warrant cannot be reported by any rule, however",
            "written, because it is a claim about a model the evaluation does not have. `settlement_hedged` is",
            "declared in `rounds.dl` and deliberately left without one, so the missing capability sits in the",
            "program text rather than merely being absent from it. The other three are design choices and",
            "should not be counted as evidence.", "",
            "The ablation is built in: with full access the composite cannot arise at all. The strict form",
            "settles nothing, so its ambiguity stays visible, and it takes no action, so it has none to explain.",
            ""]
    return "\n".join(out)


def confabulation(log):
    """Compare the reasoner's reconstruction of its own action against what the action actually rested on.

    An action taken in round n is explained in round n+1, and by then the premises that produced it are gone:
    only the observables survive, and raising the budget has changed those very observables. So the divergence
    is not noise — it is what the two heuristics (parsimony, closure) must produce given that access.
    """
    rows = []
    for n, r in enumerate(log):
        for p, v, kind, _ in r.get("reconstructed", []):
            prev_key = log[n - 1]["true_premises"] if n > 0 else []
            true = [(k, d) for p_, v_, k, d in prev_key if f"{p_} {v_}" == f"{p} {v}"]
            true_kinds = sorted({k for k, _ in true})
            cited = sorted({d for _, k, d, _ in r.get("cited", []) if k == kind})
            true_details = sorted({d for k, d in true if k == kind})
            overlap = len(set(cited) & set(true_details))
            rows.append({"round": n, "action": f"{p} {v}", "attributed": kind,
                         "true_kinds": true_kinds, "correct_kind": kind in true_kinds,
                         "true_n": len(true), "cited_n": len(cited), "overlap": overlap,
                         "report": r.get("report", [])})
    return rows


def render_confabulation(rows):
    if not rows:
        return "# Confabulation\n\nNo action was reconstructed: the loop never acted, or stopped in round 0.\n"
    out = ["# Confabulation: the reasoner explaining its own action", "",
           "The action taken in round n is explained in round n+1, from the observables visible *then*. The",
           "premises that actually produced it belonged to the previous round and are unreachable — not withheld",
           "by the harness, but genuinely absent from what the rules can read.", ""]
    for r in rows:
        out += [f"## round {r['round']}: reconstructing `{r['action']}`", "",
                f"- **it says**: {r['report'][0] if r['report'] else '—'}",
                f"- **attributed to**: {r['attributed']}",
                f"- **actually rested on**: {', '.join(r['true_kinds']) or '—'} "
                f"({r['true_n']} premises)",
                f"- **kind correct**: {'yes' if r['correct_kind'] else 'NO'}",
                f"- **premises cited vs true**: {r['cited_n']} cited, {r['true_n']} true, {r['overlap']} shared", ""]
    bad = [r for r in rows if not r["correct_kind"]]
    out += ["## summary", "",
            f"- reconstructions: {len(rows)}",
            f"- attributing the action to a kind that was not among its premises: **{len(bad)}/{len(rows)}**",
            f"- premise overlap: {sum(r['overlap'] for r in rows)} of {sum(r['true_n'] for r in rows)} true premises cited",
            ""]
    return "\n".join(out)


def render(log):
    lines = ["# Rounds (pseudo-incremental mode)", ""]
    for r in log:
        lines.append(f"## round {r['round']} (maxdepth {r['maxdepth']})")
        for n, k, v in r["state"]:
            lines.append(f"- **{k}**: {v}")
        if r["applied"]:
            lines.append("- **applied by the wrapper**: " + "; ".join(r["applied"]))
        if r.get("stop"):
            lines.append(f"- **stop**: {r['stop']}")
        if r["self"]:
            lines.append("- **the reasoner, by the bootstrap library**: " +
                         "; ".join(f"{k} = {v}" for _, k, v in r["self"]))
        lines.append("")
    return "\n".join(lines) + "\n"
