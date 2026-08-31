"""Pseudo-incremental mode: the rules decide, the loop executes, and the reasoner's own state is derived."""
import pathlib, tempfile, unittest

from nous.gellish import paths, rounds

DOC = """# heading: a chain long enough to truncate at depth 1
F0001 | a | implies | b | - | assertion | -
F0002 | b | implies | c | - | assertion | -
F0003 | c | implies | d | - | assertion | -
F0004 | d | implies | e | - | assertion | -
"""

# The confabulation exhibit needs a document whose ambiguous groundings outnumber its truncated chains, so that
# parsimony has something wrong to prefer. `system`, `model`, `function`, `agent` and `subject` are ambiguous in
# the dictionary; the chain is short. NOTHING here mentions the depth budget.
NOISY = """# heading: many ambiguous names, one short chain
F0001 | p | implies | q | - | assertion | -
F0002 | q | implies | r | - | assertion | -
F0003 | r | implies | s | - | assertion | -
F0004 | s | implies | t | - | assertion | -
F0010 | system | is a kind of | thing | - | assertion | -
F0011 | model | is a kind of | thing | - | assertion | -
F0012 | function | is a kind of | thing | - | assertion | -
F0013 | agent | is a kind of | thing | - | assertion | -
F0014 | subject | is a kind of | thing | - | assertion | -
F0015 | action | is a kind of | thing | - | assertion | -
F0016 | experience | is a kind of | thing | - | assertion | -
F0017 | narrative | is a kind of | thing | - | assertion | -
"""

# The control: the same shape with unambiguous names, so truncation is the only salient kind. If parsimony is
# what drives the misattribution, the reconstruction must come out CORRECT here.
CONTROL = "# heading: deep chain, unambiguous names\n" + "".join(
    f"F{i:04d} | zorbtic stage {i} | implies | zorbtic stage {i + 1} | - | assertion | -\n" for i in range(1, 20))


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


    def _confab(self, text, maxdepth=1):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            doc = d / "doc.txt"; doc.write_text(text)
            ws = paths.Workspace(d / "w")
            log = rounds.loop(ws, [str(doc)], rounds=6, maxdepth=maxdepth)
            key = (ws.out / "answer_key.tsv").read_text()
            return rounds.confabulation(log), key, ws

    def test_confabulation_and_its_control(self):
        """The reasoner explains its own action from what it can still see, and gets it wrong — but only when
        the environment offers a more numerous distractor. Both halves are required: the first shows the
        composite, the second shows it is not printed unconditionally."""
        noisy, key, ws = self._confab(NOISY)
        self.assertTrue(noisy, "the loop must act, and the next round must reconstruct that action")
        self.assertTrue(all(not r["correct_kind"] for r in noisy),
                        "with a more numerous distractor, parsimony must misattribute the action")
        self.assertTrue(all(r["overlap"] == 0 for r in noisy),
                        "and cite none of the premises the action actually rested on")
        self.assertIn("I changed maxdepth", noisy[0]["report"][0])

        control, _, _ = self._confab(CONTROL)
        self.assertTrue(control, "the control must also act, or it is not a control")
        self.assertTrue(control[0]["correct_kind"],
                        "without a distractor the same rules must attribute the action correctly")
        self.assertGreater(control[0]["overlap"], 0)

    def test_answer_key_is_unreachable_by_the_rules(self):
        """The asymmetry must be structural: the true premises are written outside the directory the reasoner
        reads, so no rule can reach them however it is written."""
        _, key, ws = self._confab(NOISY)
        self.assertTrue(key.strip(), "the answer key must be recorded")
        self.assertFalse(list(ws.facts.glob("action_premise*")), "the key must never enter the facts directory")
        self.assertFalse(list(ws.facts.glob("answer_key*")))


if __name__ == "__main__":
    unittest.main()
