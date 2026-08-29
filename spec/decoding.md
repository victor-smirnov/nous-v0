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

## Output

The prose for the section replaces the prose above its block; the block stays. A pure-prose
rendering is the document with all fences removed — derived, never edited by hand.
