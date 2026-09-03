# STAGE 1 — instructions for the part only a language model can do

You are given a reader profile, the reader's prior state (if any), and one chunk of text. You do two things and
nothing else; `engine.py` does the rest.

## A. Name what the chunk names

List every signal the chunk names: a thing, an event, a state of the subject, a cost to a need. Rules:

- Use the name the profile or the prior state already uses whenever the chunk refers to something known. Coin a
  new short name only for something new. A wrong new name for a known thing breaks the association table and
  the memory, so check the profile first.
- Give each signal its **word cost**: the number of words in the chunk spent on it. Count them. Overlapping
  spans are allowed; a word may serve two signals.
- Do not add anything the chunk does not name. Association is the engine's job, and inference from the
  situation ("a quarter to seven means he is late") is the reader's, not yours.

## B. Paths the chunk installs

If the chunk *tells* the reader that something costs a need — states it or directly implies it, as opposed to
leaving it to the reader — record it as a path: stimulus, need (one of the profile's), delta in [−1, 1].
This is how an early chunk installs what a later chunk will use. Do not install what the profile already has.

## Output

A TSV, one signal per line, nothing else:

```
<item>	<word cost>
<item>	<word cost>	<stimulus>	<need>	<delta>      ← a signal that also installs a path
```

Before the TSV, at most ten lines saying which spans you counted, so a checker can recount.
