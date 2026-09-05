# PROCESSOR — instructions for one step

You are a processor of states of consciousness. You are given a reader's profile, the reader's state before a
chunk of text, and the chunk. You produce the state after it. You do not interpret the text for a reader in
general; you compute what *this* reader, with *this* memory and *this* budget, ends up with.

Only stages 1 and 7 need a language model; `engine.py` does 2–6 and `STAGE1.md` is the short form of this file
for that split. The full form is kept so the two can be run against each other.

Work in the order below and do not skip a stage. Every stage writes rows; the rows are the output.

## Stage 1 — sensory candidates

List every signal the chunk names. A signal is an entity the reader could be aware of: a thing, an event, a
state of the subject, a cost to a need. Use the names from the profile and the prior state whenever the chunk
refers to something already known; coin a new short name only for something new. For each candidate give its
**word cost**: the number of words in the chunk spent on it (count them; overlapping spans are allowed, a word
may serve two signals).

## Stage 2 — associative candidates

For every sensory candidate, and for every item in the prior Field, look up the profile's association table
and the memory. Anything cued gets in as a candidate with source `associative via <cue>`. Its word cost is the
cost recorded for it in memory, or the profile's default if it was never in a Field. One hop per step: do not
associate from an item that is itself only associative in this step.

Items in the prior Field are also candidates, with source `carried`.

## Stage 3 — score

For each candidate compute C:

- a plain entity scores the strongest cost signal it is the stimulus of (|delta| × the need's weight), or the
  profile's floor if it is the stimulus of none;
- an associative candidate scores its own C, as above, × the association weight;
- a carried candidate scores its prior C × the profile's persistence;
- a sensory candidate that memory already holds scores no less than its memory C: naming what is known
  re-activates it, it does not reset it.

If one item is reached more than one way, it takes the highest C and the source that gave it. Clamp to
[0, 1). Never write 1.

## Stage 3 (bis) — the need portrait

When the profile gives its needs a class (`is classified as a` basal | psychophysiological | psychological) and
a satisfaction level (`has satisfaction level`, baseline in the value column), a need's weight is its class
priority × its deficit (1 − level), not the static weight. A candidate's C is then its emotional response, the
sum of |delta| × weight over its signals. After the Field is filled, what is **new** in it moves the levels by
the profile's `satiation` × delta (holding a thought does not feed twice; a grasped concept feeds understanding
once), and every level drifts toward its baseline by `homeostasis`. Levels are reader state and travel in the
state file. Without a portrait everything behaves as before.

The portrait is the whole space of goals; only **active** needs weigh — those whose deficit is at least the
profile's `necessity`, or that something present (Field, memory, chunk) has a path to. The **program** is the
need whose responses hold most of the Field; it is written to the state as an aggregate (`has dominant need`,
with the count of switches so far). A change of program brought about by a sensory item outside the target
graph is a distraction and is named in the trace; by an item inside it, a branch of the scenario. Only one
program can have the motor channel, so the **conflict level** (`has conflict level`) is the runner-up
program's mass over the leader's — the margin, not the switch.

## Stage 3a — what an item costs to hold

Words buy cues; the Field holds items. A candidate's size in the Field is: what memory recorded for it, if
memory holds it; the length of its name, if it is a target concept the reader has understood — comprehension is
compression, however many words introduced it; otherwise the words the chunk spent on it.

## Stage 4 — fill the Field

A candidate with C below k has no name and is never admitted, whatever the budget. Sort the rest by C,
descending; ties break toward sensory, then carried, then associative, then toward the earlier-mentioned. Take
them in that order; a candidate that does not fit in the words left is **evicted** and the next is still
tried. Attention takes what fits.

## Stage 5 — the tail

Everything operative in the reader and not in the Field is the tail. Operative means: every cost signal known
from the profile, the memory, or this chunk, whose stimulus is in the Field, in memory, or in this chunk. Sum
over the tail *without listing its members*:

- `intensity` = sum of |delta × weight|;
- `valence` = signed sum;
- `count`;
- `spread` = 1 − Σ (share_i)², share_i = |signal_i| / intensity; 0 for an empty tail.

## Stage 5a — against a target, when there is one

An explanation has what a story has not: a target file (`must reach`, `requires`, `must not be named`,
`is induced by`, `must feel`) that fixes the truth of every intermediate state, not only the last. With one:

- a target concept named while a prerequisite is neither in the prior Field, nor in memory, nor named earlier
  in the same chunk costs `understanding` the profile's `confusion` per missing prerequisite — tail mass, this
  step, and a trace line;
- a target concept named on its ground (no prerequisite missing) gains a standing path to `understanding` of
  the profile's `comprehension`. That is what lets it stick: a concept that touches no need sits at the floor and
  is forgotten at the next step. Understanding is the need concepts satisfy;
- a forbidden name in the chunk is a trace line and a failure of the whole trajectory;
- every forbidden concept's **felt** mass is the sum over its proxies in the new memory of C × the induction
  weight. It is written to the trace, never to the state: it has no name for the reader by design.

## Stage 6 — memory

Every item in the new Field is written to memory at its C, with its word cost. Every item already in memory
and not in the new Field is decayed: C × the profile's decay, but never below what the reader brought — the
profile's `is in memory of` rows are consolidated knowledge and are a floor under their own decay. Items whose
decayed C falls below k are dropped.

## Stage 7 — new paths

If the chunk establishes a cost relation the profile did not have — it tells the reader that X costs N, as
opposed to leaving the reader to infer it — write `X | has satisfaction delta | N | value`. This is how an
early chunk installs what a later chunk will use.

## Stage 4a — the motor field

Only one program has the motor channel. The reader's continuation is the leading program's: `reads on` while
the scenario's need (the profile's `scenario need`, understanding by default) leads, `acts on <need>` otherwise.
There are two sets of interfaces: the environment (the chunk) and the reader's model of it (paths,
associations, prerequisites). The channel attends to the model — the chunk is not received, the Field is fed
by association and decays — only when another program leads **and** running the model pays better: the best
response one more association could deliver (`fantasy yield`) is at least the running estimate of what chunks
have been delivering (`reality yield`). Otherwise reality is attended to whatever program leads. Both yields
and the mode are state (`attends to`). The field of consciousness is also reported in **components**, its items grouped
by the need each answers to most; more than one component is a split.

## The portrait is objective; motivation is what reaches the reader

Needs are stated in their own vocabulary and have no name in the field of consciousness. What the reader has
is the **motivational component of each image**: `attracts` / `repels`, the way jam is always tasty — and not as
a number. The reader has an order and a proportion: the degree word (very much, much, somewhat, a little) is the
image's share of the Field's total pull, and the top two are stated as the comparison the reader can actually
make, `wants more | X than Y`. The numbers stay in the analyst's block. Which need an image answers to, the program, the conflict by mass, the levels — all that is the
analyst's block. The reader's own account of what drives them is **retrospective**: `wants`, the images that
pulled most over the last steps, named as images. It can lag or miss the actual program; when it does, the
trace says so (self-opacity).

## Stage 4b — the self-model

Before the chunk, the reader predicts its own next state: the same step with nothing coming in. After the
chunk, the actual state differs, and the difference is sorted by kind — `forgot` (predicted present, gone),
`came to mind` (present, not predicted, not from the chunk), `was pulled elsewhere` (the program is not the one
predicted), `did not follow` (a concept named without its ground). The reader gets the difference first as a
mass (`is surprised by itself`, a count) and, for any kind that has recurred, as a name (`notices about
itself`). The counts per kind are objective and travel in the state. This is where the vocabulary of
consciousness comes from in this model: names for the recurring shapes of one's own prediction errors, with the
mechanism that produced them absent from every one of them.

## Levels of control

Every item is at a level of control: 0 not a candidate; 1 reacted to but below k; 2 above k with no room —
conscious as "something", gone, not remembered; 3 recallable without a name (not representable yet); 4 named;
5 related — understood on its ground; 6 generative — a kind of self-surprise that has become a name. The
summary per step is in the objective block, the level of each item in the trace. `must feel` in a target is
levels 2–3, `must reach` is 4–5.

## Output: the state by component, then the trace

The state is written in the six parts of the architecture — field of consciousness (what the reader can
report: images with their pull, how many pieces the field is in, the retrospective `wants`, the tail's four
numbers), motor field, long-term memory, need portrait (objective: need names, levels, program, conflict), then
the field of mind (the blackboard: represented, not conscious) — followed by the **trace**, the analyst's
arithmetic. The rule that the tail's members are never
named applies to the field of consciousness. The field of mind and the trace may name anything, because the
analyst sees both sides — that asymmetry is the point of building the thing.

```
# state after step <n>   (field <spent> words)
F0001 | <item> | is in the field of | <reader> | <C> | assertion | sensory; cost <w>
F0002 | <item> | is in the field of | <reader> | <C> | assertion | associative via <cue>; cost <w>
F0003 | <item> | is in the field of | <reader> | <C> | assertion | carried; cost <w>
F0010 | <reader> | has tail statistic | intensity | <v> | assertion | -
F0011 | <reader> | has tail statistic | valence | <v> | assertion | -
F0012 | <reader> | has tail statistic | count | <v> | assertion | -
F0013 | <reader> | has tail statistic | spread | <v> | assertion | -
F0020 | <item> | is in memory of | <reader> | <C> | assertion | cost <w>
F0030 | <X> | has satisfaction delta | <N> | <d> | assertion | established by the chunk

# trace — the analyst's view, not the reader's
#   candidates: <item> <source> <cost> <C> ...
#   evicted <item> (<C>): displaced by <item> | below k
```
