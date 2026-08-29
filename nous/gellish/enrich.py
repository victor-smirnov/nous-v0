"""Enrichment: write what the reasoner derived back into the hybrid document.

For every ```gellish <id>``` block, an ```gellish-derived <id>``` block is written (replacing an
existing one) with rows the closure added about that section's entities:

  fact-UID | left | relation phrase | right | value | intention | context
  D0001    | Dennett | is classified as a | philosopher | - | hypothesis | dictionary: philosophy_of_mind (depth 1)

- intention follows the derivation level: 4 → assertion, 3 → hedged-assertion, 2 → hypothesis.
- context carries provenance: `derived: closure`, `theory: Synthea`, `field: <depth>`, `gellish: <depth>`.
- top-cut: dictionary ancestry deeper than --depth (default 1), the upper-ontology stop list,
  and standard-Gellish *facts* (engineering content, --gellish-facts to keep) are dropped.
- identity classes are collapsed: rows are written once, for the first-mentioned member of a
  `same` class, so aliases do not repeat every derivation.
- a row is placed in the first section that mentions its left entity (else right).
- definitions of grounded entities are added as `X | is defined as | "…"` rows (--no-defs to skip).
"""
import csv, pathlib, re

from . import parse

LEVEL_INTENT = {"4": "assertion", "3": "hedged-assertion", "2": "hypothesis", "1": "hypothesis"}
STOP = {"anything", "concept", "individual thing", "totality", "matter", "material", "physical object", "artefact",
        "solid item", "single object", "relation", "relation between individual things", "binary relation between individual things",
        "higher order or variable order relation", "higher order or variable order relation between individual things",
        "aspect", "extrinsic aspect", "characteristic", "attitude", "social attitude", "intention", "communicative intent",
        "quality", "state", "role", "related", "involved", "related individual thing", "kind", "occurrence", "assembly",
        "lifeform", "social entity", "resource", "possession", "information", "individual", "wave", "inanimate physical object",
        "property", "scalar property", "calculating", "mathematical operation", "physical process", "spatial object", "part"}
ENTAIL = {"implies", "is a necessary condition for", "is a sufficient condition for", "is logically equivalent to"}


def read_tsv(p):
    p = pathlib.Path(p)
    if not p.exists():
        return []
    with p.open(newline="") as f:
        return list(csv.reader(f, delimiter="\t"))


def section_entities(doc):
    """section id -> ordered set of entity names stated in that section (left and right objects)."""
    ents, order = {}, []
    for kind, sid, lines in parse.iter_blocks(doc):
        if kind != "gellish":
            continue
        order.append(sid)
        s = ents.setdefault(sid, set())
        for r in parse.parse_rows(lines, sid, {}, []):
            for c in (r[1], r[4]):
                if c and not re.match(r"^[A-Za-z0-9_.-]+:F\d+$", c):
                    s.add(c)
    return ents, order


FACT_REF = re.compile(r"^[A-Za-z0-9_.-]+:F\d+$")


def identity_classes(out_dir, order, ents):
    """entity -> canonical name (first-mentioned member of its identity class)."""
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            parent[x] = parent.get(parent[x], parent[x]); x = parent[x]
        return x

    for l, rel, r, lv, origin in read_tsv(pathlib.Path(out_dir) / "kb.csv"):
        if rel == "is identical to" and not FACT_REF.match(l) and not FACT_REF.match(r):
            a, b = find(l), find(r)
            if a != b:
                parent[a] = b
    first = {}
    for sid in order:
        for e in sorted(ents[sid]):
            first.setdefault(find(e), e)
    return lambda x: first.get(find(x), x)


def plan(doc, out_dir, depth=1, defs=True, include_derived=True, gellish_facts=False):
    """-> {section id: [row tuples]}"""
    ents, order = section_entities(doc)
    if not order:
        return {}
    where = {}
    for sid in order:                       # first section mentioning the entity wins
        for e in ents[sid]:
            where.setdefault(e, sid)
    placed = {sid: [] for sid in order}
    canon = identity_classes(out_dir, order, ents)
    stated = set()
    for kind, sid, lines in parse.iter_blocks(doc):
        if kind == "gellish":
            for r in parse.parse_rows(lines, sid, {}, []):
                stated.add((canon(r[1]), r[3], canon(r[4])))

    def place(l, r, row):
        sid = where.get(l) or where.get(r)
        if sid:
            placed[sid].append(row)

    seen = set()
    for l, rel, r, lv, origin, d in read_tsv(pathlib.Path(out_dir) / "enrich.csv"):
        d = int(d)
        if (FACT_REF.match(r) or FACT_REF.match(l)) and rel not in ENTAIL:
            continue
        if r.lower() in STOP or l.lower() in STOP:
            continue
        if origin in ("gellish", "field", "theory"):
            if d > depth and r not in where:          # a deep ancestor the document itself talks about stays
                continue
            if origin == "gellish" and d == 0 and not gellish_facts:
                continue
        if origin == "derived" and not include_derived:
            continue
        cl, cr = canon(l), canon(r)
        key = (cl, rel, cr)
        if key in seen or cl == cr or key in stated:
            continue
        seen.add(key)
        ctx = {"derived": "derived: closure", "theory": f"theory: Synthea (depth {d})" if d else "theory: Synthea",
               "field": f"field: depth {d}" if d else "field: fact", "gellish": f"gellish: depth {d}" if d else "gellish: fact"}[origin]
        place(cl, cr, (cl, rel, cr, "-", LEVEL_INTENT.get(lv, "hypothesis"), ctx))
    if defs:
        for x, text, origin in read_tsv(pathlib.Path(out_dir) / "enrich_def.csv"):
            cx = canon(x)
            if (cx, "def") in seen or origin == "gellish" and not gellish_facts:
                continue
            seen.add((cx, "def"))
            place(cx, "", (cx, "is defined as", '"' + text.replace("|", "/") + '"', "-", "definition",
                          {"theory": "theory: Synthea", "field": "field: definition", "gellish": "gellish: definition"}[origin]))
    return placed


def write(doc, placed, out=None):
    doc = pathlib.Path(doc)
    lines = doc.read_text(encoding="utf-8").splitlines()
    # drop existing derived blocks
    kept, skip = [], False
    for l in lines:
        if re.match(r"^```\s*gellish-derived\b", l):
            skip = True; continue
        if skip:
            if l.strip() == "```":
                skip = False
            continue
        kept.append(l)
    # insert after the matching gellish block
    result, i = [], 0
    while i < len(kept):
        l = kept[i]; result.append(l)
        m = re.match(r"^```\s*gellish(?:\s+(\S+))?\s*$", l)
        if m:
            sid = m.group(1)
            i += 1
            while i < len(kept) and kept[i].strip() != "```":
                result.append(kept[i]); i += 1
            if i < len(kept):
                result.append(kept[i])
            rows = placed.get(sid, [])
            if rows:
                result += ["", f"```gellish-derived {sid}"]
                for n, row in enumerate(rows, 1):
                    result.append(f"D{n:04d} | " + " | ".join(row))
                result.append("```")
        i += 1
    out = pathlib.Path(out) if out else doc
    out.write_text("\n".join(result).rstrip("\n") + "\n", encoding="utf-8")
    return out, sum(len(v) for v in placed.values())
