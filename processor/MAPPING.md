# MAPPING — from the architecture's state to language, and from language to Datalog

The method: higher-order states, most often projections with distortion, are expressed in a concrete cognitive
architecture; mapped onto language; processed through language; and unloaded, by the same mapping, into
Datalog wherever the mapping is total. This table is that mapping. One row per relation the engine emits.

Columns: what the state says (objective, the analyst's vocabulary) → how it reaches the reader (the
subject's vocabulary, what a report would contain) → the Datalog relation it unloads to, existing in
`nous/gellish/*.dl` or missing. "—" in the reader's column means the relation never reaches the reader by that
name: it is objective, and appears to the reader only through other rows.

## Field of consciousness

| state relation | in the reader's language | in Datalog |
|---|---|---|
| `is in the field of` (item, C, source, cost) | the item, as named; "it came to mind" if associative | `frame` (hot.dl); source and cost missing |
| `attracts` / `repels` (degree word) | "I like / I don't like", by proportion; "very much" when it holds most of the pull | `emotional_signal` sign and share (bootstrap.dl); the degree word is a rendering rule, missing |
| `wants more` (X than Y) | the one comparison the reader can make | missing: a rule over two `emotional_signal` rows |
| `has consciousness components` (count) | "I am torn", "in two minds" | `conflict` (bootstrap.dl) at the level of needs; components by program missing |
| `has tail statistic` intensity / valence / count / spread | "something weighs on me", "vaguely good / bad", "diffuse" | `proto` (hot.dl): intensity, valence, count, spread — total |
| `wants` (images) | "I want X", retrospective, named by images | `reconstructed_cause` (rounds.dl) has the shape; over pull, missing |
| `is surprised by itself` (count) | "I keep surprising myself", a mass | `unfinished_count` (rounds.dl) is the analogue at the level of derivations; over self-prediction, missing |
| `notices about itself` (kind) | "I forgot", "it came to me", "I got pulled away", "I lost the thread" | `self_model` (rounds.dl) has the shape; the kinds are missing |

## Motor field

| state relation | in the reader's language | in Datalog |
|---|---|---|
| `does` (reads on / acts on need) | "I went on reading", "I went to get lunch" | `recommend` / `acted` (rounds.dl): the rules decide, the wrapper executes — total |
| `attends to` (reality / fantasy; yields) | "I was daydreaming", "I snapped back" | missing: a rule comparing two yields; the rounds wrapper can carry both |

## Long-term memory

| state relation | in the reader's language | in Datalog |
|---|---|---|
| `is in memory of` (item, C, cost) | "I remember", if asked; not spontaneously | `settled` (rounds.dl) is the persistence mechanism; decay and the consolidated floor missing |
| `has pulled` (item, carried) | — (the material of `wants`) | missing |
| `has satisfaction delta` (installed path) | "I found out that X costs / gives Y" | `delta` (bootstrap.dl) — total; the "understood" path is `delta` to understanding |

## Need portrait (objective)

| state relation | in the reader's language | in Datalog |
|---|---|---|
| `has satisfaction level` (need) | — | `need_of` weight (bootstrap.dl) is static; levels and their dynamics missing |
| `is classified as a` (class) | — | dictionary: the Gellish taxonomy — total once the classes are concepts |
| active needs (trace) | — | `active_need` (bootstrap.dl) — total; the necessary-or-reachable rule missing |
| `has dominant need` (program, switches) | "I was busy with", only retrospectively and by images | missing: an argmax over need mass in `frame` |
| `has conflict level` (runner-up / leader) | "torn", "on the fence" | `conflict`, `anguish` (bootstrap.dl) are the need-level forms; the program-level ratio missing |
| `has met self-surprise` (kind, count) | — | missing |
| `has items at control levels` (L0–L6) | — | `frame` ∪ `tail` give L1/L2/L4; `unconscious_fact` L1; `represented_fact` L4; understood L5 and self-names L6 missing; **L3 not representable in either** |

## Field of mind (blackboard, analyst's)

| state relation | in the reader's language | in Datalog |
|---|---|---|
| evicted (item, C, why) | — | `tail` (hot.dl) — total; the reason (no room / below k) missing |
| candidates and their arithmetic | — | the body of every rule: total by construction |

## What the table says

- The **reader's column is where the phenomenology lives**, and it is small: a dozen forms, all of them
  comparative, retrospective or diffuse, none of them a number, none of them a need. That is what an LLM has
  learned from language; it is also what the oracle should be asked to render, and nothing else.
- The **Datalog column is mostly total or one rule away.** What is missing splits cleanly: renderings (degree
  words, comparisons), and dynamics between batches (levels, decay, yields, self-prediction). The renderings are
  rules over existing relations. The dynamics belong to the rounds wrapper, which is where they already live for
  the reflexive exhibits.
- **Level 3** — a recallable memory without a name — is missing in both columns. It is the one representational
  gap the architecture has, and the place the multiscale extension enters.
