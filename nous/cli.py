"""nous — command line.

  nous gellish build-dict [--fetch]                 dictionary + extensions → data/dictfacts
  nous gellish check TABLE... [--theory ...]        parse → Soufflé → report (stdout), outputs in work/out
  nous gellish ask "<node>"                         everything known about a node (after check)
  nous gellish why <relation> [filters...]          proof trees (after check)
  nous gellish report                               re-render the last report
  nous gellish phrases [-o spec/phrases.md] [--all]  relation-phrase reference for the encoder
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
