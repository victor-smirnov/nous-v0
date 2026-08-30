"""The thesis stratum and summarize run on the v3 fixture section and select stated rows only."""
import pathlib, tempfile, unittest

from nous.gellish import paths, run, summarize

DOC = pathlib.Path(__file__).resolve().parent / "fixtures" / "S2.2.hybrid.md"


class Summarize(unittest.TestCase):
    def test_runs_and_selects_stated_rows(self):
        with tempfile.TemporaryDirectory() as d:
            ws = paths.Workspace(d)
            run.check(ws, [str(DOC)], quiet=True)
            header, hubs, order, why, facts = summarize.build(ws.out, ws.facts, budget=20)
            self.assertTrue(header, "problem schema present")
            self.assertTrue(any(st == "addressed" for _, _, st, _ in header))
            self.assertLessEqual(len(order), 20)
            for f in order:
                self.assertIn(f, facts)
            text = summarize.render(header, hubs, order, why, facts)
            self.assertIn("```gellish-summary", text)


if __name__ == "__main__":
    unittest.main()
