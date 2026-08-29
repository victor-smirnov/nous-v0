"""Enrichment export and semantic diff on a small hybrid document."""
import pathlib, tempfile, unittest

from nous.gellish import diff, enrich, paths, run

DOC = """# A

```gellish S1
F0001 | Moral Agent | is a specialization of | Agent | - | assertion | -
F0002 | Agent | is a specialization of | Observer | - | assertion | -
F0003 | Dennett | is classified as a | philosopher | - | assertion | -
F0004 | Dennett | is identical to | Dennett 1991 | - | assertion | -
```
"""


class EnrichDiff(unittest.TestCase):
    def test_enrich_writes_derived_block(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            doc = d / "doc.md"; doc.write_text(DOC)
            ws = paths.Workspace(d / "w")
            run.check(ws, [str(doc)], quiet=True)
            placed = enrich.plan(doc, ws.out, depth=1)
            rows = placed["S1"]
            triples = {(r[0], r[1], r[2]) for r in rows}
            self.assertIn(("Moral Agent", "is a specialization of", "Observer"), triples)   # transitive closure
            self.assertTrue(any(r[0] == "Dennett" and r[1] == "is asserted by" or r[2] == "Dennett" and "asserted" in r[1] for r in rows)
                            or any("illusionism" in r for r in rows))                       # theory fact via grounding
            self.assertFalse(any(r[2] in ("anything", "concept") for r in rows))            # top-cut
            self.assertFalse(any(r[0] == "Dennett 1991" for r in rows))                     # identity class collapsed
            for r in rows:
                self.assertIn(r[4], ("assertion", "hedged-assertion", "hypothesis", "definition"))
                self.assertRegex(r[5], r"^(derived|theory|field|gellish): ")
            out, n = enrich.write(doc, placed, d / "out.md")
            text = out.read_text()
            self.assertIn("```gellish-derived S1", text)
            self.assertEqual(n, len(rows))
            # idempotent: a second write replaces, not duplicates
            out2, _ = enrich.write(out, placed, d / "out2.md")
            self.assertEqual(out2.read_text().count("```gellish-derived S1"), 1)

    def test_diff_reports_added_and_relevelled(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            a = d / "a.md"; a.write_text(DOC)
            b = d / "b.md"; b.write_text(DOC.replace("F0002 | Agent | is a specialization of | Observer | - | assertion",
                                                     "F0002 | Agent | is a specialization of | Observer | - | hypothesis")
                                         + "\n```gellish S2\nF0001 | Observer | is a specialization of | role | - | assertion | -\n```\n")
            wa, wb = paths.Workspace(d / "wa"), paths.Workspace(d / "wb")
            run.check(wa, [str(a)], quiet=True); run.check(wb, [str(b)], quiet=True)
            text = diff.render(wa.out, wb.out, "a", "b")
            self.assertIn("Observer —is a specialization of→ role", text)
            self.assertIn("Agent —is a specialization of→ Observer: asserted → conjectured", text)
            self.assertIn("## Added", text)


if __name__ == "__main__":
    unittest.main()
