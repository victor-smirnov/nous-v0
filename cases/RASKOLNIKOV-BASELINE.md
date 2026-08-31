# Baseline: what the library derives on Raskolnikov today

Case: `raskolnikov.txt`, encoded in the existing schema only, run with `--theory doctrine`. Source of the
proposition list: `Synthea/docs/functional_decomposition_raskolnikov.md`.

## Result

```
Raskolnikov          level Moral Agent   |  the child Raskolnikov  level Moral Agent
                     valence  negative on the letter (-0.95)
                     valence  positive on the proposed murder (+0.35)
                     conflict × 8 (unranked, stimulus not shown)
                     quale    freedom (agency) / rightness (moral-epistemic) / conscience (moral)
                     silent   need for social belonging
automatism: poverty, illness, the article, Marmeladov, the tavern conversation
0 contradictions, 0 violations, 0 missing conditions
```

## Coverage against the document's 24 checkable propositions

| | count |
|---|---:|
| fully derived | 5 |
| partially derived | 2 |
| not derivable in the current schema | 17 |

**21% fully derived; 29% with partials.** Of the 5 derived, three are the level labels, and those follow in one
step from premises the encoding *asserted*. Only two derivations are load-bearing:

- **quale projection** — `freedom (agency context)` is exactly the document's claim that the openness of the
  disjunction is the subjective signature of the causal break, arrived at independently;
- **automatism / manifestation split** — five of the six determinants land in `automatism`, and the Observer
  manifests only on the letter and on the proposed murder. That is the document's central structural claim.

## The automatism hit is right for the wrong reason

Those five determinants were classified as automatism because the encoding gave them **no satisfaction deltas**,
not because Raskolnikov **cannot trace them**. Same output, different cause. A derivation that reaches the right
conclusion from the wrong premise is not load-bearing: change the case and it stops tracking. This is the single
strongest argument for module 1 (determinants with per-standpoint access), because it converts an accident
into an inference.

## The headline defect: adult and child are indistinguishable

Both come out `Moral Agent`, and that is the *one* distinction the document is built to draw — the child is a
pure moral stack, the adult a fractured one carrying two competing theories of the common good. The library has
no notion of a theory of the common good as an object, so `holds_common_good` is a regex on a phrase and fires
identically for one theory and for two in collision. **The composition that constitutes the novel's central
state is invisible to the library.**

Related, same cause: the eight `conflict` rows are the cross-product of positive×negative needs on a stimulus.
The document asserts *one* conflict, between two Acceptors. Pair-level conflicts do not compose into
theory-level conflict, and nothing ranks them. `case_state` also projects the stimulus out of the conflict row,
so the output cannot say *which decision* a conflict is about — a reporting bug independent of the schema gap.

## Second defect: valence answers a different question than anguish

The murder sums to **+0.35** — the library reports positive valence on the murder. Defensible as a decision
signal (he does go through with it), but the document's phenomenal claim is that the anguish *is* the conflict,
not the sum. Valence and anguish are two observables and the library exports only the first as the headline.
A magnitude of conflict — something like Σ|negative| given Σpositive > 0 — is missing and is cheap to add.

## What this makes the four modules concrete

| module | what it buys, measured |
|---|---|
| 1. determinants + per-standpoint access | props 2, 3, 4, 7; converts the automatism hit into an inference; lets Encounter be derived instead of asserted (prop 5, 6) |
| 2. presupposition via Gellish role restrictions | props 8, 9 — the Observer derived from the *form of the question* |
| 3. acceptors / theories of common good as objects | props 15, 16, 17, 19, 21 — and separates adult from child |
| 4. episode index | props 22 — the dream as an earlier state of the same subject, and the collision on waking |
| (bonus) approximation verdict | props 13, 14 — "I decided" as approximation, not fabrication |

Module 3 alone unlocks five propositions and the central discrimination; it is the one to build first.

## The quality criterion this suggests

Coverage (derived / total propositions) is the obvious metric and it is **gameable by assertion**: add a row
asserting the conclusion and coverage rises while nothing was inferred. Discrimination is not gameable the same
way. So the optimization target for the fixpoint loop should be:

1. **Discrimination** — for each curated *pair* of cases the source distinguishes (adult/child, Raskolnikov/
   thermostat, Raskolnikov before/after the murder), does the library's output differ, and differ in the way
   the source says? Binary, per pair.
2. **Derivation depth** — how many derived facts rest on premises that were themselves derived, versus asserted
   directly. Guards against encoding the answer into the case.
3. **Ablation stability** — remove one row from the case; which conclusions survive? The document claims each
   determinant is necessary and none sufficient. That is a checkable claim about the ablation matrix, and it is
   also the counterfactual an essay cannot provide.

All three are computable from artifacts the reasoner already writes.

---

# After module 3 (acceptors and theories of the common good as objects)

Added to `ext/synthea_bootstrap`: concepts `theory of the common good`, `target state`; relations `is an
acceptor of` · `has target state` · `applies the theory` · `has verdict on` · `holds theory`. Added to
`bootstrap.dl`: `acceptor_of` · `applies_theory` · `target_state` · `verdict` · `holds_theory` ·
`acceptor_conflict` · `theory_conflict` · `means_conflict` · `moral_stack` · `anguish`, plus a derivation of
`holds_common_good` from a theory object instead of a regex on a phrase.

## The discrimination now holds

```
Raskolnikov            level Moral Agent   moral stack CONTESTED
                       theory conflict  the Napoleonic theory vs conventional morality on the proposed murder
                       anguish 1.11 on the proposed murder   (valence +0.35)
                       anguish 0.18 on the letter            (valence -0.95)
the child Raskolnikov  level Moral Agent   moral stack UNCONTESTED
                       anguish 0.20 on the attempt to protect the horse
```

Both remain Moral Agents — correctly, the document says the child *is* one. The level label was never the
thing that distinguished them, and now it does not have to: the **shape** of the stack does.

Two results that were not designed for and fell out:

- **The murder is positive in valence (+0.35) and highest in anguish (1.11) at once.** Those are not in
  tension; they are the document's two claims about the same state — he goes through with it, and it tears
  him apart. One number could not carry both.
- **The letter separates from the murder by kind, not degree.** Anguish 0.18 against valence −0.95: the
  letter is a blow, the murder is a dilemma. Nothing in the encoding says so; it follows from the shape of
  the signal masses.

`means_conflict` earns its place by staying empty here: two acceptors under *one* theory disagreeing about an
action is a conflict of means, not of goods, and the library now refuses to call that moral conflict. The
regression test (`sys-C` / `sys-D` in `test_bootstrap_lib.py`) is built precisely on that pair — identical in
every observable the pre-module library had, differing only in how many theories are in play.

## Coverage

| | before | after |
|---|---:|---:|
| fully derived | 5 | 10 |
| partially derived | 2 | 2 |
| not derivable | 17 | 12 |

**42% fully derived** (props 15, 16, 17, 19, 21 unlocked). Derivation depth improved as well: `holds_common_good`
now rests on a classification the case states about a theory object, rather than on a phrase match, so Level 2
is inferred rather than spelled.

Next by the same measure: module 1 (determinants with per-standpoint access), which converts the automatism
result from accident into inference and lets Encounter be derived — props 2, 3, 4, 5, 6, 7.
