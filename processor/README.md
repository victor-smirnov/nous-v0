# The state processor — phase 1

A processor of states of consciousness, implemented as instructions to a language model. Phase 1 of three:

1. **This.** The processor is an LLM following `PROCESSOR.md`; pre- and post-processing may be ordinary programs;
   sub-agents evaluate. Worked up on micro-examples, then on the opening of "Die Verwandlung".
2. The same, with the reasoning about states unloaded into Datalog (`nous/gellish/hot.dl` already holds the
   target relations: frame, tail, proto, displacement).
3. Residuum: a novel written entirely by an LLM using that unloaded reasoning.

## What a state is

A reader has a **Field** (Поле Сознания) of bounded volume, a **memory**, and a **tail**. Every signal the reader
could be aware of carries a degree of awareness C in [0, 1): 0 is a fully unconscious process, 1 is excluded
because nothing is ever fully represented. The Field holds the signals with C above a threshold k — these have
*names*; the rest reach the reader only as aggregates keyed by nothing but the reader: intensity, valence,
spread. That nameless remainder is the tail, and it is the protopathic component of the state.

Two things fill the Field at every step, and they compete for the same budget:

- **sensory** — what the current chunk of text names;
- **associative** — what memory drags in, cued by the named signals ("the bucket").

The budget is measured in words for now (bits later). The text pays for cues; the bucket delivers the rest.

## The architecture

The state is written in six parts, one per component of the cognitive architecture:

| component | in the engine |
|---|---|
| sensory field (receptors) | the stage-1 candidates: what the chunk names, at what cost in words |
| motor field (effectors) | the one continuation: the leading program's action; a chunk arriving while the motor field is elsewhere is not received |
| field of mind (blackboard) | every candidate of the step — sensory, carried, associative — with a name, not conscious |
| field of consciousness | the cut of the field of mind by k and by budget; non-unitary: its components are the items grouped by the need each answers to |
| long-term memory | what persists, decaying, with consolidated prior knowledge as a floor |
| need portrait | objective, in its own vocabulary: needs with class, priority, satisfaction level; the active subset; the program; the conflict level. Reaches the reader only as the pull of images and a retrospective `wants` |
| model of the environment | the paths, associations and prerequisites, run instead of the text: the second set of interfaces. The channel attends to reality or to the model by reinforcement — which pays better now |
| model of the self | the reader's prediction of its own next state, and the difference from what happened, sorted by kind; recurring kinds become the reader's names for itself |

The model — a language model, or the engine — computes the dynamics by the rules. The content of the field of
consciousness is never written; it is derived from the state of the whole.

None of what the engine does is absent from language; deficits, satiation, the pull of images, the lag of the
retrospective report are all in the statistics a language model has learned, dispersed. What the engine adds is
not a mechanism the model lacks but a form in which those dispersed elements are gathered into one context and
become continuable — and, once unloaded into rules, stay gathered without depending on where attention happens
to fall. Knowledge is not what is scarce here; attention is.

## Two levels, for now

"Mass without a name" is a two-level case of a multiscale representation: an item is held either as its name
(the leaf) or as its contribution to the tail's aggregates (the root), and nothing in between. The general form
would hold each item at some level of the generality hierarchy (`is a specialization of`, which the Gellish
dictionary already has), with the cost of holding growing with resolution — bits to tell the item from its
alternatives in the current context — and the response aggregating upward, so that the tail statistics are
simply the response at the root. Filling the Field would then coarsen and merge rather than evict, and the
resolution required would be set by what the leading program has to decide.

There is no effective formula yet for the cost of a representation at a given detail, so the engine stays at
two levels. Two properties are kept so the levels can be added without rebuilding: the cost of holding is a
column of its own, separate from what the text spent in words; and the response aggregates upward by sum.

## The contract

Input, per step:

| item | form |
|---|---|
| reader profile | needs with weights, an association table (cue → item, weight), threshold k, budget B in words |
| prior state | the Field, the memory (item, C), the tail statistics — all as fact rows |
| chunk | the next span of text, verbatim |

Output, per step, all as fact rows in the case-file format (`F#### | left | relation | right | value | intent | note`):

| relation | meaning |
|---|---|
| `is in the field of` | item is named for the reader; value = C; note says `sensory`, `carried` or `associative via <cue>`, and the word cost |
| `is in memory of` | item persists with value = C (decayed if not republished) |
| `has tail statistic` | left = reader, right = `intensity` / `valence` / `spread` / `count`, value = number |
| `has satisfaction delta` | new signal the chunk established (a path a later chunk can use) |

Evictions are not state: they go in a trace block after it, the analyst's view, which may name what the
state may not.

Invariants the evaluator checks:

1. The Field's word cost never exceeds B.
2. Nothing in the tail is named. If a tail-only target appears with a name, the step failed.
3. Every associative item has a cue that is itself in the Field or was in the previous Field.
4. Memory decays: an item not republished loses C by the profile's decay; at C below k it leaves memory.
5. Determinism under repetition and movement under perturbation: the same input twice gives the same Field;
   swapping which need is heavy moves the eviction.

## Division of labour

Of the seven stages in `PROCESSOR.md`, only two need a language model: naming the signals a chunk contains
with their word cost (stage 1), and noticing that a chunk installs a cost relation the reader did not have
(stage 7). Association, scoring, filling the Field, the tail statistics and memory (stages 2–6) are arithmetic
over the profile and the prior state, and `engine.py` does them. `STAGE1.md` is the instruction for the LLM
part alone. That boundary is where phase 2 unloads: what the engine computes is what `nous/gellish/hot.dl`
will compute; what stage 1 produces is a case file.

Running the full `PROCESSOR.md` through a model and the split pipeline side by side is itself a test: on
micro-1 the engine reproduced the model's three states exactly, given the model's own stage-1 candidates.

## What micro-1 showed

Three sentences, one reader whose memory holds that an alarm clock means being late and being late means the
boss. By the third sentence the Field is occupied by *being late* and *the boss*, neither of which the text
names, and the sentence's own content — rain — is evicted and reaches the reader only as tail mass. The bucket
ate the budget out from under the sensory input. That is the mechanism, in the smallest case that has it.

Two rules were forced by the run rather than designed: the state block and the trace block are separate
because an eviction row would otherwise name a tail member (found by the evaluator on step 3); and nothing
below k is admitted whatever the budget, because the Field is defined by k, not by room.

## qm-5: the first example with a truth for every step

An explanation of a formal subject has a target graph: which concepts must reach memory, in what order, which
words must never be named, and which forbidden ideas must nevertheless be felt through proxies. That fixes
the truth of every intermediate state, not only the last, so the evaluator no longer has to trust an encoding.
`examples/qm-5/` runs the loop explainer → stage 1 → engine → `validate` → verdict back to the explainer on
"superposition and measurement for a reader of five". Three iterations took it from 2 of 6 concepts reached
to 6 of 6, and every rule the run forced (comprehension as the need concepts satisfy, a chunk as one batch, a
ceiling report for infeasible targets) went into the engine, not into the example. See its README.

`examples/quad-8/` adds prior knowledge: the reader arrives with concepts in memory, and the target's
prerequisites point at them. Its first run failed on the engine, not the text — consolidated memory was
decaying like working memory, a mention was resetting a known concept to the floor, and one large item was
blocking small ones that had room — and the three fixes are checked against qm-5, whose verdicts did not move.

`examples/algo-8/` (the concept of an algorithm, for a reader of eight) forced two more: an understood concept
is held in the Field at the size of its name, not of the words that introduced it, and `ceiling` bounds what
any final chunk can leave. It also produced the first divergence between model and reader: told that familiar
examples outbid a new concept, the explainer removed every analogy, and the model scored the result higher
while a child would do worse. The engine has no rule by which an example grounds a concept, only the rule by
which it competes for the Field. That gap is recorded, not patched.

The **need portrait** (classes, priorities, satisfaction levels with dynamics) is in the engine and tried on
algo-8 with a fed and a hungry child: the hungry one does worse on the text built on a sandwich and the same
on the text without food. Under the portrait no text passes the thresholds that were set against a static
ceiling, which is the open question it leaves: with dynamic weights, absolute thresholds on C are the wrong
instrument. See algo-8's README.

## Layout

```
processor/
  README.md          this
  PROCESSOR.md       the full instructions, all seven stages, for running a model end to end
  STAGE1.md          the instructions for the two stages only a model can do
  EVALUATOR.md       the instructions the evaluating sub-agent runs
  engine.py          stages 2–6 as a program
  examples/
    algo-8/          an algorithm for a reader of eight: v1 with analogies, v2 without, README.md
    quad-8/          quadratic equations for the eighth grade: prior knowledge in memory, README.md
    qm-5/            target.txt, profile.txt, text.txt, v1/ v2/ v3/, README.md
    micro-1/         profile.txt, text.txt
      states/        the model's end-to-end states, one per step
      eval/          the evaluator's reports on them
      engine/        stage-1 candidates and the engine's states
```
