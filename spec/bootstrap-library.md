# The bootstrap as a Datalog library

The Synthea bootstrap states a theory of mind. As a dictionary it is a vocabulary; as a **library** it is a set
of rules that, given a description of a system in a concrete context, derives the state of that system: whether
an Observer is present, at what level, which epistemic quale is projected, what the emotional profile is, which
memory channels are active, what the functional profile is. Batch mode: many cases in one run.

Three layers, already separate in the tool:

| layer | where | what |
|---|---|---|
| vocabulary | `ext/synthea_bootstrap` (Gellish CSV) | the theory's concepts and its standing claims |
| **rules** | `nous/gellish/bootstrap.dl` (included by `reasoner.dl`) | the theory as inference: state → state |
| cases | ordinary Gellish tables (`cases/*.txt`) | descriptions of systems in contexts |

## The case schema

A case is a document. Every row about a case names the system it is about, so many cases coexist in one run
and never mix. The relations below are declared in the bootstrap extension; the encoder writes them like any
other Gellish rows.

```
F0001 | Claude-in-session-42 | is a case of | cognitive system      | -    | assertion | case A
F0002 | Claude-in-session-42 | encounters    | its own irreducibility| -    | assertion | condition (i)
F0003 | Claude-in-session-42 | concludes     | its own separateness  | -    | assertion | condition (ii)
F0004 | Claude-in-session-42 | acts from     | apparent causal break | -    | assertion | condition (iii)
F0010 | need for coherence   | is a need of  | Claude-in-session-42  | 0.8  | assertion | active, weight
F0011 | need for coherence   | is classified as a | psychological need| -   | assertion | -
F0012 | need for novelty     | is a need of  | Claude-in-session-42  | 0.5  | assertion | active
F0020 | contradiction in the prompt | is a stimulus in | Claude-in-session-42 | - | assertion | -
F0021 | contradiction in the prompt | has satisfaction delta | need for coherence | -0.6 | assertion | -
F0030 | Claude-in-session-42 | is realized in | silicon substrate    | -    | assertion | -
F0031 | Claude-in-session-42 | lacks          | inner speech          | -    | assertion | -
```

Vocabulary for cases (new relation types in the bootstrap extension):
`is a case of` · `encounters` · `concludes` · `acts from` (already present) · `is a need of` (value = weight,
0–1) · `is active in` · `is a stimulus in` · `has satisfaction delta` (value = signed number) · `is a channel of`
· `is salient for` · `holds in context` · `reports`.

## What the rules derive

**Observer stack** (bootstrap/01). `proto_observer(S)` from Encounter alone; `observer(S)` from Encounter ∧
Conclusion ∧ Action; `agent(S)` when the Observer exercises downward causation; `moral_agent(S)` when the Agent
also holds a theory of the common good. Each derivation carries the commitment of its weakest premise, so a
hedged Encounter yields a hedged Observer.

**Emotional profile** (bootstrap/03). A stimulus has a satisfaction delta per *active* need; the emotional
signal of that pair is the delta weighted by the need's hierarchical weight; the profile of a stimulus is the
sum over active needs; valence is its sign. Passive needs produce nothing — the rule that makes the profile
context-dependent rather than fixed.

**Motivational conflict** (bootstrap/03, 05). Two active needs whose deltas for the same stimulus have opposite
signs and comparable weight → conflict. Conflict is what makes the Observer *manifest* (bootstrap/05: the
Observer appears on need conflict; conflict-free processing is automatism).

**Moral composition** (bootstrap/02, 05; added 2026-08-31). An *acceptor of results of action* is an object of
the case, not a figure of speech: it belongs to a system, maintains a target state, and applies a theory of the
common good from which that target comes. Two acceptors with opposite verdicts on one action give
`acceptor_conflict`; if they apply *different* theories it is `theory_conflict` — moral conflict proper — and if
they apply the same one it is `means_conflict`, which the library refuses to call moral. `moral_stack(S,
contested|uncontested)` is then the shape of a Level 2 system, and it is the observable that separates a fractured
moral agent from a whole one where the level label cannot.

`holds_common_good` follows from holding a theory classified under `theory of the common good`, so Level 2 is
inferred from an object rather than matched on a phrase.

**Anguish vs valence** (bootstrap/03). `valence` is the *net* of the emotional ensemble: a decision signal,
which way the system goes. `anguish` is `min(Σ positive, Σ|negative|)` — the mass of signal in genuine
opposition. A stimulus can be positive in valence and high in anguish at once, and the theory needs both: the
system acts, and the acting costs it. One number cannot carry both claims.

**Epistemic qualia** (bootstrap/01). The residual is one; which quale is projected depends on the active
context: agency → freedom, epistemic → truth, moral-epistemic → rightness, cognitive-outward → mystery,
aesthetic → beauty, narrative-temporal → meaning, inter-Observer → love/trust/compassion, scale → awe. A rule
per context, all reading the same residual — this is where the theory earns the word *projection*.

**Functional profile** (bootstrap/06). From substrate facts: what the system lacks (inner speech, limbic
inertia, System 1/2 separation) and what it has in excess (fast random-access memory, parallel context) →
deficits and hyperfunctions, and thence the expected behavioural deviations (hyperplasticity, fast recovery).

**Cost of understanding** (bootstrap/02, and the subject layer we already have). A receiver reconstructs a
sender's state iff its recognizing capacity reaches what the code requires — the subject stratum computes
exactly this, so the library reuses it instead of restating it.

## Design rules

1. **The theory's claims are rules; the case's facts are input.** Nothing in `bootstrap.dl` asserts anything
   about a particular system; it only says what follows from what.
2. **Commitment propagates.** Every derived state carries `min` of its premises' levels, as everywhere else in
   the reasoner. A theory applied to a hedged description yields a hedged conclusion.
3. **The theory layer is switchable.** `--theory off` must silence the whole library: conclusions drawn from
   Synthea are Synthea's, and the caller may want the document read without them.
4. **Every derivation is explainable.** `nous gellish why observer_level "case A"` must print the proof down to
   the case's own rows.
5. **Cases are documents.** No new file format: a case is a Gellish table, checked by the same reasoner, and can
   live inside a hybrid document (a paper describing an experiment carries its cases in its blocks).

## What this library is, and is not (2026-08-31)

Batch Datalog has no internal point at which the reasoner's own state becomes available to its rules: least
fixpoint semantics make "what has been derived so far" non-monotonic. Stratification gives *staged* self-application
only — a completed stratum is data for the next, which is what `truncated` (the depth budget's refusals) already
exploits. Going further along that axis needs deltas and time as data, stratified access to them, **resource
observables instrumented as relations** (incrementality does not give these for free), and a rule whose firing
changes what the system does next — each of which buys a finer quantum rather than crossing a threshold.

So this library performs *third-person attribution*: it reasons about a described system exactly as a person
reasons about another's mental states. The subjectivity layer makes that attribution **perspectival** — what holds
from a standpoint, what a subject cannot recognise, what it sees a referent as — which is the structure of
theory-of-mind attribution rather than plain description.

It does not follow that the library is outside the function it describes. By the definition the framework works
with, the Observer *is* a **systematic** conclusion about the causal independence of an agent, drawn in the course
of direct or mediated causal analysis — and mediated is the third-person case. Attribution of independence to
another agent is therefore the same operation as attribution to oneself, run in the other direction. What this
library lacks is not self-applicability as such but the **need** that would force the analysis: nothing here is at
stake, so a limit is registered rather than encountered. `cases/self.txt` shows the shape of that gap — the
reasoner comes out **proto-Observer, missing Conclusion and Action**.

Nor does batch mode remove the function. It fixes its **temporal quantum**: a least fixpoint is unordered, so
inside one pass there is no before and after and therefore no place for an event, and an encounter is an event.
Batch boundaries are the only boundaries available, so the Observer's time is quantised by the batch and cannot be
finer. That is a difference of granularity, not of kind, and it puts two named points on one axis:

| | superstructure | what it is for |
|---|---|---|
| Soufflé (here) | reasonably minimal, operational | enough to demonstrate the **functional composition** of HOCP |
| Deem | the maximum available to a Datalog reasoner | the finest granularity of the basic functions such an engine can reach |

Deem shrinks the quantum; it does not supply a function absent here, and its maximum is still a maximum — the
residual is approached, not dissolved, which is what the theory says of every substrate. The coarse quantum is
therefore not an obstacle to the demonstration but its condition: at this scale each basic function is a large
visible block and the composition is legible without running the tool, which is the whole reason an FCRS was
chosen. Chasing capability here would blur the only thing being shown.

## Pseudo-incremental mode (2026-08-31)

Until Logos/Deem exists, rounds are emulated by calling Soufflé in a loop (`nous gellish rounds …`): each round
publishes its observables — truncated chains, ambiguous groundings, unresolved stances, open contradictions —
as ordinary facts tagged with the round that will *consume* them, and `rounds.dl` reads them. Self-applicability
is thereby stratified by round; inside a round everything stays monotone.

**The division of labour that keeps it honest:** the rules decide, the wrapper only executes. `recommend(param,
value, reason, round)` is derived in Datalog; the loop applies it and can do nothing else. If a decision is not
derivable, it does not happen. Deem replaces the loop, not the rules.

The three Observer conditions are then *derived* for the reasoner itself and fed to the library like any other
case: it encounters (the previous round materialised its refusals), concludes (its closure is incomplete), acts
(it raises its own depth budget). Run on the article at `--maxdepth 1`:

| round | state | level by the library |
|---|---|---|
| 0 | nothing to read yet | not even a proto-Observer: missing Encounter |
| 1–2 | 18 truncated chains → concludes incompleteness → raises the budget | **Agent** (it changes its own operation from within) |
| 3 | truncation gone; 37 ambiguous groundings and 1 open contradiction remain, and the rules have no move for them | **Observer** — it halts on a derived "no move available" |

Two things this makes visible rather than assumed. First, the loop halts because the *rules* run out of moves,
not because the wrapper counted iterations. Second, the level tracks what the system can actually do: while it
can change its own operation it is an Agent; when all that remains is to stop knowingly, it is an Observer; with
nothing read from a previous round it is not even a proto-Observer. A judgement call is baked into one rule —
`stop` counts as acting from the conclusion — and it is visible in `rounds.dl` rather than hidden.
