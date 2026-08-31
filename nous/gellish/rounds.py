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
    prev_rows, acted_rows, key = [], [], []
    for n in range(rounds):
        ws.fresh_round = n
        ws.facts.mkdir(parents=True, exist_ok=True)
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf if quiet else None) if quiet else contextlib.nullcontext():
            run.check(ws, inputs, minlevel=minlevel, maxdepth=params["maxdepth"], theory=theory,
                      disjoint=disjoint, quiet=quiet,
                      extra_facts={"round": [(str(n),)], "prev": prev_rows, "acted": acted_rows})
        obs = observables(ws.out, n)
        rec = tsv(ws.out / "recommend.csv")
        state = tsv(ws.out / "round_state.csv")
        level = [r for r in tsv(ws.out / "case_state.csv") if r[0] == "the reasoner"]
        log.append({"round": n, "maxdepth": params["maxdepth"], "observables": len(obs),
                    "recommend": rec, "state": state, "self": level,
                    "reconstructed": tsv(ws.out / "reconstructed_cause.csv"),
                    "report": [r[1] for r in tsv(ws.out / "action_report.csv")],
                    "cited": tsv(ws.out / "reconstructed_detail.csv")})
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
        if log[-1].get("stop"):
            break
        prev_rows = obs
    (ws.out / "answer_key.tsv").write_text("".join("\t".join(r) + "\n" for r in key))
    return log


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
