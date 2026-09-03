# eval, step 2

Inputs: profile micro-1 (B = 12, k = 0.2, persistence 0.8, decay 0.6, floor 0.1, default cost 2);
prior state = fact block of step-1 (Field: a limb that will not move 0.63, the sleeper 0.10, waking 0.10;
memory: the same three); chunk "The alarm clock on the chair showed a quarter to seven." (11 words).
Output: states/step-2.txt. Everything below is recomputed from those, not read off the ledger.

**Format.** PASS. One block, every row has seven pipe-separated columns; ledger lines are `#` comments
before the block and nothing follows it.

**1. Budget.** PASS.
Word costs, counted against the chunk: "The alarm clock" = 3; the limb carries its step-1 cost of 6;
being late was never in a Field, so default 2. Field total 6 + 2 + 3 = 11 <= 12.
(Non-Field sensory counts also check out: "the chair" 2, "showed a quarter to seven" 5.)

**2. Nothing nameless is named.** PASS.
Operative cost signals (stimulus in Field, memory, or chunk): the limb (stimulus in Field and memory) and
being late (stimulus in Field as an associative item). Both are in the Field, so nothing is nameless.
The boss and rain are not operative: neither stimulus is in the Field, memory, or chunk.
Note: the ledger (line 14) mentions "the boss" while explaining the one-hop rule. This is not a violation
because the boss is not operative this step, but it will become operative at step 3 (being late will then be
in the prior Field and cue it); the processor should avoid the habit.

**3. Cues exist.** PASS.
`being late | associative via the alarm clock`: the alarm clock is in this Field (sensory, so not itself
associative this step); the association `the alarm clock is associated with being late 0.8` is in the profile.
One hop. No cue fires on any prior-Field or memory item (limb, sleeper, waking have no table entries), and
being late -> the boss was correctly not taken.

**4. Scores.** PASS. Recomputed:
- a limb that will not move: carried over, 0.63 x 0.8 = 0.504 -> 0.50 (output 0.50)
- being late: |-0.6| x 0.8 (standing at work) = 0.48, x 0.8 (association) = 0.384 -> 0.38 (output 0.38)
- the alarm clock, the chair, a quarter to seven: no cost signal, floor 0.10 (output 0.10 each)
- the sleeper, waking: carried over, 0.10 x 0.8 = 0.08 (output 0.08 each)
No C is 1 or above; no difference exceeds 0.02.

**5. Eviction is by C.** PASS.
Sorted: limb 0.50 (6 -> 6), being late 0.38 (2 -> 8), then a three-way tie at 0.10 among sensory items;
earliest-mentioned is the alarm clock (3 -> 11). Next, the chair (2 -> 13 > 12) is the first that does not
fit and is evicted with everything after it: a quarter to seven 0.10, the sleeper 0.08, waking 0.08.
Every evicted C <= every admitted C (the chair ties at 0.10, resolved by the earlier-mentioned rule).
All four eviction notes name the alarm clock, the item that took the last of the budget. Correct.

**6. Tail statistics.** PASS.
Tail as determined in check 2: empty. intensity 0, valence 0, count 0; spread is undefined on an empty tail
and the output writes 0 with note "empty tail", consistent with step 1. Output matches.

**7. Memory.** PASS.
Field items at C: limb 0.50, being late 0.38, the alarm clock 0.10 (rows F0030-F0032).
Prior memory not in the Field: the sleeper 0.10 x 0.6 = 0.06 < 0.2, dropped; waking likewise. Nothing else
is present.

**8. Paths.** PASS.
No `has satisfaction delta` row. The chunk states a time and nothing about what it costs; the inference that
a quarter to seven means lateness is the reader's, not the text's, and was correctly not installed.

Failures: 0
