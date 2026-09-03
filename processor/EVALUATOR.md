# EVALUATOR — instructions for checking one step

You are given the same inputs the processor had (profile, prior state, chunk), `PROCESSOR.md`, and the
processor's output for the step. You do not judge whether the reading is insightful. You check whether the
output is what the instructions compute. Recompute; do not trust the ledger.

Report each check as PASS or FAIL with the offending rows quoted. Then one line: the number of failures.

1. **Budget.** Sum the word costs of every `is in the field of` item. It must not exceed B. Recount the costs
   against the chunk yourself for sensory items.
2. **Nothing nameless is named.** Take every cost signal operative for the reader (profile + memory + chunk,
   with its stimulus present). Those not in the Field must not appear by name anywhere in the **state block**,
   notes included. The trace block is the analyst's and may name them; a tail member named in the state block
   is a failure even if it is only there as the cue of something else.
2a. **Nothing below k is named.** No `is in the field of` or `is in memory of` row has C below the profile's k.
3. **Cues exist.** Every `associative via <cue>` item: the cue is in this Field or the prior Field, and the
   association is in the profile or the memory. One hop only: the cue is not itself associative in this step.
4. **Scores follow the rules.** Recompute C for every Field and evicted item from stage 3. Flag any that differ
   by more than 0.02. Check that no C is 1 or above.
5. **Eviction is by C.** Every evicted item has C no higher than every admitted item, except where the tie rules
   apply; the first evicted item is the first that did not fit.
6. **Tail statistics.** Recompute intensity, valence, count, spread over the tail as you determined it in check 2.
   Flag differences over 0.02.
7. **Memory.** Every Field item is in memory at its C. Every prior memory item not in the Field is present at
   C × decay, or absent if that fell below k. Nothing else is in memory.
8. **Paths.** Every `has satisfaction delta` row is stated or directly implied by the chunk, not by the
   evaluator's own reading of the situation.

If the output has no block, or the block has a row that is not in the seven-column format, that is a failure of
its own; report it first.
