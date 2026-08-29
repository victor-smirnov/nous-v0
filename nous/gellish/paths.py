"""Where things live.

  repo/data/dict        the gellish.net CSV release (git-ignored; `nous gellish build-dict --fetch`)
  repo/data/dictfacts   Soufflé facts exported from the dictionary + extensions
  repo/ext/<name>/spec.py   domain-extension specs (built into data/dictfacts)
  repo/work/facts, repo/work/out, repo/work/prov   per-run working directories

Override the root with NOUS_DATA=<dir> (then <dir>/dict, <dir>/dictfacts, <dir>/work).
"""
import os, pathlib, shutil, sys

PKG = pathlib.Path(__file__).resolve().parent
REPO = PKG.parent.parent
DATA = pathlib.Path(os.environ.get("NOUS_DATA", REPO / "data"))
EXT = REPO / "ext"

DICT_URL = "https://www.gellish.net/wp-content/uploads/2024/09/Gellish-Dictionary-zip-CSV-files-July-2020.zip"


class Workspace:
    def __init__(self, work=None):
        self.dict = DATA / "dict"
        self.dictfacts = DATA / "dictfacts"
        self.work = pathlib.Path(work) if work else (DATA / "work" if "NOUS_DATA" in os.environ else REPO / "work")
        self.facts = self.work / "facts"
        self.out = self.work / "out"
        self.prov = self.work / "prov"
        self.reasoner = PKG / "reasoner.dl"

    def fresh(self):
        for d in (self.facts, self.out):
            shutil.rmtree(d, ignore_errors=True)
            d.mkdir(parents=True)
        self.prov.mkdir(parents=True, exist_ok=True)

    def require_dictfacts(self):
        if not (self.dictfacts / "d_phrase.facts").exists():
            sys.exit(f"no dictionary facts in {self.dictfacts} — run `nous gellish build-dict --fetch` first")


def require_souffle():
    if shutil.which("souffle") is None:
        sys.exit("souffle not found on PATH (https://souffle-lang.github.io/install) — the reasoner needs it")
