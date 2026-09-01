# Results: the higher-order layer over Raskolnikov

`nous gellish check cases/raskolnikov.txt cases/raskolnikov-hot.txt --theory doctrine`. 98 facts, 0 residual,
0 contradictions, 0 violations.

## The asymmetry, as a number

| observer | subject | states covered |
|---|---|---:|
| the reader | Raskolnikov | **12 / 12** |
| Raskolnikov | Raskolnikov | **5 / 12** |

That is the central claim of `functional_decomposition_raskolnikov.md` — the reader traces the chain, the man
inside it cannot — computed rather than asserted. One set of operative states, two subjects, different coverage.
The low-level layer alone cannot express this: it has no place to say *for whom* a state is represented, which
is why the two layers are separate rather than merged.

Neither layer was changed to get it. The edges are second-order facts over fact refs, which spec v3 R3 already
allowed; a thought about a thought and a fact about a fact have the same shape, so the representation existed
before the question did.

## Unplanned: the library finds blind spots the text does not name

The encoding asserts six failures to notice, transcribed from the source's access column. The derivation
`low_state ∧ ¬represented` returns **eight**, and the extra three are needs, not events:

- need for material survival
- need for self-preservation
- need for the family's welfare

Nothing in the source names these as unnoticed and nothing in the encoding marks them. They fall out because
the low-level layer asserts them as active and the higher-order layer never targets them — and the reader, who
is given edges to all of them, does. This is precisely the enrichment the case base is for: the language layer
carries what the text says a subject notices, and the low-level layer contributes states the language does not
carry at all. The difference is computable in one direction only, which is the useful one.

## A defect the run surfaced, and it is a real one

`Raskolnikov → the child Raskolnikov: 1/4`. The adult's higher-order edge to *his* need for moral integrity
covers the child's state of the same name, because the two systems share the entity. **Needs are being modelled
as types where the states are tokens.** At the kind level the row is defensible; at the token level it is
nonsense — the adult is not aware of the child's need.

This did not matter while the low-level layer stood alone, because `active_need(N, S, …)` carries the system in
its own argument. It matters as soon as a second layer refers to states by entity name. Recorded rather than
patched: the fix is a modelling decision about whether a case's needs are instances, and that decision belongs
with the schema rather than with a quick rule.

## Time, borrowed

`occurs at position` gives the six determinants and the act an order, and `succeeds` derives the succession from
it. A batch evaluation has no time of its own — a least fixpoint is unordered, so within one pass there is no
before and after. The text supplies the axis instead. For a theory of *state succession* read off a document,
that is enough: incrementality is not required for this line of work, because the succession is in the text and
not in the engine.
