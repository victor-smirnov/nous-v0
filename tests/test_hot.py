"""The protopathic layer: what an observer has of a subject's signals only as mass, never as a name."""
import csv, pathlib, tempfile, unittest

from nous.gellish import paths, run

# One subject, four signals of unequal weight. Two observers over the same signals: one names the heavy
# signal and leaves the light ones to the tail, the other names the light ones and leaves the heavy one.
# Everything else is identical, so whatever the layer says about them comes from the split alone.
LOW = """# heading: proto
F0001 | sys-A | is a case of | cognitive system | - | assertion | -
F0002 | sys-A | encounters | its own irreducibility | - | assertion | -
F0003 | sys-A | concludes | its own separateness | - | assertion | -
F0004 | sys-A | acts from | its own conclusion | - | assertion | -
F0010 | need-1 | is a need of | sys-A | 1.0 | assertion | -
F0011 | need-1 | is active in | sys-A | - | assertion | -
F0012 | need-2 | is a need of | sys-A | 1.0 | assertion | -
F0013 | need-2 | is active in | sys-A | - | assertion | -
F0020 | stim | is a stimulus in | sys-A | - | assertion | -
F0021 | stim | has satisfaction delta | need-1 | -0.9 | assertion | the heavy one
F0022 | stim | has satisfaction delta | need-2 | -0.1 | assertion | light
F0030 | stim-2 | is a stimulus in | sys-A | - | assertion | -
F0031 | stim-2 | has satisfaction delta | need-1 | -0.2 | assertion | light
F0032 | stim-2 | has satisfaction delta | need-2 | 0.1 | assertion | light
"""

def edges(heavy_names, light_names):
    rows = [f"F0100 | {heavy_names} | is aware that | proto:F0021 | - | assertion | -"]
    for i, f in enumerate(("F0022", "F0031", "F0032")):
        rows.append(f"F{110 + i} | {light_names} | is aware that | proto:{f} | - | assertion | -")
    return "# heading: proto-hot\n" + "\n".join(rows) + "\n"


def table(out, name):
    return list(csv.reader((out / f"{name}.csv").open(newline=""), delimiter="\t"))


def stats(out, name):
    return {(o, s, k): float(v) for o, s, k, v in table(out, name)}


def analyse(hot_text):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d)
        (p / "proto.txt").write_text(LOW); (p / "proto-hot.txt").write_text(hot_text)
        ws = paths.Workspace(p / "w")
        run.check(ws, [str(p / "proto.txt"), str(p / "proto-hot.txt")], theory="doctrine", quiet=True)
        return {
            "proto": stats(ws.out, "proto"),
            "frame": stats(ws.out, "frame_stat"),
            "nameless": {(o, s): float(v) for o, s, v in table(ws.out, "nameless_share")},
            "displacement": {(o, s) for o, s in table(ws.out, "displacement")},
            "tail_keys": {(o, f) for o, _, f, _ in table(ws.out, "tail")},
        }


class Protopathic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = analyse(edges("obs-heavy", "obs-light"))

    def test_tail_is_the_complement_of_the_frame(self):
        self.assertEqual(self.r["tail_keys"], {("obs-heavy", "proto:F0022"), ("obs-heavy", "proto:F0031"), ("obs-heavy", "proto:F0032"),
                                               ("obs-light", "proto:F0021")})

    def test_statistics_survive_the_projection(self):
        p = self.r["proto"]
        self.assertAlmostEqual(p[("obs-light", "sys-A", "intensity")], 0.9)
        self.assertAlmostEqual(p[("obs-light", "sys-A", "valence")], -0.9)
        self.assertAlmostEqual(p[("obs-light", "sys-A", "spread")], 0.0)      # one contributor: fully localised
        self.assertAlmostEqual(p[("obs-heavy", "sys-A", "intensity")], 0.4)
        self.assertAlmostEqual(p[("obs-heavy", "sys-A", "valence")], -0.2)    # -0.1 - 0.2 + 0.1
        self.assertGreater(p[("obs-heavy", "sys-A", "spread")], 0.6)          # three contributors: diffuse

    def test_nameless_share_orders_the_observers(self):
        n = self.r["nameless"]
        self.assertAlmostEqual(n[("obs-light", "sys-A")], 0.9 / 1.3)
        self.assertAlmostEqual(n[("obs-heavy", "sys-A")], 0.4 / 1.3)

    def test_displacement_discriminates(self):
        """Same signals, same number of edges within one; a full frame is not a well-placed one."""
        self.assertEqual(self.r["displacement"], {("obs-light", "sys-A")})

    def test_displacement_follows_the_split_not_the_name(self):
        """Perturbation: swap which observer names what, and the finding moves with the split."""
        r = analyse(edges("obs-light", "obs-heavy"))
        self.assertEqual(r["displacement"], {("obs-heavy", "sys-A")})


if __name__ == "__main__":
    unittest.main()
