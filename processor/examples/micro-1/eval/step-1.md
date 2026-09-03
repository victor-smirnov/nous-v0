# eval — micro-1, step 1

Inputs: profile `micro-1/profile.txt`; prior state none (empty Field, empty memory); chunk
"He woke and found that his right arm would not move." Output: `states/step-1.txt`. Everything below is
recomputed from the profile and the chunk; the ledger was not used.

Parameters read from the profile: B = 12, k = 0.2, persistence 0.8, decay 0.6, floor 0.1, default cost 2.
Need weights: self-preservation 0.9, standing at work 0.8, bodily comfort 0.4.

**Format.** One block, ten rows (F0001–F0003, F0020–F0023, F0030–F0032), every row has seven `|`-separated
columns. PASS.

## 1. Budget — PASS

Chunk word count, done by hand: He / woke / and / found / that / his / right / arm / would / not / move = 11.

| Field item | span | words |
|---|---|---|
| a limb that will not move | "his right arm would not move" | 6 |
| the sleeper | "He" | 1 |
| waking | "He woke" | 2 |

Sum 9 ≤ 12. The overlap on "He" is allowed by Stage 1. The ledger's costs match mine.

## 2. Nothing nameless is named — PASS

Operative cost signals (profile signals whose stimulus is in the Field, memory, or chunk):

- a limb that will not move → self-preservation −0.7: stimulus is in the chunk. Operative. In the Field.
- being late → standing at work: stimulus not in chunk, memory empty, not in Field. Not operative.
- the boss → standing at work: same, not operative.
- rain → bodily comfort: same, not operative.

Tail is therefore empty. Neither "being late", "the boss", "rain", "the alarm clock" nor "staying in bed" appears
anywhere in the output, ledger included. The ledger names only Field items.

## 3. Cues exist — PASS (vacuous)

No `associative via` rows. Checking that none was owed: the association table's cue side is
{the alarm clock, being late, rain}; none of the three sensory candidates is one of these, and memory is empty.
Nothing should have been cued. Correct.

## 4. Scores follow the rules — PASS

- a limb that will not move: |−0.7| × 0.9 = 0.63. Output 0.63. Δ 0.
- the sleeper: no cost signal → floor 0.10. Output 0.10. Δ 0.
- waking: no cost signal → floor 0.10. Output 0.10. Δ 0.

No C is 1 or above. No carried-over items (prior Field empty), so persistence does not apply.

## 5. Eviction is by C — PASS

Sorted descending: 0.63 (6 words, running 6), then the two 0.10 items. Tie between the sleeper and waking:
both sensory, "He" precedes "woke", so the sleeper first (running 7), then waking (running 9). Nothing fails to
fit; zero evictions is correct, and correctly there are no `was evicted` rows.

## 6. Tail statistics — PASS

Tail empty (check 2). intensity = 0, valence = 0, count = 0. Output 0 / 0 / 0. Δ 0.
Spread is 1 − Σ share² with intensity 0, i.e. undefined by the formula; the output writes 0 with note
"empty tail". That is a reasonable convention and the note does not name a signal. Not counted as a failure, but
worth fixing in PROCESSOR.md so the convention is explicit (spread of an empty tail = 0).

## 7. Memory — PASS

Field items and their C: limb 0.63, sleeper 0.10, waking 0.10. Memory rows F0030–F0032 carry exactly these at
exactly these values. Prior memory empty, so nothing to decay and nothing to drop. No extra memory rows.

Observation, not a failure: the sleeper and waking enter memory at 0.10, which is below k = 0.2. Stage 6 only
drops items whose *decayed* C falls below k, so writing them is what the instructions say; but they will
vanish at step 2 (0.10 × 0.6 = 0.06 < 0.2) unless they are in the Field again.

## 8. Paths — PASS

No `has satisfaction delta` rows. The chunk states that an arm will not move; it does not tell the reader what
that costs. The cost relation is already in the profile (F0020), so nothing new was to be installed.

---

Failures: 0
