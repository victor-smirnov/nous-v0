# Plan: the reasoner as a standalone project and a Claude (then Codex) skill

Goal (Victor, 2026-08-29): a tool + skill for *unloading* reasoning from prose into ontological
structure (Gellish) and *loading it back*: prose → hybrid prose+Gellish document → pipeline
(consistency, enrichment, …) → optionally prose again. First real use: article v2 of
`docs/what_is_it_like_to_be_a_language_model.md`.

## 1. Shape of the product

Three layers, each usable without the next:

| layer | what | who runs it |
|---|---|---|
| **core** (deterministic) | dictionary build, parse, Soufflé closure, checks, enrichment export, provenance, diff | scripts, no model |
| **skill** (LLM-driven) | encode prose → hybrid doc; repair loop over reasoner findings; decode hybrid → prose | Claude / Codex following the skill's specs |
| **domain dictionaries** | Gellish standard + field extensions (`philosophy_of_mind`) + project theories (`synthea_bootstrap`) | live with their projects, plugged in by path |

The **hybrid document** is the central artifact: Markdown with the prose shell kept (addressee,
modality, first person — what the round-trip study showed Gellish cannot carry) and one fenced
```gellish``` block per section holding the v3 table. Fact UIDs are document-global
(`S3:F0012` — section 3). A hybrid doc is at once readable, diffable, and machine-checkable.

## 2. Repository: `nous-v0`, package `nous` (M1 done 2026-08-29)

```
nous-v0/
  nous/cli.py            `nous gellish build-dict | check | ask | why | report`  (+ enrich | diff | extract | inject — M3)
  nous/gellish/          dictionary.py  parse.py  reasoner.dl  run.py  report.py  ask.py  why.py  paths.py
  nous/gellish/ext/builder.py   the extension builder
  ext/<name>/spec.py     philosophy_of_mind (field, neutral) and synthea_bootstrap (the theory) — both live here
  bootstrap/             Synthea bootstrap 01–06 (source of synthea_bootstrap)
  data/                  gellish.net release + Soufflé export (git-ignored; build-dict --fetch)
  work/                  per-run facts/out/prov (git-ignored)
  spec/                  hybrid-format.md, encoding-v3.md, decoding.md, phrases.md (generated)
  .claude/skills/gellish/   the Claude skill (SKILL.md + references → spec/); symlinked into ~/.claude/skills
  tests/                 golden regression on tables/article-v1
```

Soufflé is a runtime dependency, checked at startup with a clear message.

CLI contract (all deterministic):
- `gellish check doc.md [--theory off|hypothesis|doctrine] [--ext DIR…]` → `out/` + REPORT.md
- `gellish enrich doc.md` → `doc.enriched.md` (derived rows appended with provenance; top-cut; definitions)
- `gellish why doc.md <relation> [filters…]` → proof trees
- `gellish diff a.md b.md` → semantic diff of the two closures (added / removed / level-changed edges)
- `gellish extract doc.md` → bare tables; `gellish inject doc.md tables/` → hybrid doc

## 3. The skill

`skill/SKILL.md` (frontmatter: name `gellish`, description, user-invocable) with subcommands
expressed as workflows for the model:

- `/gellish encode <file>` — chunk by section; for each section produce the ```gellish``` block
  under `spec/encoding-v3.md`, with the dictionary phrase list (generated from `dictfacts`,
  ~3 300 phrases grouped by family) in context; residual goes to a mandatory `untranslatable`
  list, never to invented phrases. Output: hybrid doc.
- `/gellish check <doc>` — runs the CLI, then *reads* REPORT.md and `why` output and proposes
  repairs: classify each finding as encoder error (fix the table), source inconsistency (flag
  in prose with a marker), or theory disagreement (`--theory` diff). Repairs are edits to the
  ```gellish``` blocks; re-run until clean or every remaining finding is annotated.
- `/gellish enrich <doc>` — CLI export, then the model reviews derived rows and drops noise the
  top-cut missed.
- `/gellish decode <doc>` — per section, prose from table + shell under `spec/decoding.md`:
  use second-order rows to choose register (hedge, attribute, mark figurative), never narrate
  them; keep the prose shell verbatim where it carries addressee/modality.
- `/gellish roundtrip <file>` — encode → check → enrich → decode, with the existing judges
  (first-order fidelity, second-order inversion probe) run on demand.

`references/` holds the specs and the phrase list; `scripts/` the CLI wrappers. Codex later:
same scripts, instructions moved into `AGENTS.md` / its skills directory — the deterministic
core is identical, only the prompt container changes.

## 4. Spec v3 (what changes vs v2, all from measured findings)

1. **Positive-proposition rule.** The triple always states the positive proposition;
   `denial` negates it. Negative phrasing (`cannot`, `lacks`, `is not`) with `denial` is an error.
2. **Second-order relations only over fact UIDs.** `is offered as`, `is endorsed by`, …
   require a `S#:F#` on the left.
3. **Dictionary in the contract.** The encoder receives the phrase list and must use it;
   anything else goes to `untranslatable` as `(anchor F#, category, needed relation, quote)`.
4. **Section anchoring + global UIDs**, so cross-section references and diffs work.
5. **Persons and works as individuals**, cited as `Dennett 1991` → alias rows or the people
   dictionary; no citation strings in the object columns.
6. Keep from v2: mandatory intention enum, reification, `is a cause of` ban (now enforced by
   Gellish 1922 roles), figurative rows.

## 4b. Spec v3.1 backlog (from the article run, 2026-08-29)

- Internal cross-references: a row type or residual category for "(Section 4.2)" / document links — C lost all of them.
- Reconcile "≤ 5 consecutive source words" with quoted definitions: quotes allowed only in `is defined as` and residual `quote`.
- (Dropped, Victor 2026-08-29: style/register is a separate channel, its loss through the ontology is expected and
  desirable. Decode C is the intended behaviour.) A rows-vs-prose *first-order* self-check before returning may still be useful.
- Encoders write unicode comment markers («, ＃) and occasionally truncate the first row — assembler now normalises; spec
  should say ASCII `#` only.
- Enrichment output is for review, not for decoding; document in decoding.md (done) and in enrich --for-review default.

## 5. Article v2 — the first run (work lives in `experiments/article/`, git-ignored; moves to Synthea later)

1. Chunk `docs/what_is_it_like_to_be_a_language_model.md` by section (≈ the 9 chunks used before, but section-aligned).
2. Encode with the v3 spec, Opus (the cost study found amplified Opus dominant); result: `article.hybrid.md`.
3. `check --theory off` (does the article contradict itself?) and `check --theory doctrine
   --ext synthea` (**does the article agree with the bootstrap?** — this is the first time the
   article can be checked against its own theory mechanically).
4. Repair loop with `why`; every surviving finding becomes a footnote in the prose.
5. `enrich` → `article.enriched.md`; review derived rows.
6. `decode` → `article-v2.md`; judge against v1 with the v2-experiment judges; the
   inversion probe is the acceptance metric (target: inversion mass below the v2 experiment's 785).
7. Keep both: the hybrid doc is the *source of truth* from now on; prose is a rendering.

## 8. Order of work and effort

| milestone | content | effort |
|---|---|---|
| M1 | extract repo, package, CLI, golden tests, Soufflé check | done 2026-08-29 |
| M2 | hybrid format, spec v3, phrase list generator, skill (encode/check/decode) | done 2026-08-29 |
| M3 | enrich export (top-cut, definitions, provenance column), diff, decode spec | done 2026-08-29 |
| M4 | article run: encode → check → repair → enrich → decode → judge | done 2026-08-29 (A/B/C decodes; report in experiments/article/REPORT.md) |
| M5 | thesis stratum + `summarize`; subjectivity layer (subject types, graded capacity, seen-as) | done 2026-08-29 |
| M6 | spec v3.1 (§4b) + subject rows in the encoder contract; re-encode | ~1 day + model time |
| M7 | Codex port | ½ day |

## 9. Decisions to confirm

- ~~Repo name~~ `nous-v0`, package `nous`, MIT. Both dictionaries live here.
- Encoding model for the article run: Opus (cost study) — unless Fable is preferred for frugality.
- ~~Hybrid container~~ fences (done).

## 6b. The bootstrap as a Datalog library (Victor, 2026-08-31)

The goal is not to record the bootstrap as facts about a theory but to make it **executable**: a library that,
in batch, reasons about Observer states in a concrete context. Declarative subjectivity (subject types, graded
capacity, point of view, seen-as) was the first slice; the dynamics are `nous/gellish/bootstrap.dl` — see
`spec/bootstrap-library.md`. Done in the first slice: the Observer stack with its three conditions and the
missing-condition diagnosis, emotions as signals of *active* needs with weights and valence, motivational
conflict and the Observer manifesting on it, the residual's projection into an epistemic quale selected by the
active context, functional deficits from substrate facts, self-reports of limits recognised as HOCP.
Still to write: the cognitive cycle's phases, the four-level memory and channel salience with weighted
injection, forward simulation, cognitive resistance / narrative inertia, the psychosemantic bridge tied to the
subject layer's capacities, and non-renewable psychological needs driving novelty-seeking.

## 7. Receiver profiles (direction, 2026-08-29; not detailed yet)

Victor: the difficulty of the hard problem is less how to explain consciousness than how the explanation is
*understood* — it needs a ready conceptual apparatus; people are unaware of their own limitation and there is no
fast way to make them aware. So a "philosophy-of-mind ontology" as one academic artifact is the wrong shape: it will
be a set of partial descriptions built for different levels of intrapersonal intelligence, and the work must start
from that. Focus on three receivers:

1. modern rational person with a Western humanities education (inclined to intuitionism);
2. the same with a technical education (aimed at reductionism);
3. a language model.

Mapping onto the tool:
- a receiver profile is a *dictionary*: the concepts and relation families the receiver already owns
  (`ext/receiver_*`); grounding a document against it lists what is OOD for that receiver — for the LLM this is the
  existing Gellish + field grounding (the article's 221 own concepts are its OOD);
- comprehensibility is *explanatory path length* from the receiver's known concepts to the document's own ones
  (the thesis stratum reversed); missing bridges are what a rendering must add;
- each profile weights bridge kinds: analogy/phenomenology for (1), mechanism/reduction for (2), explicit
  definitions and both for (3);
- decode per profile = one checked ontology, three renderings (the "receiver-profile personalization" middle-end
  of the amplifier plan).
Judges then measure per profile: first-order fidelity as now, plus a comprehension probe — can a reader with that
profile reconstruct the hub from the rendering.

---

# Phase 1: composition of the basic functions of consciousness (Victor, 2026-08-31)

The programme this phase serves, as Victor stated it: build a case base of characteristic texts; encode them
into the ontology; enrich the logical model with material about the actor's behaviour and state; analyse and
improve the library, paying particular attention to the **composition** of complex functions out of simple
ones; render back to prose. Phase 2 turns the resulting library back into prose, and that is article V3 — whose
point is exactly the principle V1/V2 only gesture at: **complex states of consciousness as situational
combinations of basic ones.**

What is deliberately NOT pursued: functionality. The batch engine plus small superstructures is the whole
substrate for the proof-of-concept. Batch vs incremental is a difference of **granularity, not of kind** — the
Observer's time is quantised by the batch, and Deem will shrink the quantum, not supply a function that is
missing here. The coarse quantum is what makes composition visible to the naked eye, which is why an FCRS at
this scale was chosen. Chasing capability blurs the only thing being demonstrated.

## Acceptance criteria

Thresholds marked (prov.) are mine, not confirmed.

**1. Unloading prose into the ontology.** There is no ground truth for "the logical structure of prose", so the
criterion is reproducibility plus the absence of silent loss: two *independent* encodings of one text align
above threshold; everything untranslated sits in the mandatory residual block; closure runs with no
contradictions and no violations. Threshold: 85% of entities, 70% of facts (prov.). Never yet measured — the
aligner has only been run across *different* texts. Cheapest missing measurement; do it first.
*Have:* the article closes 0 contradictions / 0 violations / 0 calibration tensions.
*Normal negative result:* low inter-encoder agreement with an honestly declared residual.

**2. Formal reasoning with HOCP over a sequence of batches.** The reasoner must derive a statement *about
itself* that appears nowhere in its input, is false under different parameters, and **changes what it does
next**; the level transition must be driven by the rules, not the wrapper.
*Have:* `truncated` → `self_conclusion` → `recommend` → raised budget, and the Agent→Observer transition at
`--maxdepth 1`. Missing: nothing is at stake — registration without need. Completing test: a paired run with
and without a need must differ in level.
*Failure:* the level is the same, i.e. the need is decorative.

**3. Functional composition — the centre.** Per composite state, four conditions:
- **discrimination** — a pair of cases the source distinguishes comes out different, and different the right way;
- **ablation** — remove one basic function and the composite disappears, and the right one disappears;
- **derivation depth ≥ 2** — the composite rests on derived premises, not asserted ones;
- **legibility** — the derivation chain reads on one page, by a human, without running the tool. If understanding
  the composition requires executing the program, the scale is wrong and FCRS was pointless.

Threshold: five composite states passing all four (prov.). A small set that passes is worth more than a large
set that does not.
*Have:* one — the fractured moral stack (adult/child discrimination, `means_conflict` empty, regression test on
the `sys-C`/`sys-D` pair).

**4. Loading back into prose by independent rules.** The danger is a decoder that is an LLM reading the ontology
and writing good prose, which would demonstrate nothing. The criterion that excludes it is the **closed loop**:
`encode(decode(O)) ≈ O`. Threshold: round-trip loss no greater than the inter-encoder noise measured in (1) —
better than an arbitrary number. Style is excluded by prior decision (a separate channel).
*Have:* V2 — 734/739 sentences verbatim, 5 accepted changes out of 34 proposed. The loop has never been closed.

**5. "Normal for a human" — rescoped.** No respected benchmark for this capability exists, and building our own
would defeat the purpose. If this work *triggers an independent party to build one*, that is the larger success.
Designing for that inverts the usual priorities:

- the most valuable artifact is the **failure profile of the bare-LLM baseline**, not our positive result. A
  benchmark gets built because something visibly breaks and nothing existing measures it. A loud claim of our own
  success works *against* the trigger: it invites argument with us instead of measurement of the phenomenon.
- **independence must be structural.** Items phrased in Gellish or in Synthea's vocabulary can only be scored by
  us. Item wording must be plain language answerable by anyone who read the text; our contribution is the item
  *schema* (which dimension is measured), and the case base must be assumed replaceable.
- **release cases without answers.** Our predictions are generated and sealed *before* any human data exists, and
  kept separate. Pre-registration is the substitute for a benchmark when there is none.
- **size.** A crisp name for the capability, a few vivid failing examples, zero friction to reproduce. Not forty
  pages.
- **stated in advance:** the framework predicts we hit structure and direction and systematically miss intensity
  and urgency, because the machine has no anxiety. A hit on intensity is evidence *against* the substrate-asymmetry
  claim, not a triumph.
- **the honesty condition:** an independent benchmark may show the ontology adds nothing. If that outcome is
  unacceptable to us, we must not invite an independent party. It is declared normal in advance.

Phase-1 acceptance for (5): a published task statement in neutral terms, a documented baseline failure profile,
cases without answers, and our sealed predictions. Success = this suffices for the task to be measured without us.

Before asserting no benchmark exists, check — theory-of-mind, social-inference and emotion-prediction sets do
exist; what appears absent is measurement of *state dynamics under motivational conflict with compositional
structure*. A day of literature check pays for itself, and a negative finding is itself presentable.

**Free partial answer key: the canon.** For a canonical text the author supplies the continuation — the machine
predicts from Part 1's encoding, the novel says what happened. Out-of-sample behavioural prediction with an
uncontestable key, at zero cost. Caveat, to be reported per case: models have memorised the plot. But so has the
baseline, and the baseline is our control — so contamination biases *against* us and a win is conservative. Include
some material outside the training distribution regardless.

**Organisation:** (1)–(4) are self-contained and defensible without human subjects and close Phase 1; (5) carries
its own gate in Phase 2, so a failure there does not retroactively devalue (1)–(4).

**The one abnormal result:** moving a criterion after seeing the number.

## Modules, sorted by the composition rule

Kept — each demonstrates composition:
- **Observer derived from compression under a prediction requirement.** The load-bearing one: a basic function
  stops being written in by the encoder and starts being computed. Definition: the agentive model (needs, goals,
  a decision rule; length independent of the determinant count) is a lossy compression of the extensional model
  (determinant → behaviour). Causal independence is the hypothesis minimising the description length of a
  predictively adequate model. The *need* for causal analysis arises when prediction of A is required **and** the
  extensional model is inaccessible or unaffordable. This absorbs the determinant module rather than adding to it,
  and it retires the shortcut in which the Encounter condition was asserted.
- **Determinants with per-standpoint graded access.** Required by the above; also yields the motive.
- **Motive as a need at a fork indexed by the subject.** Composition in its purest form: three existing layers,
  a new name on the output. Needs are objective — what the system must do; motives are situational and exist only
  as forks, i.e. for the Observer. `("motivation", "is a projection of", "need")` is already in the bootstrap's
  FACTS; the missing content was the mechanism of projection, which is the fork. Guard: motives are real
  *relative to a standpoint* — the alternative reading ("only needs are real") is the eliminativism the framework
  rejects.

Deferred — capability, not composition:
- plans as objects with steps and per-step channel collisions (a case may simply state whether a plan exists);
- anxiety with accumulation over rounds and a threshold function (show the structure, tune nothing);
- MDL with a fixed description language and measured code lengths (the definition is what does the work; use a
  proxy and call it one);
- recovering the catalogue of human cognitive biases (Phase 2 empirics, outside the proof-of-concept).

## MDL measured with a language model

A language model *is* a compressor: negative log-likelihood is code length. So the arbitrary description language
becomes a **named, pinned checkpoint** — more honest than hand-picking a formalism.

- **Meter, not decider.** The model returns a scalar in bits. The rule comparing two lengths and concluding causal
  independence is in Datalog. The model is never asked about agency, causation or freedom; it only assigns
  probability to strings. Use *scoring* of fixed strings we author, not *generation* — generation is judgement, and
  judgement leaks the conclusion out of the symbolic layer.
- **Two-part code, or the result is vacuous:** `L(model) + L(data | model)`. Comparing only the first term makes the
  agentive model win trivially because it is shorter. The claim is that it is shorter *while remaining predictively
  adequate*, and the second term is measurable the same way — the surprisal of the agent's observed behaviour given
  the model description as context.
- **The acceptance experiment is a crossover: thermostat vs Raskolnikov.** Few determinants, all visible → the
  extensional model must win. Many, partly inaccessible → the agentive model must win. If the agentive model wins on
  the thermostat, the measure is broken and nothing is demonstrated. Two points, one number, the whole thesis.
- Descriptions follow a **fixed template**; logprobs are sensitive to surface form and two phrasings of one model
  diverge by hundreds of bits. Perturb the phrasing and require the *ordering* to hold — compare the sign of the
  difference, never its magnitude.
- **Two roles, kept apart by name.** Phase 1: meter of code length, passes no judgement. Phase 2: proxy for the
  human prior ("what a human finds surprising") — legitimate, because there it models the *target* of prediction
  rather than producing the inference. Conflating them hands a critic the claim that the LLM did everything.

## Distortion analysis: systematic vs not

"The distortions are stable and systematic" is a **hypothesis**, and separating systematic from incidental is its
own stage. Systematic means *attributable to the heuristic* — not to the case, and not to the encoder. Two axes:

- **vary the case, hold the heuristic** — the distortion must recur in direction and shape across independent
  cases, else it is idiosyncratic to content;
- **vary the heuristic, hold the case** — the distortion must vanish or change shape. This is the decisive control.
  Stable along *both* axes means it belongs to the encoding, not the approximation — the failure mode that would
  quietly kill the argument, because it looks like the most convincing result of all.

**Determinism masquerading as systematicity is the main trap.** A batch reasoner reproduces its own arbitrary
tie-breaks perfectly, and any "take the strongest" heuristic bottoms out in a tie-break that runs on entity names.
Re-running the same input confirms every artifact. So stability is measured **under perturbation, not under
repetition**: permute row order, rename entities, and see whether the distortion moves. Cheap, decisive, and it goes
first, before any interpretation.

Encoder artifacts are caught by independent re-encoding plus the aligner — built for coverage, and it turns out to
be the control here.

**Deviation must be measured against something.** The strict form is not the baseline: on these queries it is
*silent*, which is why we approximate at all. So a calibration set is needed whose cases are small enough for the
exhaustive multi-model computation to be feasible, where deviation is measurable exactly. Raskolnikov is that size:
six determinants, 64 subsets, the whole ablation matrix. Heuristics are calibrated where truth exists, then applied
where brute force is impossible.

**Approximations are rules, not calls** — the same division of labour as `rounds.dl`: the rules decide, the wrapper
executes. A finite, named, inspectable set, each with a known failure mode: take the strongest grounding rather than
none; complete a truncated chain as if it had terminated; close the world within a bounded scope; prefer the
explanation with the fewest determinants. If an LLM adjudicates, the demonstration collapses into "an LLM did it".

*Declared in advance:* three surviving distortions rather than thirty is a normal result. A small set that survived
all four controls is worth more to the argument than a large set that did not.
