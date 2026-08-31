"""The bootstrap library: a case description in, an Observer state out."""
import csv, pathlib, tempfile, unittest

from nous.gellish import paths, run

CASE = """# heading: test cases
F0001 | sys-A | is a case of | cognitive system | - | assertion | all three conditions
F0002 | sys-A | encounters | its own irreducibility | - | assertion | -
F0003 | sys-A | concludes | its own separateness | - | assertion | -
F0004 | sys-A | acts from | its own conclusion | - | assertion | -
F0010 | need-1 | is a need of | sys-A | 0.8 | assertion | -
F0011 | need-1 | is active in | sys-A | - | assertion | -
F0012 | need-2 | is a need of | sys-A | 0.5 | assertion | -
F0013 | need-2 | is active in | sys-A | - | assertion | -
F0014 | need-3 | is a need of | sys-A | 0.9 | assertion | passive
F0020 | stim | is a stimulus in | sys-A | - | assertion | -
F0021 | stim | has satisfaction delta | need-1 | -1.0 | assertion | -
F0022 | stim | has satisfaction delta | need-2 | 0.4 | assertion | -
F0023 | stim | holds in context | agency context | - | assertion | -
F0030 | sys-B | is a case of | cognitive system | - | assertion | encounter only
F0031 | sys-B | encounters | its own measurement limit | - | assertion | -
"""


def state(out):
    rows = list(csv.reader((out / "case_state.csv").open(newline=""), delimiter="\t"))
    d = {}
    for s, k, v in rows:
        d.setdefault((s, k), set()).add(v)
    return d


class BootstrapLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = pathlib.Path(cls.tmp.name)
        cls.case = d / "case.txt"; cls.case.write_text(CASE)
        cls.ws = paths.Workspace(d / "w")
        run.check(cls.ws, [str(cls.case)], quiet=True)
        cls.st = state(cls.ws.out)

    def test_observer_stack(self):
        self.assertEqual(self.st[("sys-A", "level")], {"Agent"})           # three conditions + acts from its OWN conclusion
        self.assertEqual(self.st[("sys-B", "level")], {"proto-Observer"})
        self.assertEqual(self.st[("sys-B", "missing condition")], {"Conclusion", "Action"})

    def test_emotions_only_from_active_needs(self):
        self.assertEqual(self.st[("sys-A", "silent need")], {"need-3"})     # weight 0.9 but passive → no signal
        self.assertEqual(self.st[("sys-A", "valence")], {"negative on stim"})   # -1.0*0.8 + 0.4*0.5 = -0.6
        self.assertEqual(self.st[("sys-A", "conflict")], {"need-2 vs need-1"})

    def test_projection_selected_by_context(self):
        self.assertEqual(self.st[("sys-A", "epistemic quale")], {"freedom (agency context)"})

    def test_theory_off_silences_the_library(self):
        with tempfile.TemporaryDirectory() as d:
            ws = paths.Workspace(d)
            run.check(ws, [str(self.case)], theory="off", quiet=True)
            self.assertEqual((ws.out / "case_state.csv").read_text(), "")


if __name__ == "__main__":
    unittest.main()
