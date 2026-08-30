# Encoding specification v3.1

How prose becomes a Gellish fact table. v3 kept everything v2 measured as working (fact UIDs,
mandatory intention, reified second-order rows, the causation ban) and fixed what the reasoner
found broken in v2 tables: double negation, second-order rows on non-facts, invented phrases.
**v3.1** adds what the article-scale run showed missing: internal cross-references (R10), the
subject's point of view (R11), and a quote rule that no longer contradicts itself.

## Output

One fenced block per section of the source (see `hybrid-format.md`):

```
```gellish <SECTION-ID>
fact-UID | left object | relation phrase | right object | value/UoM | intention | context
```
```

- `fact-UID`: `F0001, F0002, …`, unique within the block. Every row has one.
- `left object` / `right object`: a thing, a kind, or a fact reference — local `F0007` or
  global `S2.1:F0007`. Object names name things and kinds; they are never sentences. Use the
  same name for the same thing throughout the document (the reasoner merges by name).
- `relation phrase`: **from `phrases.md`, exactly as written**. Never invent a phrase; never
  prefix a numeric UID. If no phrase fits, the content goes to the residual block.
- `value/UoM`: a value with its unit when the right object is a quantity; else `-`.
- `intention`: mandatory, from the enum below. No default.
- `context`: validity scope (section, condition, time), or `-`.

## R1 — the positive-proposition rule (new)

**The triple always states the positive proposition; `denial` negates it.**

```
F0012 | Observer | can compute | own truncated tail | - | denial | -        ← right
F0012 | Observer | cannot compute | own truncated tail | - | denial | -     ← WRONG (double negation)
F0012 | Observer | cannot compute | own truncated tail | - | assertion | -  ← WRONG (invented negative phrase)
```

Negative phrases (`is not`, `cannot`, `lacks`, `does not`, `is distinct from`) are not used with
`denial`. The only negative relation phrases allowed are those in `phrases.md` (`is distinct
from`, `is not classified as a`, `has as functional deficit`), and they take `assertion`.

## R2 — intention (unchanged from v2, restated)

The author's commitment to the row, not the row's content.

| intention | meaning |
|---|---|
| assertion | flat commitment, unhedged — a marked, strong choice |
| hedged-assertion | committed with reservation ("typically", "largely", "tends to") |
| hypothesis | conjecture to be tested ("we propose", "remains a hypothesis") |
| prediction | what will be observed ("should measurably narrow") |
| definition | stipulation of usage, not a discovery |
| question | posed, not answered here |
| denial | the author asserts the proposition is NOT the case (see R1) |
| requirement | norm, specification, necessary condition ("shall", "must") |
| attributed-claim | asserted by someone else; the author's stance is a separate row (R4) |
| rebutted-claim | raised by the author only to reject it (R5) |

If the source hedges, do not write `assertion`. When in doubt, hedge.

## R3 — second-order rows only over facts (tightened)

These phrases take a **fact reference** as left object, never a thing:

`implies` · `is a necessary condition for` · `is a sufficient condition for` · `is logically
equivalent to` · `is offered as` · `contrasts with` · `is conceded by` · `is a counterexample
to` · `is raised to rebut` · `is an objection to` · `is a reply to` · `is asserted by` · `is
endorsed by` · `is rejected by` · `is elaborated by` · `is qualified as` · `has commitment`

`is offered as` takes `figurative`, `literal` or `analogy` on the right. `has commitment` takes
`certain`, `probable`, `possible` or `contested`. A thing-level analogy uses `is analogous to`
between things; a thing-level metaphor uses `is a metaphor for`.

## R4 — attribution needs stance

Every `attributed-claim` row F has a row `F | is endorsed by | the author` or `F | is rejected
by | the author` (or `… | is asserted by | <person>` plus one of those). Provenance without
stance is incomplete. Persons are named as persons (`Dennett`), not as citations (`Dennett
1991`); the citation goes to `context` or to a bibliographic row.

## R5 — foils

A claim raised only to be rejected: intention `rebutted-claim` **and** a row `G | is raised to
rebut | F` where G is the author's counter-claim.

## R6 — causation (unchanged)

`is a cause of` / `is the cause of` only for physical or mechanistic causation between events
or processes. Never for entailment (`implies`), constitution (`is constituted by`), realization
(`is realized in`), representation (`is a projection of`), or a rhetorical "therefore". The
dictionary enforces this: the cause must be an occurrence.

## R7 — metaphor and analogy

A metaphor is its own fact plus `F | is offered as | figurative`. Never `is synonymous with`,
`is identical to` or `is classified as a` for a metaphor. A structural comparison is `is
analogous to` (things) or `F | is offered as | analogy` (claims).

## R8 — conditionals and proportionality

"If X then Y", "to the degree that", "only when" are second-order rows between facts
(`implies`, `is a necessary/sufficient condition for`), never a single flat triple.

## R9 — the residual block (new, mandatory)

Everything the section says that cannot be stated under R1–R8 goes to the section's
`gellish-residual` block, one row per item:

```
anchor | category | needed relation | quote
F0031  | rhetorical | is raised as a challenge to | "not a process, but a conclusion"
-      | modality   | may                          | "may be tempted to read this as"
```

`category` ∈ relation-missing · second-order · modality · quantity · temporal · rhetorical ·
other. An empty residual block is a claim that the section was fully encoded — make it
deliberately.

## R10 — internal cross-references (new)

"as argued in Section 4.2", "the table below", "see the appendix", a link to another document: these are the
document talking about itself, and they were lost wholesale when the prose was withheld. Encode them:

```
F0042 | Cognitive Code | is discussed in | Section 4.2 | - | assertion | -
F0043 | epistemic quale table | is listed in | the unified table | - | assertion | -
F0044 | functional decomposition | is set out in | functional_decomposition_raskolnikov.md | - | assertion | -
```

Do not use `cites` / `refers to` for these — that relation is provenance (this document cites another *author's*
work), while R10 is navigation. A cross-reference is not an argument: never let it carry a claim.

## R11 — point of view and appearance (new)

Ontologies remove the subject; this specification puts it back where the text puts it. Two cases, both optional —
use them only where the source itself marks a standpoint, never to editorialise:

1. **A claim that holds only from a standpoint.** If the text says a claim is true *for* a kind of subject, or
   that it looks different from the outside and the inside, index the fact:
   ```
   F0031 | downward causation | is classified as a | illusion | - | assertion | -
   F0032 | F0031 | holds from the point of view of | external observer | - | assertion | -
   F0033 | downward causation | is classified as a | reality | - | assertion | -
   F0034 | F0033 | holds from the point of view of | the Observer itself | - | assertion | -
   ```
   Two rows that contradict each other flatly are an error; the same two rows *indexed to different standpoints*
   are the text's own structure, and the reasoner treats them as a perspectival difference, not a contradiction.
2. **One referent under different guises.** Where the text says the same thing is *experienced as* / *appears as*
   something else to someone, use `appears as` and index it:
   ```
   F0040 | computational residual | appears as | freedom | - | assertion | agency context
   F0041 | F0040 | holds from the point of view of | the Observer itself | - | assertion | -
   ```
   `appears as` is not identity and not classification: it is how a referent shows up for a subject. Use
   `is experienced as` when the text speaks of experience without naming a subject.

The named subject may be a subject *type* from the dictionary (Rationalist, Intuitionist, Language-model subject)
or, more often, whatever the text itself names ("an external observer", "the Observer itself", "a reader with a
folk-psychological vocabulary"). Name it as the text does; do not force it into the three types.

## Hard constraints

- Output only the fenced blocks for the section; no prose, no commentary.
- **Quotes.** A verbatim span from the source is allowed in exactly two places: the right object of a row whose
  relation is `is defined as`, and the `quote` column of a residual row — in both cases wrapped in "double
  quotes". Everywhere else no cell may contain more than 5 consecutive words copied from the source.
- Comment lines inside a block start with an ASCII `#` and nothing else. No other markers.
- Do not assert what the source neither states nor directly entails.
- Completeness over brevity: the table will be large.
