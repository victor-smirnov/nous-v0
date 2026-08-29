"""Shared builder for Gellish domain-extension dictionaries.

A spec module declares CONCEPTS / RELATIONS / PEOPLE / FACTS / ... and calls build(); the
builder assigns UIDs by list position inside the spec's block, writes a CSV in the Gellish
expression format (29 columns, column-role codes in row 2) and returns the uid map so other
specs can reference this spec's concepts by name.

UID policy: Gellish reserves < 100 000 000; each of our dictionaries owns a 100 000-wide block:
  concepts   base + 1 ...       relation types  base + 1001 ...
  role kinds base + 2001 ...    individuals     base + 3001 ...
Append, never reorder, once a release is shared.
"""
import csv, pathlib

# ---- Gellish anchors (standard dictionary, July 2020)
G = {
    "anything": "730000", "kind": "730066", "individual thing": "730067", "concept": "4990",
    "role": "160170", "relation": "2850", "information": "970002", "occurrence": "193671",
    "activity": "552492", "aspect": "790229", "physical object": "730044", "state": "790123",
    "quality": "551008", "quantity": "551381", "signal": "730047", "system": "730014",
    "organism": "990009", "person": "990010", "proposition": "970028", "claim": "990163",
    "question": "790665", "mechanism": "640108", "event": "192555", "memory": "70252",
    "computer": "70051", "neural network": "911102", "model": "492032", "experience": "587172",
    "binary relation between kinds": "5937", "binary relation between individual things": "4658",
    "transitive relation": "5520", "symmetric relation": "5521", "antisymmetric relation": "5912",
    "intransitive relation": "5913", "reflexive relation": "5962", "irreflexive relation": "5963",
    "modeling of an object": "5776", "being influenced": "6208", "cause of begin or end": "1922",
    "implication": "6233", "equality": "5828", "inequality": "5831", "composition": "1260",
    "possession of an aspect": "1727", "possession of a property": "4798", "authorship": "5126",
    "description": "4682", "publication": "5751", "classification": "1225", "specialisation": "1146",
}
G_NAMES = {"1922": "is the cause of", "1225": "classification of an individual thing", "1146": "is a kind of"}

HEADER_CODES = ["0", "69", "54", "71", "16", "5", "43", "44", "2", "101", "1", "60", "3", "45", "15", "201", "65", "4", "66", "7", "14", "50", "68", "67", "8", "9", "10", "12", "13"]
HEADER_NAMES = ["Presentation sequence", "UID of language of left hand object name", "Language of left hand object name",
                "UID of language community for left hand object name", "Name of language community for left hand object name",
                "UID of intention", "Name of intention", "Simultaneous left hand cardinalities", "UID of left hand object",
                "Name of left hand object", "UID of idea", "UID of kind of relation", "Name of kind of relation",
                "Simultaneous right hand cardinalities", "UID of right hand object", "Name of right hand object",
                "Partial definition", "Full definition", "UID of UoM", "UoM", "Remarks", "UID of collection of facts",
                "Name of collection of facts", "Status", "UID of successor of relation", "Date of start of life",
                "Date of latest change", "Originator of latest change", "Reference"]
RELNAME = {"1146": "is a kind of", "1225": "is classified as a", "1981": "is a synonym of", "6066": "is a base phrase for",
           "1986": "is an inverse phrase for", "5944": "has by definition as first role a",
           "5945": "has by definition as second role a", "5343": "is by definition a role of a"}
INTENT = {"assertion": "491285", "hypothesis": "491287", "definition": "491286"}   # 491285 is Gellish's; the others are ours


class Ext:
    def __init__(self, name, coll_uid, coll_name, base, date="29-aug-26", originator="Synthea", reference="", external=None, external_phrases=None):
        self.name, self.coll_uid, self.coll_name, self.base = name, coll_uid, coll_name, base
        self.date, self.originator, self.reference = date, originator, reference
        self.uid, self.names, self.role_uid = {}, dict(G_NAMES), {}
        for k, v in G.items():
            self.names.setdefault(v, k)
        self.external = external or {}          # name -> uid from other specs
        for k, v in self.external.items():
            self.names.setdefault(v, k)
        self.rows, self.idea = [], base * 10
        self.sem, self.disjoint = [], []
        self.phrases = {"is the cause of": ("1922", False), "is caused by": ("1922", True), "is a kind of": ("1146", False),
                        "is classified as a": ("1225", False), "implies": ("6233", False), "is implied by": ("6233", True)}
        self.phrases.update(external_phrases or {})

    # --- naming
    def ref(self, x):
        if x in self.uid: return self.uid[x]
        if x in self.role_uid: return self.role_uid[x]
        if x in self.external: return self.external[x]
        if x in G: return G[x]
        if x.isdigit(): return x
        raise KeyError(f"{self.name}: unknown reference {x!r}")

    def row(self, l, rel, r, fdef="", intent="assertion"):
        self.idea += 1
        rn = self.names.get(rel) or RELNAME.get(rel) or rel
        self.rows.append([str(len(self.rows) + 1), "910036", "English", "193259", "ontology", INTENT[intent], intent, "",
                          l, self.names[l], str(self.idea), rel, rn, "", r, self.names[r], "", fdef, "", "", "",
                          self.coll_uid, self.coll_name, "proposed", "", self.date, self.date, self.originator, self.reference])

    def alias_row(self, u, alias, rel="1981"):
        saved = self.names[u]; self.names[u] = alias
        self.row(u, rel, u)
        self.names[u] = saved

    # --- declarations
    def concepts(self, items):
        """items: (name, supertype | [supertypes], definition, synonyms)"""
        for i, (n, *_ ) in enumerate(items, 1):
            self.uid[n] = str(self.base + i); self.names[self.uid[n]] = n
        for name, sup, fdef, syns in items:
            u = self.uid[name]
            for i, sp in enumerate(sup if isinstance(sup, list) else [sup]):
                self.row(u, "1146", self.ref(sp), fdef if i == 0 else "")
            for s in syns:
                self.alias_row(u, s)

    def relations(self, items, role_overrides=None):
        """items: (name, supertype, base phrases, inverse phrases, props, role1, role2, definition, sem tag)"""
        role_overrides = role_overrides or {}
        for i, (n, *_ ) in enumerate(items, 1):
            self.uid[n] = str(self.base + 1000 + i); self.names[self.uid[n]] = n
        ri = 0
        for name, sup, base, inv, props, r1, r2, fdef, tag in items:
            r1, r2 = role_overrides.get(name, (r1, r2))
            u = self.uid[name]
            self.row(u, "1146", self.ref(sup), fdef)
            for p in props:
                self.row(u, "1146", G[p])
            for p in base:
                self.alias_row(u, p, "6066"); self.phrases.setdefault(p, (u, False))
            for p in inv:
                self.alias_row(u, p, "1986"); self.phrases.setdefault(p, (u, True))
            for pos, r in (("5944", r1), ("5945", r2)):
                if r:
                    rn, player = r
                    if rn not in self.role_uid:
                        ri += 1
                        self.role_uid[rn] = str(self.base + 2000 + ri); self.names[self.role_uid[rn]] = rn
                        self.row(self.role_uid[rn], "1146", G["role"])
                        self.row(self.role_uid[rn], "5343", self.ref(player))
                    self.row(u, pos, self.role_uid[rn])
            if tag:
                self.sem.append((u, tag))

    def people(self, items, holds_rel):
        """items: (name, kind, aliases, positions held). holds_rel: relation name whose base is 'is asserted by'."""
        for i, (n, *_ ) in enumerate(items, 1):
            self.uid[n] = str(self.base + 3000 + i); self.names[self.uid[n]] = n
        hr = self.ref(holds_rel)
        self.names.setdefault(hr, "is asserted by")
        for name, kind, aliases, held in items:
            u = self.uid[name]
            self.row(u, "1225", self.ref(kind))
            for a in aliases:
                self.alias_row(u, a)
            for h in held:
                self.row(self.ref(h), hr, u)

    def facts(self, items):
        """items: (left, relation phrase or name, right, intention) — theory statements between concepts.
        An inverse phrase swaps the sides so the stored row reads in the base direction."""
        for l, rel, r, *rest in items:
            intent = rest[0] if rest else "assertion"
            if rel in self.phrases:
                ru, swap = self.phrases[rel]
                if swap:
                    l, r = r, l
            else:
                ru, swap = self.ref(rel), False
            self.names.setdefault(ru, rel)
            self.row(self.ref(l), ru, self.ref(r), intent=intent)

    def gellish_aliases(self, items):
        for gu, p, d in items:
            self.names.setdefault(gu, gu)
            self.alias_row(gu, p, "6066" if d == "base" else "1986")

    def gellish_sem(self, items):
        self.sem += list(items)

    def disjoint_pairs(self, items):
        self.disjoint += [(self.ref(a), self.ref(b)) for a, b in items]

    # --- output
    def write(self, here):
        with (pathlib.Path(here) / f"{self.name}.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
            w.writerow(["Gellish", "English", "Version:", "0.3", self.date, "Domain extension", self.coll_name] + [""] * 22)
            w.writerow(HEADER_CODES); w.writerow(HEADER_NAMES)
            w.writerows(self.rows)
        return len(self.rows)
