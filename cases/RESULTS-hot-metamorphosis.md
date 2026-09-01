# HOT analysis: the opening of "Die Verwandlung"

`nous gellish check cases/metamorphosis.txt cases/metamorphosis-hot.txt --theory doctrine`.
69 facts, 0 residual, 0 contradictions, 0 violations. Three subjects over one set of operative states: Gregor,
a reader who takes the first sentence as a fact of the world, and one who takes it as a figure.

Chosen because the failure is not Raskolnikov's. Raskolnikov cannot trace what determines him; Gregor traces his
morning in complete detail and has no higher-order representation of what his own state costs.

## The granularity of awareness turned out not to be a detail

| | Gregor | literal reader | figural reader |
|---|---:|---:|---:|
| **entity** level | 7 / 9 | 8 / 9 | 6 / 9 |
| **fact** level | **6 / 18** | 9 / 18 | 6 / 18 |

At entity level Gregor looks nearly self-aware: 7 of the 9 things operative in him are ones he notices. At fact
level he covers a third. He knows *what is there* and not *what it costs* — seven of his twelve unrepresented
facts are `what it costs` rows, including that the transformation has ended his position, cut him from his
family, and put his survival at stake, and including his need for self-preservation being active at all.

Entity-level analysis alone would have concluded the opposite about him. The distinction was not designed in:
the material forced it, because a subject can be aware that a thing is present and unaware of what it costs, and
those are two facts about one entity. `represented_fact`, `low_fact`, `unconscious_fact` and `fact_asymmetry`
were added for that reason and no other.

## What the text carries, and what a reader supplies

Between the two readers, over Gregor's 18 operative facts:

- **5 shared** — read the same way under either construal;
- **8 covered by neither** — the text does not put them in play for anyone;
- **5 divergent (28%)** — this is the portion the text underdetermines and a reader decides.

The divergent five are specific rather than diffuse. The literal reader alone reaches the transformation as a
stimulus, what it costs his survival, what it costs his bodily comfort, and the weather at the window. The
figural reader alone reaches that keeping his position is what is *active* in him — the job as the thing that
did the transforming.

That is the architecture working as stated: part of the higher-order graph is fixed by the text and part lives
in the reader's own state. The fixed part is checkable without human subjects. The 28% is where readers would
be expected to differ, and is therefore what a benchmark would have to measure.

## A negative result worth keeping

`Gregor covers, no reader does: none`. There is nothing he is aware of that neither reader reaches. Not
necessary — a text could easily give a character private access the reader lacks — so it is a fact about this
opening rather than about the method, and it is the kind of row that would go the other way in a first-person
narration.
