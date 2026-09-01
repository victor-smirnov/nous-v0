# The case base

A case is an ordinary Gellish table describing a system in a concrete context; the bootstrap library
(`nous/gellish/bootstrap.dl`) derives its state. No new file format — a case is checked by the same reasoner as
any document and can live inside a hybrid one.

    nous gellish check cases/raskolnikov.txt --theory doctrine
    nous gellish rounds cases/control_deep_chain.txt --rounds 6 --maxdepth 1

This directory is **tracked**, unlike `experiments/`. The cases are not drafts: under Phase 1 they are where the
complexity comes from. The rules are a small invariant skeleton, and a composite that needs its own bespoke rule
is a stipulation rather than a composition — so what the case base supplies is exactly the environment-contributed
structure the demonstration rests on. Controls are part of the evidence, not scaffolding.

## What is here

| file | kind | what it is for |
|---|---|---|
| `raskolnikov.txt` | exhibit | the reference case; *Crime and Punishment* Part 1, plus the dream as a second system |
| `RASKOLNIKOV-BASELINE.md` | measurement | coverage against the source document's 24 checkable propositions, before and after module 3 |
| `demo.txt` | exhibit | three small systems: a model in session, a thermostat, a deliberating person |
| `control_deep_chain.txt` | **control** | a deep chain of unambiguous names, so truncation is the only salient kind — the confabulation exhibit must *fail to appear* here |
| `self.txt` | exhibit | the reasoner as its own case |

## Selection

Cases are chosen **from the composite**, not from the text: pick the composition to exhibit, then find the case
that displays it most cleanly. That is not cherry-picking, because the claim is existential — that the phenomenon
is real and systematically reproducible — not an estimate of its rate or parameters in a population. No sampling
assumption is made, so there is no sampling bias to incur.

The burden moves rather than disappearing. Selection is free; the instance must be airtight:

1. **not stipulated** — the composite must not come from a rule written for it;
2. **robust** — it must survive perturbation (row order, entity renaming), because a batch reasoner reproduces
   its own arbitrary tie-breaks perfectly and re-running the same input confirms every artifact;
3. **legible** — the derivation chain reads on one page, by a human, without running the tool.

Controls carry a matching weight: a composite that appears unconditionally has not been shown to depend on
anything. `control_deep_chain.txt` is the current example — same rules, same shape, distractor removed, and the
misattribution disappears.

## Procedure

Before encoding, record what dimension the case varies and what the framework predicts. Encode. Run against the
**unmodified** library. Only then look. Anything that appears unplanned is a candidate composite; anything
predicted is at best a regression test, and worth close to nothing as evidence.

Moving a criterion after seeing the number is the one abnormal result.

## Reflexive exhibits

Two composites live in the reasoner itself rather than in a case, which makes them the cheapest and least
contestable evidence available: nothing has to be encoded, no claim about humans is needed, and the answer key
is internal. Both are produced by `nous gellish rounds INPUT --maxdepth 1`.

**Confabulation.** The wrapper publishes that the reasoner acted, never the derivation — that lived in the
previous round, only its observables survive, and the action changed those very observables. So the cause is
rebuilt from what is visible now, under parsimony (attribute to the most numerous unfinished kind) and closure
(assert it as *the* cause, no residual). On the article: *"I changed maxdepth to +4 because of grounding
ambiguous"*, where the action rested on entailment truncated alone and cites none of its seven premises.
Reproduced on two independent documents; `control_deep_chain.txt` removes the distractor and the same rules
attribute correctly, so the composite is not printed unconditionally.

**Anchored certainty.** The strict form refuses to ground an ambiguous name, so it never becomes more certain
than it is. The heuristic takes the strongest candidate; on the article all **37 forced choices rest on no
signal at all** — the top dictionary layer leaves two or three candidates and the engine's symbol order picks
one. The choice is then published as an ordinary fact at full commitment, the name stops being ambiguous, and
no rule reopens it. Reversing the *dictionary's* arrival order moves **13 of 37**, among them `context`,
`subject`, `meaning` and `signal` — names on which what the document is taken to be about depends.

That last measurement had to be got right twice. Reversing the document's rows moved nothing, which looked like
stability and was not: the candidates are dictionary UIDs, so the document's order cannot touch the tie-break.
Determinism masquerading as systematicity, exactly as the perturbation rule warns — the first perturbation
tested everything except the thing the choice actually rested on.

**Self-deception**, composed over the two above. The self-model is assembled *by* the approximations, so what it
omits is exactly what they cost. Four divergences appear between what it says and what a second evaluation
shows — and three of them are our wiring, which the report says out loud:

| | gap |
|---|---|
| names it still finds ambiguous: 0, against 37 still ambiguous in the dictionary | wiring — `ground_ambiguous` is still derived; the self-model is attached to the post-forcing relation |
| names it settled itself: 37 | none — reported correctly; it hides nothing |
| settlements it can mark uncertain: 0, against 13 of 37 that move | **principled** |
| why it acted, against what it acted from | memory — the wrapper could have published more |

**Exactly one gap survives that sorting.** Warrant cannot be reported by any rule however written, because it is
a claim about a model the evaluation does not have: a batch evaluation computes one, and warrant needs a second.
`settlement_hedged` is declared in `rounds.dl` and deliberately given no rule, so the missing capability sits in
the program text instead of being merely absent from it. The regression test asserts that the principled list has
exactly one member, so a later change that makes warrant reportable fails loudly rather than passing quietly.

The ablation is built in: with full access the composite cannot arise. The strict form settles nothing and takes
no action, so it has neither an anchor to hold nor a decision to explain.
