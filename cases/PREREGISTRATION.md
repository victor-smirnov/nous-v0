# Pre-registration: Antigone and Odysseus

Written before encoding, per `README.md`. Both cases run against the **unmodified** library — no rule is added
for them. Anything predicted below is at best a regression test; only what appears unplanned counts as evidence.

## antigone.txt

**Dimension varied:** number of theories of the common good, holding everything else fixed. Two subjects face
the *same* action — the burial of Polynices — and the play makes their stacks differ in shape rather than in
level. Chosen because the collision is stated almost without psychological noise: near a unit test.

**Internal control.** Creon in the first movement holds one theory (the law of the city) and no other. Same
action, same situation, one theory instead of two. If `moral_stack` comes out contested for him as well, the
discrimination is not tracking theories and module 3 is worth less than the Raskolnikov pair suggested.

**Predicted:**
- Antigone — Moral Agent, moral stack **contested**, `theory_conflict` between the two laws on the burial;
- Creon — Moral Agent, moral stack **uncontested**, `means_conflict` empty;
- anguish greater than the absolute value of valence for Antigone: she acts decisively and it costs her.

**Would count against us:** identical output for the two, or a contested stack for Creon.

## odysseus.txt

**Dimension varied:** a conflict that is dissolved *by a plan* rather than by choosing. The mast and the wax
satisfy both goals by structuring the act; nothing is given up. Chosen because it isolates sequencing from
preference.

**Predicted — a failure, and pre-registered as one.** The library has no representation of a plan: plans as
objects were deliberately deferred as capability rather than composition. So it should report an unresolved
conflict on the Sirens' song and offer nothing that marks the conflict as dissolved. The case is encoded
without any plan vocabulary precisely so the gap is visible rather than papered over.

**Would count against us:** the library reporting something that looks like resolution. That would mean a rule
is doing work we did not think it was doing.

**What this case is for:** naming the boundary in a form that can be handed to someone else. If the composite
"conflict dissolved by sequencing" is to be exhibited later, this file is where the requirement is recorded.
