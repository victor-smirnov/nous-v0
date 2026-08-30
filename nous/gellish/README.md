# Gellish ontological reasoner (Soufflé)

A Datalog reasoner for Gellish fact tables over the **full Gellish English dictionary**
(gellish.net CSV release, July 2020: 117 828 rows → 68 965 concepts, 68 631 specialisations,
3 011 relation phrases, 1 007 role definitions). It closes the ontology (taxonomy, mereology,
identity, entailment), checks it for contradictions using the dictionary's own relation
algebra, audits the encoder against the v2 spec, grounds document entities in the dictionary,
and materialises everything the language could not absorb as a typed residual.
~0.6 s on 2 300 document facts + the whole dictionary.

```
nous gellish build-dict --fetch                       # once: download dictionary → data/dict, build data/dictfacts (+ ext/)
nous gellish build-dict                               # rebuild after editing ext/*/spec.py
nous gellish check tables/article-v1/C0*.txt -o REPORT.md    # parse → souffle → report; outputs in work/out
nous gellish ask "causal break"                       # everything known about a node
nous gellish why contradiction                        # proof trees (Soufflé provenance) for every contradiction
nous gellish why kb "freedom of B" "is classified as a" "causal break"   # why a derived edge holds
nous gellish enrich doc.md -o doc.enriched.md         # derived rows → ```gellish-derived``` blocks with provenance
nous gellish diff a.md b.md                           # semantic diff of two closures
nous gellish check --minlevel 4 ...                   # doctrine-only closure
nous gellish check --maxdepth 3 ...                   # tighter entailment budget
nous gellish check --theory off ...                   # document-only consistency (Synthea layer excluded)
```
(`python3 -m nous …` without installing.)

Files: `dictionary.py` (dictionary CSVs → Soufflé facts; parses by the stable column-role
UIDs in row 1, not by header names), `parse.py` (v2 tables → facts; phrase resolution),
`reasoner.dl` (the reasoner), `run.py`, `report.py`, `ask.py`, `why.py`. Outputs in `work/out/*.csv`: `kb`,
`contradiction`, `role_tension`, `commitment_tension`, `cap_tension`, `violation`,
`residual_phrase`, `truncated`, `entails_best`, `ground`, `ground_ambiguous`, `entity_span`, `stat`.
`data/dict` and `data/dictfacts` are git-ignored (45 MB); `build-dict --fetch` recreates them.

## Three layers

**1. Dictionary layer** (`d_*.facts`). Relation types are the concepts under 2850 `relation`
(8 028 of them in the closure). Their algebra is *data*: a relation type is transitive iff it
specialises 5520 `transitive relation`; likewise symmetric 5521, antisymmetric 5912,
intransitive 5913, reflexive 5962, irreflexive 5963. Phrases come from 6066 `is a base
phrase for` / 1986 `is an inverse phrase for`; an inverse phrase swaps left/right at parse
time so the left object is always the first-role player. Roles: 5944/5945 name the two role
kinds of a relation type, 5343 says what kind of thing may play each.

The generic closure is driven by that data and nothing else:

```
holds(X,V,Y)  :- holds(X,U,Y), d_spec(U,V)                       -- relation-type inheritance
holds(Y,U,X)  :- holds(X,U,Y), rel_prop(U,"symmetric")
holds(X,U,Z)  :- holds(X,U,Y), holds(Y,U,Z), rel_prop(U,"transitive")
contradiction :- holds(X,U,Y), holds(Y,U,X), rel_prop(U,"antisymmetric")   -- etc.
```

Specialisation (1146, with 1726 qualitative subtype beneath it) is transitive and
antisymmetric *by the dictionary*, so taxonomy closure and cycle detection are not special
cases. The one Gellish rule not expressible as a relation property — classification inherits
along specialisation — is written explicitly.

**2. Extension layer** (`ext/`). Two domain dictionaries in Gellish's own format, built by
`build-dict` together with the standard dictionary — see [ext/README.md](ext/README.md):
`philosophy_of_mind.csv` (UIDs 1007xxxxx: the field, position-neutral — positions, arguments,
theories, people, dialectical/provenance relations, and what the v2 spec needed and Gellish
lacks: entailment between facts, stance, figurativeness, negative relations) and
`synthea_bootstrap.csv` (UIDs 1008xxxxx: the Synthea theory as concepts + 31 theory facts).
`ext/sem.facts` binds reasoner semantics to relation-type UIDs, Gellish's own 6233 `implies`
and 1922 `is the cause of` included. On ambiguous phrases the domain dictionary shadows the
general one. The Synthea collection is a switchable **theory layer**: `--theory off` asks
whether the document contradicts *itself*, `hypothesis` (default) reads it through Synthea at
level 2, `doctrine` at level 4.

**3. Document layer.** Intention is the gate:

| intention | level | polarity |
|---|---|---|
| assertion, definition, requirement | 4 asserted | + |
| hedged-assertion | 3 hedged | + |
| hypothesis, prediction | 2 conjectured | + |
| denial, rebutted-claim | 4 | − |
| question | 0 | none |
| attributed-claim | **none of its own** — inherits the author's stance row, else `unresolved` | |

Only positive, non-figurative rows at or above `--minlevel` enter inference; derived facts
carry min(commitment); `*_best` keeps the strongest derivation. Commitment also flows through
entailment: asserted premises entailing a row stated as `hypothesis` → `commitment_tension`;
entailing a denied row → `contradiction("entailment")`.

**Grounding.** A document entity whose lowercased name equals a dictionary concept name or
alias (1981 synonym, 1982 abbreviation, 1984 noun form, …) is grounded — *only if the match
is unambiguous* (ambiguous ones go to `ground_ambiguous`). Through grounded entities the
dictionary's supertypes flow into the document graph **at level 2**: a bare-name match is a
hypothesis about reference, not knowledge, and the closure says so (`Transformer —is a kind
of→ electrical equipment item (conjectured)` is the honest output for a homonym). Role kinds
are checked for grounded players → `role_tension`.

**Provenance.** `nous gellish why` runs the program in Soufflé's `-t explain` mode and renders the proof
tree of any output tuple with the noise removed: leaves are source rows (`row C01:F0242 ⟨…⟩
(assertion)`) and dictionary facts (`dict alias: irreducible residual · computational residual`,
`dict coll: … 100800000`), nodes are rule applications. Filters are substring matches on the
output columns (`why contradiction entailment`, `why role_tension "need conflict"`); a
raw atom is accepted too. ~1 s per call; every call re-evaluates the program.

**Thesis stratum and structural summary.** If an extension declares a *problem* — a concept with
components (`X | is a part of | psychophysical problem`) — the reasoner reports which components the
document *addresses*: a component counts as addressed when an entity grounded to it (or a subtype) is
linked by ≤ 2 explanatory relations (projection, reduction, constitution, realization, identity,
explanation, generation, causation, or classification into the document's own concept) to a concept
that is not in the public dictionaries — the document's own apparatus. The concepts addressing most
components are its *hubs*. `nous gellish summarize` turns this into a selection of stated rows
(`gellish-summary` block, budgeted): the explanatory paths component → hub, definitions of the hubs,
the author's strong salience rows, the foils with their rebuttals, central claims about the hubs. No
new claims are ever added; the block decodes into an abstract. On the article: 8/10 components of the
psychophysical problem addressed, hub = apparent causal break / computational residual — the
"particular but complete solution" that LLM summaries of the article missed.

**Subject stratum.** With `ext/subject/profiles.txt` loaded beside a document, every fact gets a third status
per subject type besides holds / does not hold: **invisible** — some object of the fact needs, along every access
dimension it can be reached by, more recognizing capacity than the subject has. `recognizable(X, S)` holds if at
least one dimension suffices (alternative access routes: Beingness through trained reflection *or* through the
residual mechanism). Facts indexed with `holds from the point of view of` hold only for those subjects;
`perspectival_difference(F, S1, S2)` lists what holds for one and not another while both could see it.
**Seen as:** `X | appears as | Y` rows indexed to a subject give `view(X, S, "as", Y)` — a status in its own
right (a subject may recognise X and still see it as Y), and `visible_as(F, S, X, Y)` for facts that are
invisible in their own terms but reachable under the guise. Report section "Subject views". Grades inherit down classification and specialisation.

**Enrichment.** `nous gellish enrich` writes what the closure added back into the document as
```` ```gellish-derived <id> ```` blocks: one row per derived edge, intention by level, context
= provenance (`derived: closure`, `theory: Synthea`, `field: depth 1`, `gellish: depth 1`,
`…: definition`). Top-cut: upper-ontology stop list, ancestry deeper than `--depth` (1),
standard-Gellish facts off unless `--gellish-facts`; identity classes collapsed to their
first-mentioned member; rows the document already states are not repeated. On the article:
563 derived rows for 2 296 stated. **Diff.** `nous gellish diff a.md b.md` closes both and
lists edges added / removed / re-levelled, plus counts of findings that appeared or vanished.

**HOCP.** Entailment closure runs under a depth budget; refused chains are materialised as
`truncated(a, b, c)` — the reasoner's own truncated tail, exposed rather than dropped.

## What it found on the article (C01–C09, 2 296 rows)

- **Phrase coverage.** With the philosophy-of-mind extension 1 673 rows resolve to a relation
  type (777 standard Gellish, 896 extension); 623 (460 distinct phrases) are residual — down
  from 868 with the standard dictionary alone. The residual head is domain verbs the encoder
  invented per nuance (`describes`, `encodes`, `generates`, `monitors`, `maximizes`, …) — the
  input to the next dictionary revision.
- **Double negation is a spec hole.** 76 rows carry a negative relation or negated phrase
  *and* intention `denial`. Encoders use `denial` for "this sentence is negative", the spec
  means "the author denies this proposition". Two of three `entailment` contradictions are
  this defect. The spec must state that the triple always carries the positive proposition.
- **Predictions that are theorems.** 7 rows stated as `prediction`/`hypothesis` are entailed
  by premises and entailment rows the author *asserts*. Calibration inconsistency invisible to
  overlap metrics.
- **Metaphor in taxonomy.** 21 classification/identity rows are simultaneously marked
  figurative; excluded from inheritance. A reasoner without the gate would literalise them —
  the v1 inversion, reproduced mechanically.
- **Grounding: 201 unambiguous, 23 ambiguous, 2 004 kb edges from the dictionaries, all at level 2.** Aliases grounding to one dictionary individual are merged (`Dennett` ≡ `Dennett 1991` ≡ `Dennett, D. C.`).
  Most are right (`Anokhin monograph → physical document`), some are homonyms
  (`current Transformer → measurement transformer`). 13 role tensions survive, most of them
  the v2 spec's ban 1 enforced by the dictionary: `need conflict is a cause of …` is flagged
  because Gellish 1922 wants an *occurrence* as cause (see [ext/README.md](ext/README.md)).
  Note also that the dictionary lists bare `is` as a phrase of 1225, so `physiological need
  is cyclical` becomes a classification — arguably right, worth knowing.
- Closure is shallow: longest entailment chain depth 2. The tables are a forest of local
  claims, not a deep hierarchy.

## Conventions

- Fact UIDs are namespaced by table (`C03:F0012`); entities are not — the same name in two
  tables is one node, so cross-chunk consistency is checked for free (85 entities span >1 table).
- Ambiguous phrases resolve to a domain-extension UID if one exists (domain shadows general),
  else to the lowest UID (e.g. `precedes` → 1385 succession, not 5815 temporal); each case is
  reported on stderr.
- `author / the authors / this article / we` → `the author`.

## Next

1. Fix the spec: positive-proposition rule for `denial`; second-order phrases only over fact
   refs; give the encoder the dictionary phrases so `other` rows must go to `untranslatable`.
2. Feed `residual_phrase` back into the extension per genre (legal: `shall`, `may`,
   `is defined in`, cross-references).
3. Grounding with context: use the document's own classifications to disambiguate homonyms
   against dictionary supertypes (a `Transformer` classified as `vectorized FCRS` is not an
   `electrical equipment item`) — turn `ground_ambiguous` into ranked hypotheses.
4. Retraction / incremental mode belongs to Nous/Deem (Logos ADR 0015); this is batch closure.
5. Value/UoM column: the dictionary's 5 341 units and scales are loaded but unused.
