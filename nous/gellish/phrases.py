"""Generate the relation-phrase reference the encoder works from (spec/phrases.md).

Default: every relation type of the domain extensions plus a curated core of standard Gellish
relation types. --all: every relation type in the dictionary that has a phrase (~1 600).
"""
import collections, pathlib

from . import paths

CORE = ["1146", "1225", "1260", "1727", "4798", "4682", "5126", "5751", "1922", "6233", "5828", "5831",
        "5829", "5023", "5830", "1388", "1385", "5815", "1384", "4872", "6012", "5020", "2044", "1732", "5776",
        "6208", "5452", "5160", "2071", "5396"]
FAMILY_ORDER = ["taxonomy & identity", "part-whole & constitution", "projection & realization", "causation, conditions & logic",
                "needs, signals & control", "dialectics & provenance", "bibliographic", "quantities, time & other"]


def load(dictfacts):
    d = pathlib.Path(dictfacts)
    name = {}
    for line in (d / "d_concept.facts").read_text(encoding="utf-8").splitlines():
        u, n = line.split("\t", 1); name[u] = n
    phr = collections.defaultdict(lambda: {"base": [], "inv": []})
    for line in (d / "d_phrase.facts").read_text(encoding="utf-8").splitlines():
        p, u, k = line.split("\t"); phr[u][k].append(p)
    spec = collections.defaultdict(list)
    for line in (d / "d_spec.facts").read_text(encoding="utf-8").splitlines():
        a, b, _ = line.split("\t"); spec[a].append(b)
    coll = {}
    for line in (d / "d_coll.facts").read_text(encoding="utf-8").splitlines():
        u, c = line.split("\t"); coll[u] = c
    role, role_of = collections.defaultdict(dict), {}
    for line in (d / "d_role.facts").read_text(encoding="utf-8").splitlines():
        u, pos, r = line.split("\t"); role[u][pos] = r
    for line in (d / "d_role_of.facts").read_text(encoding="utf-8").splitlines():
        r, k = line.split("\t"); role_of[r] = k
    defs = {}
    for line in (d / "d_def.facts").read_text(encoding="utf-8").splitlines():
        u, t = line.split("\t", 1); defs[u] = t
    return name, phr, spec, coll, role, role_of, defs


def ancestors(u, spec, limit=40):
    seen, stack = set(), [u]
    while stack and len(seen) < limit:
        x = stack.pop()
        for y in spec.get(x, []):
            if y not in seen:
                seen.add(y); stack.append(y)
    return seen


PROPS = {"5520": "transitive", "5521": "symmetric", "5912": "antisymmetric", "5913": "intransitive", "5962": "reflexive", "5963": "irreflexive"}


def family(u, anc, name):
    n = name.get(u, "").lower()
    if any(k in n for k in ("quantif", "scale", "boundary", "greater", "less than", "temporal", "sequence", "begin", "during", "dating", "succession")):
        return FAMILY_ORDER[7] if "dating" not in n else FAMILY_ORDER[6]
    if u in ("1146", "1225") or "identity" in n or "distinctness" in n or "classification" in n or "equality" in n or "inequality" in n:
        return FAMILY_ORDER[0]
    if u in ("1260", "5623", "1190") or "constitution" in n or "composition" in n or "assembly" in n:
        return FAMILY_ORDER[1]
    if "5776" in anc or u == "5776" or "realization" in n or "supervenience" in n or "reduction" in n or "encoding" in n or "manifestation" in n or "equivalence" in n or "analogy" in n or "metaphor" in n:
        return FAMILY_ORDER[2]
    if u in ("1922", "6233") or "condition" in n or "implication" in n or "explanation" in n or "prediction" in n or "counterexample" in n or "generalization" in n:
        return FAMILY_ORDER[3]
    if "6208" in anc or u == "6208" or any(k in n for k in ("signal", "tracking", "evaluation", "monitoring", "steering", "optimization", "minimization", "encounter", "conclusion from", "acting from", "directedness", "persistence", "generation", "reconstruction", "functional", "exhibition", "possession")):
        return FAMILY_ORDER[4]
    if any(k in n for k in ("assertion by", "endorsement", "rejection", "offering", "qualification", "commitment", "objection", "rebuttal", "reply", "concession", "contrast", "elaboration", "evidential", "inversion", "reformulation", "exemplification", "description", "authorship")):
        return FAMILY_ORDER[5]
    if any(k in n for k in ("dating", "publication", "citation", "publisher")):
        return FAMILY_ORDER[6]
    return FAMILY_ORDER[7]


def render(dictfacts, everything=False):
    name, phr, spec, coll, role, role_of, defs = load(dictfacts)
    rels = [u for u in phr if everything or u in CORE or coll.get(u, "").startswith("1007") or coll.get(u, "").startswith("1008")]
    groups = collections.defaultdict(list)
    for u in rels:
        anc = ancestors(u, spec)
        props = ", ".join(sorted(PROPS[a] for a in anc if a in PROPS))
        r1 = role_of.get(role[u].get("1", ""), ""); r2 = role_of.get(role[u].get("2", ""), "")
        roles = ""
        if r1 or r2:
            roles = f"{name.get(r1, '?') if r1 else '·'} → {name.get(r2, '?') if r2 else '·'}"
        src = "Gellish" if not coll.get(u, "").startswith("100") else ("Synthea" if coll[u].startswith("1008") else "field")
        groups[family(u, anc, name)].append((name.get(u, u), u, phr[u]["base"], phr[u]["inv"], props, roles, src, defs.get(u, "")))
    out = ["# Relation phrases for the encoder", "",
           "Use these phrases in the relation column, exactly as written. A phrase from the *inverse* column",
           "reads right-to-left (`A has as part B` ≡ `B is a part of A`); both are accepted. Roles say what",
           "kind of thing may stand left → right. Anything not here goes to the `gellish-residual` block.", ""]
    total = 0
    for fam in FAMILY_ORDER:
        items = sorted(groups.get(fam, []), key=lambda x: (x[6] != "Gellish", x[0]))
        if not items:
            continue
        out += [f"## {fam}", "", "| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |", "|---|---|---|---|---|---|"]
        for n, u, base, inv, props, roles, src, d in items:
            out.append(f"| {n} ({u}) | {' · '.join(base)} | {' · '.join(inv)} | {roles} | {props} | {src} |")
            total += 1
        out.append("")
    out.insert(6, f"{total} relation types.\n")
    return "\n".join(out)


def main(out=None, everything=False):
    ws = paths.Workspace(); ws.require_dictfacts()
    text = render(ws.dictfacts, everything)
    if out:
        pathlib.Path(out).write_text(text, encoding="utf-8")
    return text
