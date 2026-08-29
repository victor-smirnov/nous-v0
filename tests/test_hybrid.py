"""Hybrid document container: fences ↔ tables, cross-block refs, declared residual."""
import pathlib, tempfile, unittest

from nous.gellish import hybrid, parse

DOC = """# Intro

Prose.

```gellish S1
F0001 | a | is classified as a | b | - | assertion | -
F0002 | F0001 | is offered as | literal | - | assertion | -
```

## Method

```gellish S2
F0001 | S1:F0001 | implies | F0001 | - | hypothesis | -
```

```gellish-residual S2
F0001 | modality | must | "shall be reported"
- | temporal | within 30 days | "within thirty days of notice"
```
"""


class Hybrid(unittest.TestCase):
    def test_blocks_and_refs(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "doc.md"; p.write_text(DOC)
            rows, resid, errors = parse.parse_paths([str(p)], {})
        self.assertEqual(errors, [])
        ids = [r[0] for r in rows]
        self.assertEqual(ids, ["S1:F0001", "S1:F0002", "S2:F0001"])
        s2 = rows[2]
        self.assertEqual((s2[1], s2[4]), ("S1:F0001", "S2:F0001"))       # global and local refs both resolve
        self.assertEqual(rows[1][1], "S1:F0001")
        self.assertEqual([(r[0], r[1]) for r in resid], [("S2:F0001", "modality"), ("", "temporal")])

    def test_extract_inject_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            d = pathlib.Path(d)
            doc = d / "doc.md"; doc.write_text(DOC)
            files = hybrid.extract(doc, d / "t")
            self.assertEqual(sorted(f.name for f in files), ["S1.txt", "S2.residual.txt", "S2.txt"])
            (d / "t" / "S1.txt").write_text("F0001 | a | is classified as a | c | - | assertion | -\n")
            (d / "t" / "S3.txt").write_text("# heading: Method\nF0001 | x | is a part of | y | - | hypothesis | -\n")
            out = hybrid.inject(doc, [d / "t" / "S1.txt", d / "t" / "S3.txt"], d / "out.md")
            text = out.read_text()
            self.assertIn("is classified as a | c", text)
            self.assertNotIn("is classified as a | b", text)
            self.assertLess(text.index("## Method"), text.index("```gellish S3"))
            self.assertIn("```gellish-residual S2", text)                 # untouched blocks survive
            rows, resid, errors = parse.parse_paths([str(out)], {})
            self.assertEqual(len(rows), 4); self.assertEqual(len(resid), 2); self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
