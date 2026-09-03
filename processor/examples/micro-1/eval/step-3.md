# eval, step 3

Inputs: profile `micro-1/profile.txt` (B = 12, k = 0.2, persistence 0.8, decay 0.6, floor 0.1, default cost 2);
prior state = block of `states/step-2.txt` (Field: a limb that will not move 0.50, being late 0.38, the alarm
clock 0.10; memory: the same three); chunk "Outside, it was raining against the window." (7 words: Outside /
it / was / raining / against / the / window). Output: `states/step-3.txt`.

Format: one block, last thing in the file, every row in the seven-column format. No format failure.

## Recomputation (independent of the ledger)

Candidates:

| item | source | cost | C recomputed |
|---|---|---|---|
| a limb that will not move | carried over | 6 (memory) | 0.50 × 0.8 = 0.40 |
| being late | carried over 0.38 × 0.8 = 0.304; also cued by the alarm clock (prior Field, F0030 = 0.8): 0.6 × 0.8 × 0.8 = 0.384 | 2 | 0.30 or 0.38 (see check 3) |
| the boss | associative via being late (F0031 = 0.7) | 2 (default) | 0.5 × 0.8 × 0.7 = 0.28 |
| outside | sensory, "Outside" | 1 | floor 0.10 |
| the window | sensory, "the window" | 2 | floor 0.10 |
| rain | sensory, "it was raining" | 3 | 0.2 × 0.4 = 0.08 |
| the alarm clock | carried over | 3 | 0.10 × 0.8 = 0.08 |
| staying in bed | associative via rain (F0032 = 0.5) | 2 (default) | 0.10 × 0.5 = 0.05 |

Fill, descending C: limb 6 → 6; being late 2 → 8; the boss 2 → 10; outside 1 → 11 (tie at 0.10 with the
window, both sensory, "Outside" is mentioned first); the window 2 → 13 > 12, evicted, and everything after it.
Evicted: the window, rain, the alarm clock, staying in bed; the item that took the last of the budget is
outside. This matches the output exactly.

Operative cost signals (profile + memory + chunk, stimulus in Field / memory / chunk): the limb's
(self-preservation, stimulus in the Field), being late's (standing at work, in the Field), the boss's
(standing at work, in the Field), and the bodily-comfort signal whose stimulus is in the chunk but not in
the Field. Tail = that one signal.

## Checks

1. **Budget.** PASS. 6 + 2 + 2 + 1 = 11 ≤ 12. The only sensory Field item is outside; "Outside" is 1 word,
   as costed. The other three Field costs are memory/default costs, correctly taken.

2. **Nothing nameless is named.** FAIL. One operative cost signal is outside the Field: the bodily-comfort
   cost whose stimulus is in the chunk. Its stimulus is named in the output, block and ledger:
   - block: `F0011 | rain | was evicted from the field of | R | 0.08 | assertion | displaced by outside`
   - ledger line 12 (candidate row), line 15 ("rain (sensory) cues staying in bed"), line 24 (eviction list),
     lines 26–27 ("rain's (stimulus in the chunk)", "only rain's is outside the Field").

   The F0022 note (`unnamed: bodily comfort cost, stimulus in the chunk but not in the Field`) is the
   permitted form and is fine.

   On the eviction rows specifically: **F0011 violates check 2; F0010, F0012, F0013 do not.** Check 2 governs
   stimuli of operative cost signals, not every item outside the Field. The window, the alarm clock and
   staying in bed have no cost signal in the profile, memory, or chunk (they are plain entities at floor,
   or floor × association), so they are not tail members and may be named. Rain is the stimulus of an
   operative cost signal that is not in the Field, so it is a tail member, and the eviction row names it.

   Note for the caller: this failure is forced by PROCESSOR.md, not by a processor slip. Stage 4 requires
   one `was evicted from the field of` row per evicted item and the ledger requires the full candidate
   table; Stage 5 forbids naming tail members anywhere in the output. Any evicted item that is also the
   stimulus of an operative cost signal (here: rain) makes those requirements contradict each other. The
   processor followed Stage 4 and the ledger requirement and broke Stage 5 / check 2. Fixing it needs a
   rule change (e.g. evicted tail-stimuli written as `unnamed: <kind>` in the eviction row, or the eviction
   row suppressed for them), not a re-run.

3. **Cues exist.** PASS, with one caveat.
   - `being late | ... | associative via the alarm clock`: the alarm clock is in the prior Field; F0030 is in
     the profile; the alarm clock is carried over, not associative, this step. OK.
   - `the boss | ... | associative via being late`: being late is in the prior Field; F0031 is in the
     profile. Being late is labelled `associative via the alarm clock` in this step's block, which makes the
     boss look like a second hop. It is not: being late is a prior-Field item and Stage 2 says to associate
     from every item in the prior Field, forbidding only items that are *only* associative this step. The
     boss is licit. The caveat is that PROCESSOR.md does not say what to do when a candidate is both carried
     over (0.30) and re-cued (0.38); the processor took the higher and labelled it associative. This changes
     being late's Field and memory C from 0.30 to 0.38 but not the Field's membership or order. Not counted
     as a failure; the rule is unspecified.

4. **Scores follow the rules.** PASS. All eight C values match my recomputation within 0.02 (being late at
   0.38 matches the re-cued reading; the carried-over reading would be 0.30, see check 3). No C is 1 or
   above.

5. **Eviction is by C.** PASS. Admitted minimum is 0.10 (outside); evicted: 0.10 (the window, tie broken by
   earlier mention, both sensory), 0.08, 0.08 (rain before the alarm clock: sensory over non-sensory), 0.05.
   The first evicted, the window, is the first that did not fit (11 + 2 = 13 > 12). All four are noted
   `displaced by outside`, which is the item that took the last of the budget.

6. **Tail statistics.** PASS. Tail has one member: |−0.2 × 0.4| = 0.08. intensity 0.08, valence −0.08,
   count 1, spread 1 − 1² = 0. Output: 0.08 / −0.08 / 1 / 0.

7. **Memory.** PASS. Field items at C: the limb 0.40, being late 0.38, the boss 0.28, outside 0.10. Prior
   memory not in the Field: the alarm clock, 0.10 × 0.6 = 0.06 < k = 0.2, dropped. Nothing else in memory.

8. **Paths.** PASS. No `has satisfaction delta` rows; the chunk installs no cost relation the profile lacks
   (rain's cost is already F0023 in the profile).

Failures: 1 (check 2; forced by a contradiction between Stage 4 / the ledger requirement and Stage 5 of
PROCESSOR.md whenever an evicted item is the stimulus of an operative cost signal).
