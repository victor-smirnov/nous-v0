"""Entity alignment across two independently encoded documents."""
import pathlib, tempfile, unittest

from nous.gellish import align

A = """# heading: doc A
F0001 | apparent causal break | is a projection of | computational residual | - | assertion | -
F0002 | sender internal state | is encoded as | cognitive code | - | assertion | -
F0003 | an external observer | reconstructs | sender internal state | - | assertion | -
F0004 | large language model | lacks | inner speech | - | assertion | -
"""
B = """# heading: doc B
F0001 | apparent causal break | is a projection of | computational residual | - | assertion | -
F0002 | internal state of sender | is encoded as | cognitive code | - | assertion | -
F0003 | omniscient external observer | reconstructs | internal state of sender | - | assertion | -
F0004 | large language model | lacks | limbic inertia | - | assertion | -
"""


class Align(unittest.TestCase):
    def test_passes(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
            d = pathlib.Path(d)
            a = d / "a.txt"; a.write_text(A)
            b = d / "b.txt"; b.write_text(B)
            res = align.align(str(a), str(b), t1, t2)
            acc = {(x, y): (s, m) for x, y, s, m in res["accepted"]}
            band = {(x, y) for x, y, _, _ in res["uncertain"]}
            self.assertIn(("apparent causal break", "apparent causal break"), acc)      # identical
            self.assertIn(("cognitive code", "cognitive code"), acc)
            # word-order variant is caught by lexical or structural, one way or the other
            self.assertTrue(("sender internal state", "internal state of sender") in acc
                            or ("sender internal state", "internal state of sender") in band)
            # a restricting qualifier must NOT be auto-accepted as identity
            self.assertNotIn(("an external observer", "omniscient external observer"), acc)
            # one-to-one: no entity of A is aligned twice
            lefts = [x for x, _, _, _ in res["accepted"]]
            self.assertEqual(len(lefts), len(set(lefts)))


if __name__ == "__main__":
    unittest.main()
