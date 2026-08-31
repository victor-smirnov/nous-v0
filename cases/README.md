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
