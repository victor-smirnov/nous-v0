"""The v3-encoded section must stay clean: no spec violations, no role tensions, exactly the one
source contradiction (identity vs projection of causal break / computational residual)."""
import csv, pathlib, tempfile, unittest

from nous.gellish import paths, run

DOC = pathlib.Path(__file__).resolve().parent.parent / "tables" / "article-v3" / "S2.2.hybrid.md"


class V3Section(unittest.TestCase):
    def test_clean(self):
        with tempfile.TemporaryDirectory() as d:
            ws = paths.Workspace(d)
            run.check(ws, [str(DOC)], quiet=True)
            stats = {k: int(v) for k, v in csv.reader((ws.out / "stat.csv").open(newline=""), delimiter="\t")}
            self.assertEqual(stats["violations"], 0)
            self.assertEqual(stats["role tensions"], 0)
            self.assertEqual(stats["facts unresolved"], 0)
            contra = list(csv.reader((ws.out / "contradiction.csv").open(newline=""), delimiter="\t"))
            self.assertEqual(len(contra), 1)
            self.assertEqual(contra[0][0], "disjoint-relations")
            self.assertEqual({contra[0][1], contra[0][2]}, {"causal break", "computational residual"})
            self.assertLessEqual(stats["facts residual"], 7)


if __name__ == "__main__":
    unittest.main()
