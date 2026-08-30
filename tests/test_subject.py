"""Subject stratum: capacity matrix + access requirements → visible / invisible facts per subject type."""
import csv, pathlib, tempfile, unittest

from nous.gellish import paths, run

REPO = pathlib.Path(__file__).resolve().parent.parent
DOC = REPO / "tests" / "fixtures" / "S2.2.hybrid.md"
PROFILES = REPO / "ext" / "subject" / "profiles.txt"


class Subject(unittest.TestCase):
    def test_visibility_per_subject(self):
        with tempfile.TemporaryDirectory() as d:
            ws = paths.Workspace(d)
            run.check(ws, [str(DOC), str(PROFILES)], quiet=True)
            stats = {(s, k): int(n) for s, k, n in csv.reader((ws.out / "subject_stat.csv").open(newline=""), delimiter="\t")}
            subs = {s for s, _ in stats}
            self.assertEqual(subs, {"Rationalist", "Intuitionist", "Language-model subject"})
            for s in subs:
                self.assertGreater(stats[(s, "facts visible")], 50)
            unrec = list(csv.reader((ws.out / "unrecognizable.csv").open(newline=""), delimiter="\t"))
            # with the placeholder matrix the Intuitionist lacks mechanistic access to HOCP; the Rationalist reaches Beingness through the mechanism
            self.assertTrue(any(x == "higher-order computational phenomenon" and s == "Intuitionist" for x, s, *_ in unrec))
            self.assertFalse(any(x == "Beingness quale" and s == "Rationalist" for x, s, *_ in unrec))


if __name__ == "__main__":
    unittest.main()
