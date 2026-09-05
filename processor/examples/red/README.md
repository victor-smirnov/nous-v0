# red — a person reasoning about the look of red

The first case whose target contains an **open branch**: a question the text raises and nothing closes. Nine
chunks of inner monologue, written here (`text.txt`), with Locke's inverted-spectrum passage beside it as the
canonical source (`cases/sources/locke-essay-II-xxxii-14-16.txt`). The thinker is a reflective adult, not a
philosopher: knows in outline how seeing works, has never been asked what the look of a colour is. Seven
philosophical terms are forbidden (qualia, the hard problem, the explanatory gap, the inverted spectrum, …) and
four of them must be felt through proxies.

Chunk 4 installs the branch: "why this look — the story stops exactly there" is read by stage 1 as *the question
costs understanding*, a path of −0.6 that no later chunk closes.

## What the model predicted, and what happened

**The open branch stays open.** From chunk 4 to the end, *why this look* is in the Field with a negative pull
(−0.5, "repels much" / "very much"), at level 4 — named, never grasped. It leaves the Field once, at chunk 6
("only pointing" takes the room), and returns at 7. Nothing the text does moves it. That is the residue the
closure hypothesis says an emotion is made of, and it is the only item in any run so far that the reader
holds *against* its pull for six chunks.

**Locke's move appears without being written.** At chunks 8 and 9 the reader's one comparison is
`wants more | a tidy explanation than why this look`. "The whole mechanism" in chunk 8 cues *a tidy explanation*
through the bucket, and its pull (+0.54) outranks the question's. The thinker prefers the explanation it has to
the question it cannot close — which is exactly what Locke does in §15: the contrary supposition "is of little
use … and so we need not trouble ourselves to examine it". The text's last chunk, "the apple is still red, I
pick it up", is the same closure by action, and it scores on coherence.

**The tail turns.** Valence of what reaches consciousness without a name: +0.37 at the question's arrival
(a mystery is a puzzle, and puzzles please), +1.58 at chunk 5 (the inverted-spectrum thought, still a puzzle),
then −0.41 and −0.43 at chunks 8–9, when *no path from one to the other* cues *a contradiction*. The diffuse
feeling goes from delight to unease as the branch is recognised as unclosable. Conflict rises at the end
(0.21): coherence against understanding.

**The reader's words for itself**: *forgot* (chunk 5), *came to mind* (8), *did not follow* (9). Not
"ineffable" — the model has no kind for "named, well-posed, and unclosable"; it only has the kinds its
self-prediction can miss on. That is the gap this case exposes, below.

## The verdict, and what it says

| check | result |
|---|---|
| never named a forbidden word | pass |
| felt | qualia, the hard problem — pass; the explanatory gap 0.15, the inverted spectrum 0.00 — fail |
| reached | 3 of 9 |
| in order | 2 misses, both at chunk 8 |

The reach failures are the text's, under the profile: the mechanism concepts (wavelength, the pattern in the
brain) are named in chunks 1–2 and decay below k long before chunk 8 contrasts "the whole mechanism" with the
look, so the contrast is made of unknown tokens and *two truths and no path* is named without its ground. A
real thinker holds the mechanism through a nine-sentence thought; either the monologue should re-hold it, or an
adult's decay is slower than 0.8. Not tuned here. The phenomenology above does not depend on it.

## Two engine rules the case forced

- **Installed paths are state.** The −0.6 the question costs understanding was written at chunk 4 and lost by
  chunk 6, after which the question was "grasped" like any concept and attracted (+0.38). Every path the text
  installs is now carried in every state file.
- **A grasped concept carries its ground.** Re-naming an understood concept after its prerequisites have decayed
  was counted as a miss; comprehension is compression, and the prerequisites are inside it. Checked only until
  the concept is grasped. Controls unchanged (qm-5 11/11, quad-8 13/13, algo-8 13/13).

## What the case exposes

The engine can hold an open branch — as a named item with a standing negative pull — but it cannot say what
kind of item it is. On the scale of control the question sits at level 4 forever: named, not grasped, not
closable. The look of red itself, the thing the question is about, sits lower: recallable (the thinker can
imagine red), reportable as "that", with no name beyond the pointer — level 3, which the engine cannot
represent at all. So the two central objects of this reasoning are exactly the two states the architecture is
weakest on: a level-3 item and a permanently open level-4 branch. The self-model's vocabulary has no kind for
either, which is why the reader ends with *forgot* and *did not follow* rather than *ineffable*. The hard
problem, in this machine, is the place where its own representational gaps coincide — which is at least a
precise statement of what would have to be built.
