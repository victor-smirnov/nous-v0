"""nous — command line.

  nous gellish build-dict [--fetch]                 dictionary + extensions → data/dictfacts
  nous gellish check TABLE... [--theory ...]        parse → Soufflé → report (stdout), outputs in work/out
  nous gellish ask "<node>"                         everything known about a node (after check)
  nous gellish why <relation> [filters...]          proof trees (after check)
  nous gellish report                               re-render the last report
  nous gellish phrases [-o spec/phrases.md] [--all]  relation-phrase reference for the encoder
  nous gellish rounds INPUT... [--rounds 3]            pseudo-incremental mode: the rules decide, the loop executes
  nous gellish state CASE.txt [--theory ...]           the bootstrap library: case description → Observer state
  nous gellish summarize DOC.md [--budget 80] [-o SUMMARY.md] [--theory ...]   thesis stratum → selected rows (gellish-summary)
  nous gellish enrich DOC.md [-o OUT.md] [--depth 1] [--no-defs] [--gellish-facts] [--theory ...]   derived rows → gellish-derived blocks
  nous gellish diff A.md B.md [--theory ...]        semantic diff of two closures
  nous gellish extract DOC.md -o DIR                fenced tables → DIR/<section>.txt
  nous gellish inject DOC.md TABLE... [-o OUT.md]   tables → fenced blocks in the document
"""
import argparse, sys

from .gellish import paths


def main(argv=None):
    ap = argparse.ArgumentParser(prog="nous", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gellish", help="Gellish ontological reasoner").add_subparsers(dest="gcmd", required=True)

    p = g.add_parser("build-dict"); p.add_argument("--fetch", action="store_true", help="download the gellish.net release first")
    p = g.add_parser("check")
    p.add_argument("tables", nargs="+")
    p.add_argument("--minlevel", type=int, default=2, help="lowest commitment admitted into inference (4 asserted, 3 hedged, 2 conjectured)")
    p.add_argument("--maxdepth", type=int, default=8, help="entailment chain budget")
    p.add_argument("--theory", choices=["off", "hypothesis", "doctrine"], default="hypothesis", help="how the Synthea-bootstrap collection enters")
    p.add_argument("--disjoint", help="TSV of disjoint kind pairs")
    p.add_argument("--work", help="working directory (default repo/work)")
    p.add_argument("-o", "--report", help="write the report here instead of stdout")
    p = g.add_parser("ask"); p.add_argument("query"); p.add_argument("--work")
    p = g.add_parser("why"); p.add_argument("target", nargs="+", help="relation [filters...] or a raw atom"); p.add_argument("--work")
    p = g.add_parser("report"); p.add_argument("--work")
    p = g.add_parser("rounds"); p.add_argument("inputs", nargs="+"); p.add_argument("--rounds", type=int, default=3)
    p.add_argument("--maxdepth", type=int, default=8); p.add_argument("--minlevel", type=int, default=2)
    p.add_argument("--theory", choices=["off", "hypothesis", "doctrine"], default="hypothesis"); p.add_argument("--work")
    p = g.add_parser("state"); p.add_argument("cases", nargs="+"); p.add_argument("--work")
    p.add_argument("--theory", choices=["off", "hypothesis", "doctrine"], default="hypothesis")
    p = g.add_parser("summarize"); p.add_argument("doc"); p.add_argument("-o", "--out"); p.add_argument("--budget", type=int, default=80)
    p.add_argument("--theory", choices=["off", "hypothesis", "doctrine"], default="hypothesis"); p.add_argument("--work")
    p = g.add_parser("enrich"); p.add_argument("doc"); p.add_argument("-o", "--out"); p.add_argument("--depth", type=int, default=1)
    p.add_argument("--no-defs", action="store_true"); p.add_argument("--no-derived", action="store_true"); p.add_argument("--gellish-facts", action="store_true")
    p.add_argument("--theory", choices=["off", "hypothesis", "doctrine"], default="hypothesis"); p.add_argument("--work")
    p = g.add_parser("diff"); p.add_argument("a"); p.add_argument("b"); p.add_argument("--stated-only", action="store_true")
    p.add_argument("--theory", choices=["off", "hypothesis", "doctrine"], default="hypothesis"); p.add_argument("--work")
    p = g.add_parser("phrases"); p.add_argument("-o", "--out"); p.add_argument("--all", action="store_true")
    p = g.add_parser("extract"); p.add_argument("doc"); p.add_argument("-o", "--out", required=True)
    p = g.add_parser("inject"); p.add_argument("doc"); p.add_argument("tables", nargs="+"); p.add_argument("-o", "--out")
    a = ap.parse_args(argv)

    ws = paths.Workspace(getattr(a, "work", None))
    if a.gcmd == "build-dict":
        from .gellish import run
        run.build_dict(ws, fetch=a.fetch)
    elif a.gcmd == "check":
        from .gellish import run
        text = run.check(ws, a.tables, a.minlevel, a.maxdepth, a.theory, a.disjoint)
        if a.report:
            open(a.report, "w").write(text)
        else:
            sys.stdout.write(text)
    elif a.gcmd == "ask":
        from .gellish import ask
        ask.main(a.query, ws.out)
    elif a.gcmd == "why":
        from .gellish import why
        why.main(a.target, ws)
    elif a.gcmd == "report":
        from .gellish import report
        sys.stdout.write(report.render(ws.out, ws.facts))
    elif a.gcmd == "rounds":
        from .gellish import rounds
        paths.require_souffle(); ws.require_dictfacts()
        sys.stdout.write(rounds.render(rounds.loop(ws, a.inputs, a.rounds, a.minlevel, a.maxdepth, a.theory)))
    elif a.gcmd == "state":
        from .gellish import run, state
        run.check(ws, a.cases, theory=a.theory, quiet=True)
        sys.stdout.write(state.render(ws.out))
    elif a.gcmd == "summarize":
        from .gellish import run, summarize
        run.check(ws, [a.doc], theory=a.theory, quiet=True)
        text = summarize.main(ws.out, ws.facts, a.budget, a.out)
        if not a.out:
            sys.stdout.write(text)
    elif a.gcmd == "enrich":
        from .gellish import enrich, run
        run.check(ws, [a.doc], theory=a.theory, quiet=True)
        placed = enrich.plan(a.doc, ws.out, a.depth, not a.no_defs, not a.no_derived, a.gellish_facts)
        out, n = enrich.write(a.doc, placed, a.out)
        print(f"{n} derived rows → {out}", file=sys.stderr)
    elif a.gcmd == "diff":
        from .gellish import diff, run
        wa, wb = paths.Workspace(ws.work / "diff-a"), paths.Workspace(ws.work / "diff-b")
        run.check(wa, [a.a], theory=a.theory, quiet=True); run.check(wb, [a.b], theory=a.theory, quiet=True)
        sys.stdout.write(diff.render(wa.out, wb.out, a.a, a.b, a.stated_only))
    elif a.gcmd == "phrases":
        from .gellish import phrases
        text = phrases.main(a.out, a.all)
        if not a.out:
            sys.stdout.write(text)
    elif a.gcmd == "extract":
        from .gellish import hybrid
        for f in hybrid.extract(a.doc, a.out):
            print(f)
    elif a.gcmd == "inject":
        from .gellish import hybrid
        print(hybrid.inject(a.doc, a.tables, a.out))


if __name__ == "__main__":
    main()
