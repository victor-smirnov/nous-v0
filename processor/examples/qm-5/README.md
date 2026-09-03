# qm-5 — superposition and measurement, for a reader of five

The first example with a well-defined truth for every intermediate state, not only the last. An explanation
of a formal subject has what a story has not: a target graph. `target.txt` says which concepts must reach
memory, which may be named only after which, which words must never be named, and which of the forbidden ideas
must nevertheless be *felt* — as mass induced through proxies, without a name.

`profile.txt` is the reader: a Field of 18 words, k = 0.2, memory decaying ×0.7 per chunk, three needs
(understanding, fun, safety), a bucket of games and objects, and two parameters that give concepts a price:
`confusion` (what a concept named without its ground costs understanding) and `comprehension` (what a concept
named on its ground gives it, and therefore what keeps it in memory).

The loop: an explainer writes the chunks → stage 1 names what each chunk names, with word costs → the engine
computes the trajectory → `validate` reads it against the target → the verdict and the trace go back to the
explainer.

## v1

Eight chunks, longest 16 words, no forbidden word, prerequisites in order. Under the model:

| check | result |
|---|---|
| never named a forbidden word | pass |
| prerequisites in place at every naming | pass |
| reached (≥ 0.3 in final memory) | 2 of 6 |
| felt (induced mass in final memory) | 0 of 3 |

Two findings, both about the plan rather than the engine:

- **The memory horizon is two chunks.** A concept named on its ground sits at 0.36; unrepeated, it decays to
  0.25 and then below k. Whatever the last two chunks do not re-cue is gone at the end. Four of six concepts
  were last named in chunks 4–7 and were forgotten by the verdict.
- **The closer displaced the content.** "Fun game, yes?" scores 0.30 on the fun need and evicted "the pattern
  from many tries" and "looking at it", both at 0.29 as carried concepts, from the final Field. The cue meant to
  make the child like the explanation cost the child two of its concepts.

Before `comprehension` existed the run failed everything: concepts that touch no need sit at the floor and
cannot survive a step. That was the run's first lesson and it went into the processor as a rule, not a fix to
the example.

The v1 text, candidates and states are kept under `v1/`.

## v2 — the verdict and the trace went back to the explainer

Told the memory horizon and what the closer had cost, the explainer re-named every concept in the last two
chunks and dropped the fun cue.

| check | v1 | v2 |
|---|---|---|
| never named a forbidden word | pass | pass |
| prerequisites in place | pass | 1 miss |
| reached | 2 / 6 | 4 / 6 |
| felt | 0 / 3 | 2 / 3 |

The one miss is real and the model's own: chunk 7 names *you cannot know which until you look* two chunks after
*both at once* was last named, so the ground is gone; named without it, the concept gets no comprehension, sits
at the floor and is forgotten by the end. The concept that failed to be *felt* (probability amplitude) is the
one whose proxies are exactly the two concepts that failed to be reached. The verdict is consistent with itself.

Two things the run forced into the engine:

- **A chunk is one batch.** The first v2 run reported a second miss — *both at once* named before *looking at it*
  inside chunk 8. That was the engine checking prerequisites in the order the words came, and it contradicts the
  principle everything else here rests on: inside a batch there is no before and after. Fixed; the miss was an
  artefact. One remained.
- **A ceiling report.** Two of the three `must feel` thresholds were above what the profile can produce at all
  (a concept reaches at most `comprehension × weight of understanding` = 0.36, and the induction weights cap
  what its proxies can carry). The validator now says so before anything is run: an infeasible target is a
  finding about the profile, not about the text. The thresholds were brought under the ceiling.

Everything for v2 is under `v2/`.

## v3 — converged

Told the one root cause (a concept named after its ground was forgotten does not stick) and the one budget
fact (a known concept can be re-named in two or three words), the explainer kept *both at once* alive into
chunk 7 and closed with all six concepts in short form, 17 words.

| check | v1 | v2 | v3 |
|---|---|---|---|
| never named a forbidden word | pass | pass | pass |
| prerequisites in place | pass | 1 miss | pass |
| reached | 2 / 6 | 4 / 6 | **6 / 6** |
| felt | 0 / 3 | 2 / 3 | **3 / 3** |

Three iterations of the loop, driven by nothing but the verdict and the trace. That is the fixpoint
optimisation the plan asked for, on the smallest case that has all the parts: a target with intermediate
truth, a profile with a budget and a memory, a nameless component that has to be induced, and an explainer
that never sees the model, only what it measured.

Everything for v3 is under `v3/`.

## Two caveats the run left

- **Short forms are trusted.** v3 closes by re-naming six concepts at three words each. The engine takes a
  short form at the concept's full C, on the explainer's own discipline of keeping every full naming within two
  chunks. It does not check that. A short form of a concept not in memory should be a new unknown token, not a
  re-naming; stage 1 can mark short forms, and the engine can then require the full concept in memory.
- **Stage 1 is not deterministic.** The same chunk-4 clause cost *looking changes it* 7 words in the v2 run and
  11 in the v3 run, and "Count them all" was read as setup in one run and as the pattern's short form in the
  next. The verdicts did not turn on these, but they could. Span-matching of *known* names is a program's job;
  the model should be left with only what is new.

## Running it

```
uv run python -m processor.engine ceiling  examples/qm-5/profile.txt examples/qm-5/target.txt
uv run python -m processor.engine --target examples/qm-5/target.txt examples/qm-5/profile.txt \
    examples/qm-5/engine/step-1.candidates.tsv examples/qm-5/engine/step-1.txt            # then step 2 with step-1.txt as prior, ...
uv run python -m processor.engine validate examples/qm-5/target.txt examples/qm-5/engine/step-{1..8}.txt
```
