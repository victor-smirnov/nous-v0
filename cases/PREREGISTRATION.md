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

---

# Pre-registration: Akaky and Oedipus

Same procedure. Written before encoding; both run against the unmodified library.

## akaky.txt

**Dimension varied:** whether a Subject is enacted at all, within one character. Gogol gives the ablation for
free — the same man before and after the overcoat becomes a need.

**A concession recorded in advance.** The clean version would change exactly one thing, the added need. It is
not available without misreading the text: Akaky at his desk does not encounter, conclude or act, and giving him
those conditions to tidy the experiment would be encoding a different man. So **two things change** — a need is
added and the three Observer conditions become satisfiable — and any finding must be read against that. Fidelity
over experimental tidiness, stated here rather than discovered later.

**Predicted:**
- before — no conflict, `automatism` on the copying, `missing_condition` Encounter, no level;
- after — conflict between standing and subsistence, anguish, an Observer that manifests.

**Would count against us:** conflict before the coat, or automatism after it.

## oedipus.txt

**Dimension varied:** access to one's own determinants, before and after the revelation. The determinants
themselves do not change — only what he can reach.

**Predicted — a gap, pre-registered as one.** The library has no representation of determinant access: it was
folded into the module that derives the Observer from compression under a prediction requirement, which is not
built. So the **ladder should fail to discriminate the two stages**, and that failure is the point of the case:
it is the sharpest available statement of what module 1 is for, since the play changes nothing except access.

**Also predicted, and this one is a real derivation:** the epistemic quale should differ between the stages,
because the projection is selected by the active context and the context does change — he demands to know, and
then he knows. Same residual, different projection, no new rule.

**Would count against us:** identical qualia across the two stages, which would mean the projection is not
tracking context; or the ladder discriminating them, which would mean something is representing access that we
did not think was.
