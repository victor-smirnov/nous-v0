"""Golden regression: the article's first encoding must close to the same statistics and the
same contradictions. Run: python3 -m unittest discover tests   (needs data/dictfacts and souffle)."""
import csv, pathlib, tempfile, unittest

from nous.gellish import paths, run

REPO = pathlib.Path(__file__).resolve().parent.parent
TABLES = sorted(str(p) for p in (REPO / "tables" / "article-v1").glob("C0*.txt"))
GOLDEN = pathlib.Path(__file__).parent / "golden"


def tsv(p):
    with open(p, newline="") as f:
        return sorted(tuple(r) for r in csv.reader(f, delimiter="\t"))


class Golden(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.ws = paths.Workspace(cls.tmp.name)
        cls.report = run.check(cls.ws, TABLES, quiet=True)

    def test_stats(self):
        # dictionary-level counts move whenever an extension changes; the golden holds the document-level closure
        doc = lambda rows: [r for r in rows if not r[0].startswith("dictionary ") and r[0] != "theory concepts"]
        self.assertEqual(doc(tsv(self.ws.out / "stat.csv")), doc(tsv(GOLDEN / "stat.csv")))

    def test_contradictions(self):
        self.assertEqual(tsv(self.ws.out / "contradiction.csv"), tsv(GOLDEN / "contradiction.csv"))

    def test_report_mentions_sections(self):
        for s in ("## Stats", "## Contradictions", "## Spec violations", "## Residual relation phrases"):
            self.assertIn(s, self.report)


class Theory(unittest.TestCase):
    def test_theory_off_drops_theory_groundings(self):
        with tempfile.TemporaryDirectory() as d:
            ws = paths.Workspace(d)
            run.check(ws, TABLES, theory="off", quiet=True)
            stats = dict((k, int(v)) for k, v in tsv(ws.out / "stat.csv"))
            self.assertEqual(stats["entities grounded in theory"], 0)
            self.assertEqual(stats["theory level"], 0)


if __name__ == "__main__":
    unittest.main()
