# Gellish domain extensions

Two dictionaries, built by `nous gellish build-dict` from the shared builder
`nous/gellish/ext/builder.py` into the Gellish expression format (same 29 columns as the standard files):

| file | collection | UID block | content |
|---|---|---|---|
| `philosophy_of_mind/spec.py` → `philosophy_of_mind.csv` | 100700000 *Philosophy of mind (field)* | 1007xxxxx | the field, position-neutral: 88 concepts, 61 relation types, 54 role kinds, 29 people, 778 rows |
| `synthea_bootstrap/spec.py` → `synthea_bootstrap.csv` | 100800000 *Synthea bootstrap* | 1008xxxxx | one theory: 52 concepts, 5 relation types, 31 theory facts, 158 rows |

plus `sem.facts` (reasoner tags on relation-type UIDs) and `disjoint_rel.facts`.

## Why two

A domain dictionary that mixes *the field* with *a position in it* turns disagreement into
error: encode Chalmers with a dictionary in which `approximationism ⊑ illusionism` and
`freedom ⊑ epistemic quale` are facts, and the reasoner will "find contradictions" that are
just Chalmers not being Synthea. So:

- **philosophy_of_mind** says what things *are called* and how the field *argues*: positions
  (physicalism … panpsychism, illusionism, eliminativism), theories of mind (HOT, GWT, IIT,
  predictive processing, somatic marker, TFS, enactivism, dual-process, artificial curiosity,
  multiple drafts), arguments (zombie, Chinese room, knowledge argument, hard problem, bat
  question), distinctions (phenomenal/access, quale, explanatory gap, self-model gap,
  supervenience, downward causation), psychology's vocabulary with neutral definitions (need,
  emotion, motivation, feeling, thought, intuition, salience, valence, prediction error, acceptor
  of results of action), LLM engineering facts (token bottleneck, computational constraint,
  Transformer, LLM), people with citation aliases, and the relation types the field uses
  (projection, realization, supervenience, constitution, reduction, functional equivalence,
  metaphor; signals/tracks/steers/gates; explains/predicts/objects/rebuts/replies/concedes;
  provenance and stance; bibliographic). It asserts nothing about which position is right.
- **synthea_bootstrap** is the theory: the Observer stack (proto-Observer, Observer, Agent,
  Moral Agent, the three conditions), apparent causal break, computational residual, HOCP,
  NCode/CCode, self-report, narrative, subjective average, need taxonomy and need/emotional
  profiles, attention channel, cognitive cycle, forward simulation, Beingness and the fourteen
  epistemic qualia, functional profile / deficit / hyperfunction, hyperplasticity, cognitive
  resistance, psychosemantics, approximationism, substrate chauvinism, functional
  consciousness — each hooked to a field concept (Observer ⊑ role, epistemic quale ⊑ quale,
  approximationism ⊑ illusionism, functional consciousness ⊑ consciousness) — and the
  bootstrap's **claims as facts** between concepts: `cognitive code is a projection of neural
  code`, `motivation is a projection of need`, `emotion is a signal of need`, `Observer is
  constituted by apparent causal break`, `Beingness quale is identical to Observer`, `HOCP is
  a necessary condition for Observer`, `Transformer is functionally equivalent to vectorized
  FCRS (hypothesis)`, `approximationism is asserted by Victor Smirnov`, `eliminativism is
  rejected by Victor Smirnov`, …

## The theory layer in the reasoner

`nous gellish check --theory off | hypothesis | doctrine` (default `hypothesis`):

| mode | grounding into Synthea concepts | level of Synthea-derived edges | what it answers |
|---|---|---|---|
| `off` | none | — | *does the document contradict itself?* |
| `hypothesis` | yes | 2 (conjectured) | *what does the document look like read through Synthea, held tentatively?* |
| `doctrine` | yes | 4 (asserted) | *what follows if Synthea is taken as true?* |

The field dictionary always enters at level 2 (a bare-name match is a hypothesis about
reference); only the Synthea collection is switchable. Every concept and fact carries its
collection (`d_coll.facts`, 4th column of `d_fact.facts`), so the gate is data-driven —
a third dictionary would get its own switch the same way.

On the article (C01–C09):

| | `off` | `hypothesis` |
|---|---:|---:|
| entities grounded | 160 | 200 (31 into Synthea) |
| kb edges from dictionaries | 1 650 | 2 118 |
| contradictions | 4 | 6 |

The two extra contradictions under `hypothesis` are both `identity-vs-taxonomy`: the article
classifies causal break under irreducible residual, while *our* synonym rows declare `truncated
tail` = `irreducible residual` = `computational residual`. Under `off` they vanish — they are
the document disagreeing with the theory's vocabulary, not with itself. That distinction is
the point of the split.

## Conventions

- UIDs by list position inside each block (concepts `base+1…`, relation types `base+1001…`,
  role kinds `base+2001…`, individuals `base+3001…`); append, never reorder, once shared.
- Domain shadows general on ambiguous phrases (`is composed of` → constitution, not Gellish
  5623). Synthea does not redefine field phrases; it adds facts and subtypes.
- Cross-dictionary references are by name (a spec lists `DEPENDS` and receives the built dependencies' uid and phrase maps).
- Intention UIDs 491286/491287 (`definition`, `hypothesis`) are ours; Gellish only ships
  491285 `statement`. `gellish_dict.py` ignores the intention column, so this only documents
  intent for human readers for now.
- Role players for claim-sides of dialectical relations are `anything`: Gellish's `claim` is
  a *role* and `proposition` a *quality* (⊑ attitude ⊑ characteristic), neither usable as a
  player kind.

## Known gaps / next

- The field dictionary is thin where the article is thin: no philosophy of perception, no
  personal identity, no free will beyond what the Observer stack needs, no phenomenology
  (Husserl/Merleau-Ponty), no theory of intentionality beyond `is directed toward`, no
  mental causation debate (exclusion argument), no representationalism / higher-order variants.
  The next step is to build it out as a proper ontology of the field rather than as the
  article's shadow.
- Theory facts are stated between *kinds*; Gellish would want some of them as conceptual
  relations (`can be a`…). Left as is until the reasoner needs the distinction.
- Gellish's upper ontology puts `occurrence` under `relation between individual things`, so
  HOCP inherits `higher order relation`. Documented, not fixed.
