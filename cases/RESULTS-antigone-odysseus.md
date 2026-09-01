# Results: Antigone and Odysseus

Run against the unmodified library, `--theory doctrine`. Both close with 0 contradictions, 0 violations, 0
residual rows. Predictions in `PREREGISTRATION.md`, written before encoding.

## Predicted, and confirmed

| | predicted | got |
|---|---|---|
| Antigone | Moral Agent, **contested**, theory conflict on the burial | as predicted: the law of the gods vs the law of the city |
| Creon (first movement) | Moral Agent, **uncontested** | as predicted |
| Antigone | anguish above \|valence\| | 0.81 against 0.08 |
| Odysseus | unresolved conflict, nothing marking resolution | as predicted |

The internal control holds: same act, same play, one theory instead of two, and the stack shape differs while
the level does not. That is the second independent pair for module 3 after adult/child, and this one was
predicted in writing beforehand — so it is a regression test, worth little as evidence, which is what a
control is for.

## Unplanned — what the cases produced that was not designed in

**1. Creon processes the same act automatically that manifests Antigone's Observer.** One stimulus, two
systems: `observer_manifests(Antigone, the burial)` and `automatism(Creon, the burial)`. His two active needs
both take negative deltas from the burial, so there is no opposition at all and no anguish — he is not in
conflict, he is executing. Nothing in the encoding aimed at this: the case was built to vary the *number of
theories*, and the discrimination appeared on a different axis, manifestation. It is also, incidentally, the
play's verdict on him.

**2. Odysseus is in anguish on *both* available options** — 0.72 on listening, 0.64 on sailing past. Neither
option is free of opposition, and that is exactly the condition "no available action satisfies all pursued
needs", showing up as a pattern in the output rather than as a rule anywhere in the library. The second
stimulus was encoded for completeness, not to produce this. It is the closest thing we have to the
channel-exclusivity account arriving from the data instead of from the theory.

**3. Odysseus separates motivational conflict from moral conflict.** He is a Moral Agent with an
**uncontested** stack and an unresolvable conflict: his dilemma is over means, not over goods, and the library
says so without being asked. This is a useful negative check on module 3 — `theory_conflict` is not merely
tracking "a conflict exists", or it would have fired here.

**4. Antigone's two measures diverge by an order of magnitude.** Valence −0.08, anguish 0.81. By the net she is
almost balanced; by the opposition she is at a maximum. The deltas were chosen by hand, so this is weaker
evidence than the three above, but the sum was not computed in advance and the pattern is what the play
asserts: she does not hesitate, and it costs her everything.

## The gap Odysseus was encoded to expose

The library reports the conflict and offers nothing that would dissolve it, exactly as pre-registered. What is
missing is not a verdict but a *structure*: the mast and the wax satisfy both ends by ordering the act, and
nothing in the vocabulary can say "first bound, then past". Recorded here as the requirement, should the
composite "conflict dissolved by sequencing" be exhibited later. Encoding it away — by adding a stimulus called
"the plan" with positive deltas everywhere — would have produced a resolution that means nothing, which is why
the case carries no plan vocabulary at all.
