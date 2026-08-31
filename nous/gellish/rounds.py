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
    """Run `rounds` rounds; return a list of per-round records."""
    log, params = [], {"maxdepth": maxdepth}
    prev_rows = []
    for n in range(rounds):
        ws.fresh_round = n
        ws.facts.mkdir(parents=True, exist_ok=True)
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf if quiet else None) if quiet else contextlib.nullcontext():
            run.check(ws, inputs, minlevel=minlevel, maxdepth=params["maxdepth"], theory=theory,
                      disjoint=disjoint, quiet=quiet, extra_facts={"round": [(str(n),)], "prev": prev_rows})
        obs = observables(ws.out, n)
        rec = tsv(ws.out / "recommend.csv")
        state = tsv(ws.out / "round_state.csv")
        level = [r for r in tsv(ws.out / "case_state.csv") if r[0] == "the reasoner"]
        log.append({"round": n, "maxdepth": params["maxdepth"], "observables": len(obs),
                    "recommend": rec, "state": state, "self": level})
        applied = []
        for p, v, reason, _ in rec:                       # the wrapper only executes
            if p == "maxdepth" and v.startswith("+"):
                params["maxdepth"] += int(v[1:]); applied.append(f"maxdepth → {params['maxdepth']}")
            elif p == "stop":
                log[-1]["stop"] = reason
        log[-1]["applied"] = applied
        if log[-1].get("stop"):
            break
        prev_rows = obs
    return log


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
