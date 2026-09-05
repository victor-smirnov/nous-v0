# algo-8 — the concept of an algorithm, for a reader of eight

Eight concepts (steps in order, exactness, repeatability, termination, following without understanding, the
name itself, a computer only follows algorithms, a bug), prior knowledge of instructions, recipes, games and
machines already in memory, six forbidden names, three ideas to be felt: a Turing machine through "anyone can
follow it without knowing why", the halting problem through "it must come to an end", formal semantics through
"every step must be exact".

The reader: a Field of 24 words, memory decaying ×0.75, needs in which fun and doing-it-myself weigh nearly as
much as understanding, and a bucket in which *a robot* drags in *a silly robot* and *a computer* drags in
*a game*.

## v1 — the familiar outbids the new

Nine chunks built on teeth, a sandwich and a silly robot. Under the model, 3 of 8 reached, 2 of 3 felt, three
prerequisite misses, all downstream of one event: in chunk 6 the name *an algorithm* did not enter the Field.
The chunk re-activated *making a sandwich* (memory 0.40) and *a robot* and dragged in *a silly robot*; a newly
understood concept scores 0.36, the familiar things the child already holds score at their memory strength and
win the room. The name never reached memory, and every later mention of it was an unknown token.

That is a real effect of the model and probably of children: the example is more vivid than the thing it
exemplifies. It is also the model's blind spot, see below.

## v2 — the explainer removed every analogy

Told the root cause, the explainer stripped out teeth, sandwich and robot entirely and wrote ten chunks of
pure structure. The model pushed it there: analogies have a price in this engine and no benefit. A real
eight-year-old would do worse with v2 than with v1. The engine has no rule by which a familiar example
*grounds* a new concept — carries part of its comprehension, or lowers its cost — only the rule by which it
competes for the Field. That is the next thing this example asks for, and it is not added here because it was
not forced by a measurement; it is a hypothesis.

The first v2 run came out worse than v1 (2 of 8), and that failure was the engine's, the second such since
qm-5:

- **Words buy cues; the Field holds items.** Stage 1 charges an introducing chunk's words to the concept it
  introduces — 22 of 24 for *an algorithm* — and the engine was taking that as the concept's size in the Field
  and carrying it forward. A concept the reader has understood is now held at the size of its *name*, however
  many words it took to introduce. Comprehension is compression; what is not understood stays at the words it
  cost. Under that rule v1 rose to 4 of 8 (the name now fits) and v2 to 4 of 8 with the four foundational
  concepts at 0.27–0.29, one chunk old.
- **The last Field has a capacity.** Eight names cost 38 words; the Field holds 24; a concept one chunk old is
  worth 0.36 × 0.75 = 0.27. So at a threshold of 0.3 the target was infeasible for any text, and the explainer
  had said as much in its own notes. `ceiling` now reports this before a run. The thresholds were set to 0.25,
  which means "named in the last two chunks", and v2 passes 13 of 13.

Both controls hold under the new engine: qm-5 v3 11 of 11, quad-8 13 of 13.

| check | v1 | v2 |
|---|---|---|
| never named | pass | pass |
| prerequisites in place | 1 miss | pass |
| reached (≥ 0.25) | 4 / 8 | **8 / 8** |
| felt | 2 / 3 | **3 / 3** |

## What this example adds to the method

Two engine rules with reasons independent of the example (compression on comprehension; a capacity bound
on the final Field), one explicit gap (analogies only cost), and a clean instance of the loop making a text
*worse for the reader while better for the model* — the first time the two came apart, and the kind of
divergence the whole apparatus exists to make visible rather than to hide.

v1 under `v1/`, v2 under `v2/`.

## The need portrait — a first run

`profile-fed.txt` and `profile-hungry.txt` are the same child with a **need portrait**: each need has a class
(basal, psychophysiological, psychological), a class priority, and a satisfaction level whose deficit is its
weight. Safety is basal and satisfied, so it weighs nothing at home. Hunger is psychophysiological; a sandwich,
lunch and a cake pull on it. The emotional response of a candidate is Σ delta × weight over its signals, and
that is its C — what decides admission to the Field and rank within it. What is new in the Field moves the
levels; between steps they drift back to baseline; understanding is fed once per concept, when it is grasped.

| | v1 (with analogies) | v2 (without) |
|---|---|---|
| fed | 7 / 13 | 8 / 13 |
| hungry | **5 / 13** | 8 / 13 |

The hungry child does worse on the text built on a sandwich and does exactly as well as the fed one on the text
without food in it. "No lunch, ever" in chunk 4 pulls at 0.34 when hungry and sits at the floor when fed, and
what it displaces is a concept. That is the portrait doing what it was introduced to do: the cost of an analogy
depends on the state of the need it touches.

Three engine rules came out of getting here, all of the same kind — a level must move on **events**, not on
presence: holding a thought does not feed a need twice; a concept feeds understanding once, when it is grasped;
and the comprehension path is reader state, written to the state file, or every step forgets that the concept
was ever understood and grasps it again. The controls did not move (qm-5 11/11, quad-8 13/13, algo-8 static
13/13).

Neither text passes under the portrait, and the reason is structural rather than a defect of the texts: with a
static profile a grasped concept reaches 0.36 and one chunk old is worth 0.27; under the portrait understanding's
deficit is 0.8–0.9, so a grasped concept reaches 0.30–0.32 and one chunk old is 0.23, under the 0.25 the target
demands. The thresholds were set against a static ceiling. Once the weights are dynamic, absolute thresholds on
C stop being the right instrument — the verdict should ask where a concept stands among what memory holds, not
what number it has. Open, and a design decision rather than a fix.

One more thing the run showed: prior knowledge is re-activated at its memory C (0.40 for the sandwich) whatever
the portrait says, so the portrait cannot modulate the familiar directly — only through what the familiar
drags in. Whether the pull of a known thing should come from memory or from the response is the same design
decision seen from the other side.

## The program, and distraction

Candidates enter the Field by winning the contest of responses; the **program** is the need whose responses
hold most of the Field, and it is written to the state as an aggregate (`has dominant need`, no keys — the
reader feels which need is driving without a list of why). A change of program brought about by a sensory item
outside the target is a **distraction**, and the engine now names it in the trace.

On v1, chunk 4 ("No lunch, ever"), fed against hungry:

| | Field | need mass |
|---|---|---|
| fed | six items, *making a sandwich* at 0.26 | understanding 1.01, fun 0.39, hunger 0.03 |
| hungry | *lunch* enters at 0.33, *same steps, same result* loses its room | understanding 1.01, fun 0.39, hunger 0.33 |

The distractor takes a slot and displaces a concept, and the program holds: understanding's aggregate is three
times hunger's. That is distraction as a graded thing — the girl walks past, one boy looks up, the game goes on.
A full change of program needs the side response to outweigh the program's whole mass, which a psychophysiological
need at priority 0.7 does not do against a Field full of grasped concepts; a basal need at deficit would.

## Active needs, and the pieces shaped like girls

The portrait is the whole space of goals; the **active** needs are those that must be pursued now (deficit
above the profile's `necessity`) or can be (something present has a path to them). Only active needs weigh.
Safety, basal and satisfied at home, is inactive throughout; the rest are active in every run here.

`profile-starving.txt` is the test the chess example asks for: hunger at deficit 0.95 and class priority 1.0,
and the worked example — *making a sandwich* — given a path to understanding as well as to hunger. The piece is
also a girl. On v1:

| chunk | program | understanding | hunger | event |
|---|---|---:|---:|---|
| 1 | understanding | 0.36 | – | |
| 2 | **hunger** | 0.96 | 1.04 | distraction by *making a sandwich* |
| 3 | hunger | 0.91 | 1.01 | |
| 4 | **understanding** | 1.24 | 1.02 | back, as grasped concepts accumulate |
| 5–9 | understanding | 1.2–1.9 | ~1.0 | hunger holds a third to half of the Field to the end |

Two switches, then a standing contest at near parity; the score falls with the deficit (fed 7, hungry 5,
starving 4 of 13). The switching is damped rather than chaotic because understanding's mass is a sum over
many grasped concepts and grows as the text goes on, while hunger's comes from two or three items and does not.
Whether real attention is this well-behaved is an empirical question; the model's answer is that a program
built of many small responses is robust against one strong distractor and vulnerable to several, or to a basal
deficit.

A change of program by an item inside the target graph would be a **branch** of the scenario rather than a
distraction; the trace already tells them apart by that criterion.

## Conflict is the margin, not the switch

Only one program can have the motor channel, so the felt quantity is not the change of program but how nearly
the runner-up matches the leader. The **conflict level** is the runner-up program's mass over the leader's,
written to the state as an aggregate (`has conflict level`): 0 is one program alone, 1 is the channel contested
every step.

Conflict per chunk on v1:

| | switches | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| fed | 0 | .00 | .60 | .62 | .39 | .54 | .32 | .00 | .00 | .26 |
| hungry | 0 | .00 | .60 | .62 | .39 | .54 | .16 | .16 | .16 | .26 |
| starving | 2 | .00 | .92 | .91 | .82 | .80 | .53 | .65 | .66 | .81 |

The switch count said 0, 0, 2. The margin says the starving child's channel is contested at 0.8–0.9 for the
whole text, with or without a switch — which is what "incomplete play" is. And the fed child is not at rest
either: in chunks 2–5 the runner-up is not hunger but *fun*, the silly robot the text itself brought in to
hold attention. The device that keeps the child reading is also the child's second program.

## The motor field, and what a gate does

Only one program has the motor channel. With the motor field in the engine, the reader's continuation is the
leading program's: "reads on" while understanding leads, "acts on hunger" otherwise — and a chunk that arrives
while the motor field is elsewhere is **not received**.

Starving child, v1, hard gate:

| chunk | motor field | field of consciousness |
|---|---|---|
| 1 | reads on | steps done one after another |
| 2 | **acts on hunger** | *making a sandwich* 0.74 (both paths: the piece is a girl), lunch, robot, teeth, two concepts; components hunger 2 / understanding 2 / fun 1 / none 2 |
| 3–8 | acts on hunger | nothing received; the Field carries and decays |
| 9 | reads on | empty |

2 of 13. The child left the room at chunk 2 and came back to an empty Field. That is the hard gate's
consequence and it is bistable: once the channel is lost, nothing new arrives to feed the scenario's program, so
the program that took the channel keeps it until everything has decayed. Whether attention is that
all-or-nothing is the open empirical question; the soft alternative — reception degraded by the runner-up's
share rather than cut — is one parameter away and not chosen here.

The `has consciousness components` row is the non-unitary Field made visible: at chunk 2 the child's
consciousness is in four pieces by the need each item answers to. The bootstrap's conflict, at the level of
programs, is exactly a Field in more than one piece.

## Two interfaces: the environment, and the model of it

The reader has receptors and effectors toward the text, and a model of the environment — the paths, the
associations, the prerequisites — that can be run instead. Attending to reality means the sensory field is the
chunk; attending to fantasy means the Field is fed from the model, by association from what it already holds.
Which interface the channel uses is decided by reinforcement: **reality yield**, a running estimate of the
response the chunks have been delivering, against **fantasy yield**, the best response the model can produce
from the Field by one more association.

Measured first, on the mass-gated run above: while the starving child's channel was held by hunger (chunks
3–8), fantasy yield was 0.00 — lunch was already in the Field and the bucket had nothing further — against a
reality yield of 0.46. The channel was in the wrong place by the reader's own accounting. So the gate was
changed from mass to reinforcement: the model of the environment gets the channel only while it pays better.

| | mass gate | reinforcement gate |
|---|---|---|
| starving, v1 | 2 / 13; hunger holds chunks 2–8, six chunks not received | **4 / 13**; hunger leads chunks 2–3 but reality still pays, every chunk received, understanding back at 4 |

The lock-in is gone: a program can lead the Field without owning the channel, and it owns the channel only
while running the model is worth more than looking. Fantasy never actually took over here, because a bucket of
ten entries has nothing to daydream with; a richer model of the environment is what would make it pay.

The mode and both yields are state (`attends to`, with the yields in the value and the note). The critic — the
gap between what the model predicted a chunk would deliver and what it did — is the next quantity to write; it
is what should move the reality yield, rather than the running average that stands in for it now.

## The portrait is objective; "I want" is retrospective

Needs have no name in the reader's block. What the reader has is each image's pull (`attracts` / `repels`),
the number of pieces the Field is in, and a retrospective `wants`: the images that pulled most over the last
steps, named as images — "making a sandwich, lunch", never "hunger". Which need that resolves to, and whether
it matches the program, is the analyst's to say.

Starving child, v1, the retrospective against the drive:

| chunk | the reader's `wants` | resolves to | program |
|---|---|---|---|
| 1 | steps done one after another | understanding | understanding |
| 2–3 | making a sandwich, lunch | hunger | hunger |
| **4** | making a sandwich, lunch | hunger | **understanding** |
| 5–9 | the concepts | understanding | understanding |

At chunk 4 the drive has already returned to the text and the reader's account still says food. The report is
a lag of the thing it reports, by construction: it is made of what pulled, and what pulled is a step old.
That is self-opacity as a measured event, the smallest one the machine can show, and it is the same shape as
the confabulation exhibit in the reasoner's rounds — a retrospective attribution built from salience, right
most of the time and wrong at the turn.

## The self-model: a vocabulary about oneself, grown from the difference

The reader models not only the environment but itself. Before each chunk it predicts its own next state — the
same step with nothing coming in: what I will be thinking if nothing arrives — and the actual step differs. The
difference is sorted by kind, and the kinds are the beginnings of a vocabulary about oneself:

| kind | what it is in the engine |
|---|---|
| forgot | predicted in the Field, gone |
| came to mind | in the Field, not predicted, not from the chunk |
| was pulled elsewhere | the program is not the one predicted |
| did not follow | a concept named without its ground |

To the reader this is first a **mass** — `is surprised by itself`, a count with no names — and a kind that
recurs becomes a **name**: `notices about itself | forgot`. The mechanism of the curvature is in none of the
steps; its manifestations, compared against the reader's own prediction of itself, become content.

Starving child, v1:

| chunk | self-surprise | names the reader has for itself |
|---|---:|---|
| 1 | 0 | – |
| 2 | 3 | – (lunch and the silly robot came to mind; pulled to hunger) |
| 3 | 1 | – |
| 4 | 3 | forgot, was pulled elsewhere |
| 7 | 3 | + came to mind |
| 9 | 4 | + did not follow |

Nine chunks in, the reader has four words about itself, none of which it had at the start, and none of which
name a need, a level or a program. The vocabulary is made of the *shape* of the errors, not of their causes:
which is exactly where the causal gap sits. "Forgot" is a fair name for what the engine measures only in part —
it fires as well when a concept is displaced by the chunk as when it decays — and the next refinement is to let
the kinds split as they recur, the way the reader's own would.
