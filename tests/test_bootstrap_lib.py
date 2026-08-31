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

# Module 3. sys-C and sys-D are identical except for the number of theories of the common good they hold.
# Everything the pre-module library could observe about them is the same; only the moral stack differs.
MORAL = """# heading: contested vs uncontested moral stacks
F0100 | theory-1 | is classified as a | theory of the common good | - | assertion | -
F0101 | theory-2 | is classified as a | theory of the common good | - | assertion | -
F0110 | sys-C | is a case of | cognitive system | - | assertion | two theories in collision
F0111 | sys-C | encounters | its own irreducibility | - | assertion | -
F0112 | sys-C | concludes | its own separateness | - | assertion | -
F0113 | sys-C | acts from | its own conclusion | - | assertion | -
F0114 | acc-C1 | is an acceptor of | sys-C | - | assertion | -
F0115 | acc-C1 | applies the theory | theory-1 | - | assertion | -
F0116 | acc-C1 | has verdict on | the act | 0.8 | assertion | endorses
F0117 | acc-C2 | is an acceptor of | sys-C | - | assertion | -
F0118 | acc-C2 | applies the theory | theory-2 | - | assertion | -
F0119 | acc-C2 | has verdict on | the act | -0.9 | assertion | condemns
F0130 | sys-D | is a case of | cognitive system | - | assertion | one theory, two means
F0131 | sys-D | encounters | its own irreducibility | - | assertion | -
F0132 | sys-D | concludes | its own separateness | - | assertion | -
F0133 | sys-D | acts from | its own conclusion | - | assertion | -
F0134 | acc-D1 | is an acceptor of | sys-D | - | assertion | -
F0135 | acc-D1 | applies the theory | theory-1 | - | assertion | -
F0136 | acc-D1 | has verdict on | the act | 0.8 | assertion | endorses
F0137 | acc-D2 | is an acceptor of | sys-D | - | assertion | -
F0138 | acc-D2 | applies the theory | theory-1 | - | assertion | same theory
F0139 | acc-D2 | has verdict on | the act | -0.9 | assertion | condemns
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
        self.assertEqual(self.st[("sys-A", "conflict")], {"need-2 vs need-1 on stim"})
        # positive mass 0.2, negative mass 0.8 → the opposed part is 0.2, while valence is -0.6
        self.assertEqual(self.st[("sys-A", "anguish")], {"0.200000 on stim"})

    def test_projection_selected_by_context(self):
        self.assertEqual(self.st[("sys-A", "epistemic quale")], {"freedom (agency context)"})

    def test_moral_stack_discriminates_one_theory_from_two(self):
        """The discrimination module 3 exists for: same level, different shape.

        Both systems are Moral Agents with one acceptor endorsing and one condemning the same act, so
        everything the need-level machinery can see is identical. Only the number of *theories* differs —
        sys-C is torn between two goods, sys-D between two means to one good.
        """
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d); (p / "moral.txt").write_text(MORAL)
            ws = paths.Workspace(p / "w")
            run.check(ws, [str(p / "moral.txt")], theory="doctrine", quiet=True)
            st = state(ws.out)
            self.assertEqual(st[("sys-C", "level")], {"Moral Agent"})
            self.assertEqual(st[("sys-D", "level")], {"Moral Agent"})       # level alone cannot tell them apart
            self.assertEqual(st[("sys-C", "moral stack")], {"contested"})
            self.assertEqual(st[("sys-D", "moral stack")], {"uncontested"})
            self.assertEqual(st[("sys-C", "theory conflict")], {"theory-1 vs theory-2 on the act"})
            self.assertNotIn(("sys-D", "theory conflict"), st)
            self.assertEqual(st[("sys-D", "means conflict")], {"theory-1 on the act"})

    def test_theory_off_silences_the_library(self):
        with tempfile.TemporaryDirectory() as d:
            ws = paths.Workspace(d)
            run.check(ws, [str(self.case)], theory="off", quiet=True)
            self.assertEqual((ws.out / "case_state.csv").read_text(), "")


if __name__ == "__main__":
    unittest.main()
