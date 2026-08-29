# Decoding specification: render, don't narrate

How a hybrid document's tables become prose again. The block is the source; the prose shell
(addressee, modality, first person, section order) is kept; the second-order rows decide the
*register* of each sentence and are never spoken aloud.

## Rules

1. **Every fact in the block appears in the prose**, at the commitment its intention gives it:
   `assertion` → plain declarative; `hedged-assertion` → a hedge from the source's own register
   ("typically", "largely"); `hypothesis` → "we propose / conjecture"; `prediction` → future or
   "should"; `definition` → definitional phrasing ("by X we mean"); `question` → a question;
   `denial` → a negation of the positive proposition; `requirement` → "must / shall";
   `attributed-claim` → attributed to its `is asserted by` party, with the author's stance from
   `is endorsed by` / `is rejected by`; `rebutted-claim` → presented and then rejected, using
   the `is raised to rebut` row for the rejection.
2. **Second-order rows are instructions, not content.** `F | is offered as | figurative` means:
   write F as an image, do not write "this is a metaphor". `F | has commitment | possible`
   lowers the register of F. `F | is qualified as | most consequential` gives F emphasis and
   position, not a sentence about being consequential. `F | implies | G` becomes "therefore /
   so / which means" between the two sentences. Fact UIDs never appear in prose.
3. **Derived rows** (from `enrich`, marked `derived:` / `dictionary:` / `theory:` in context)
   are rendered only if they add something a reader of the section needs; dictionary
   supertypes (`… is a kind of artefact`) are almost never rendered. When rendered, a derived
   row keeps its level: a level-2 derivation is a conjecture in prose.
4. **Residual rows are the exception list.** Each `gellish-residual` row names something the
   table could not hold; the decoder carries it from the *prose shell*, not by inventing.
   If the shell was discarded, the residual row is rendered as a marked gap ("[modality lost:
   'may']") rather than silently dropped.
5. **Terminology is the table's.** Object names are used as written; synonyms only where the
   table itself declares them (`is identical to`, `is a synonym of`).
6. **No new claims.** Nothing enters the prose that is not a row, a residual, or shell.

## Hard bans (each was found by blind judges and counted as hallucination)

- Never state the author's stance as a sentence ("and we largely accept this", "the author endorses"). A stance
  row selects the register of the claim it is about; it is never itself said.
- Never write meta-commentary about the table, the source or the encoding ("listed twice in the source",
  "the text nowhere equates", "strictly, the rows say"). If two rows disagree, render the source's sentence.
- Never narrate definitions ("by X we mean", "X is the position whose core thesis is") where the source simply
  used the term; render a definition row only where the source defined the term.
- Never add evaluative or theoretical glosses that are not rows of this section.
- Never insert a qualifier ("apparent", "computational", "functional") into a term the source uses bare, unless a
  row of this section states the qualified form and the sentence being rendered uses it.
- Taxonomy rows (`is a kind of`, `is realized in`) are satisfied by using the term correctly, not by a sentence.
- Length within ±10 % of the source section; longer means you are narrating rows instead of rendering them.
- Derived blocks are not decoder input unless the run explicitly asks for review-style rendering.

Measured on the article (38 sections, blind Opus judges): with these bans, fidelity 86.6 → 97.8, hallucination
20.4 → 4.7, epistemic stance 66.8 → 94.1, inversion mass 8 881 → 1 139, length ×1.22 → ×1.02.

## Output

The prose for the section replaces the prose above its block; the block stays. A pure-prose
rendering is the document with all fences removed — derived, never edited by hand.
