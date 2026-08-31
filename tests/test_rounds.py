"""Pseudo-incremental mode: the rules decide, the loop executes, and the reasoner's own state is derived."""
import pathlib, tempfile, unittest

from nous.gellish import paths, rounds

DOC = """# heading: a chain long enough to truncate at depth 1
F0001 | a | implies | b | - | assertion | -
F0002 | b | implies | c | - | assertion | -
F0003 | c | implies | d | - | assertion | -
F0004 | d | implies | e | - | assertion | -
"""


class Rounds(unittest.TestCase):
    def test_loop_closes_and_halts(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            doc = d / "chain.txt"; doc.write_text(DOC)
            ws = paths.Workspace(d / "w")
            log = rounds.loop(ws, [str(doc)], rounds=6, maxdepth=1)
            self.assertEqual(log[0]["round"], 0)
            self.assertEqual(log[0]["state"], [])                      # round 0 has no previous state to read
            # a later round encounters the truncation, concludes, and acts by raising the budget
            acted = [r for r in log if any(p == "maxdepth" for p, *_ in r["recommend"])]
            self.assertTrue(acted, "the rules must recommend raising the depth budget")
            self.assertGreater(log[-1]["maxdepth"], log[0]["maxdepth"])
            self.assertTrue(any("conclusion" == k for r in log for _, k, _ in r["state"]))
            self.assertTrue(log[-1].get("stop"), "the loop must halt on a derived recommendation")
            # while it can change its own operation the library calls it an Agent
            levels = {v for r in log for _, k, v in r["self"] if k == "level"}
            self.assertIn("Agent", levels)


if __name__ == "__main__":
    unittest.main()
