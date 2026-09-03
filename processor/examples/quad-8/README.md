# quad-8 — quadratic equations, for a student in the eighth grade

The second example with a truth for every intermediate state, and the first with **prior knowledge**: the
student arrives with a linear equation, the unknown x, the square root, expanding brackets and the area of a
square already in memory (`is in memory of` rows in the profile). Two prerequisites in the target graph point
at that prior knowledge and nowhere else.

The profile is a larger reader than the child: a Field of 40 words, memory decaying ×0.8, four needs
(understanding, getting the answer right, not feeling stupid, interest), and a bucket in which *a formula*
drags in *a formula to memorise* (interest −0.4) and *a test*, *an example* drags in *a worked example*
(competence +0.5, understanding +0.3), *proof* and *why* drag in *a long derivation*, and "obviously" costs
not-feeling-stupid −0.5 outright.

Eight target concepts; five forbidden names (complex numbers, the imaginary unit, the fundamental theorem of
algebra, Vieta's theorem, "polynomial"); three of them must be felt through proxies: the negative-discriminant
case as a door rather than a wall, the three cases and the formula as the shape of the theorem, checking by
substitution and the roots themselves as the sum-and-product observation.

Unlike qm-5, the explainer was told the reader model up front — the budget, the decay, that a short form of a
known concept is cheap, that a concept named without its ground does not stick. Knowing the reader is what a
good explainer has; the loop is there for what it does not know.

## v1

Nine chunks of 31–39 words, a single worked example (x² + 5x + 6 = 0) threaded through, no forbidden word.

The first run failed almost everything, and the failure was the engine's:

| | first run | after the fixes |
|---|---|---|
| reached | 3 / 8 | **8 / 8** |
| felt | 1 / 3 | **3 / 3** |
| prerequisites in place | 14 misses | clean |
| never named | clean | clean |

Three rules, each visible in the trace and each with its own reason:

- **Consolidated memory does not decay.** Prior knowledge was decaying like working memory — 0.5, 0.4, 0.32,
  0.26, gone by chunk 5 — and from then on every new concept was named without its ground, got no
  comprehension, sat at the floor and was forgotten. A cascade from one wrong rule. What the reader brings is
  now a floor under its own decay.
- **Naming what memory holds re-activates it.** A mention of *the unknown x* was scoring it at the floor
  (0.20) and writing that over the 0.6 it had; a cue now scores at least what memory has.
- **What does not fit is skipped, not everything after it.** A 20-word item was blocking 5-word items that
  had room. Attention takes what fits.

The fixes were made after seeing the failure, so the check that matters is the control: qm-5 v3 still passes
11 of 11 under the new engine, and its v1 and v2 re-run to the same verdicts they had (2 of 6 and 4 of 6, with
the same prerequisite miss). The engine changes changed the engine, not the earlier story.

Everything for v1 is under `v1/`.

## What the run says about the text

Under the fixed model the text passes on the first iteration, which is what a text written with the reader
model in hand should do. The trace still shows the price: two concepts (*why the formula works*, *the sign of
the discriminant*) lose the Field once each for lack of room, and the recap chunk carries nine items in 33
words with nothing left over. The example equation is dropped as an unknown token twice — a short form of
something the Field had already evicted — which is the model saying the running example was not kept alive
between chunks 1 and 3. A human reader of the same text would probably notice the same thing.
