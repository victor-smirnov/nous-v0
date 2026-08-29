---
name: gellish
description: Unload reasoning from prose into Gellish fact tables (hybrid prose+ontology documents), check them with the Nous reasoner (contradictions, calibration, provenance), enrich, and render back to prose. Use for /gellish encode|check|enrich|decode|ask|why on any Markdown document, and whenever a text's logical structure must be made explicit and verified.
---

# Gellish: unload, check, load back

You turn prose into a **hybrid document** — the prose plus one ```` ```gellish <SECTION-ID> ````
block per section holding the section's propositional content as a Gellish fact table — check
it with the deterministic reasoner, and render it back. The hybrid document is the source of
truth; prose is a rendering.

Specifications (read the one the step needs before acting):
- `references/hybrid-format.md` — the container: fences, section ids, global fact refs, residual blocks
- `references/encoding-v3.md` — how prose becomes rows: intention enum, positive-proposition rule, second-order rows, residual
- `references/phrases.md` — the only relation phrases allowed (96 types; regenerate with `nous gellish phrases -o …`)
- `references/decoding.md` — how rows become prose: render, don't narrate

Tooling: the `nous` CLI (`python3 -m nous` from the nous-v0 repo if not on PATH). It needs
Soufflé and a built dictionary (`nous gellish build-dict --fetch`, once). Outputs land in `work/out/`.

## /gellish encode <file.md> [--out doc.md]

1. Read the whole file once for terminology; fix the **names** you will use for recurring
   things (the reasoner merges by exact name across sections — one name per thing).
2. Split by headings (`##`, and `###` where a section exceeds ~800 words). Section id =
   `S<n>` in order, or a short slug from the heading number (`S2.2`).
3. For each section, write the ```` ```gellish <id> ```` block under `encoding-v3.md`,
   using only phrases from `phrases.md`, and the ```` ```gellish-residual <id> ```` block
   for what would not fit. Work exhaustively: completeness over brevity. **The prose stays
   verbatim** — insert the blocks after the section's text and change nothing else; never
   summarise or paraphrase the section in its place (a summary is not a shell, and the
   decoder needs the shell).
4. Prefer producing the document directly. For very long inputs, write one table per section
   to a directory and assemble with `nous gellish inject <file.md> DIR/*.txt -o doc.md`
   (a table's first line `# heading: <heading text>` places it under that heading).
5. Verify the prose is untouched (`diff <(nous gellish extract … ) …` is not enough — diff the
   document against the source with the fences stripped), then run `/gellish check`.

## /gellish check <doc.md> [--theory off|hypothesis|doctrine]

1. `nous gellish check doc.md -o REPORT.md` (add `--theory off` to ask only whether the
   document contradicts *itself*; `hypothesis` (default) reads it through the Synthea
   bootstrap at conjecture level; `doctrine` takes the bootstrap as true).
2. Read REPORT.md top to bottom: Stats, Contradictions, Commitment tensions, Cap tensions,
   Spec violations, Residual phrases, Declared residual, Role tensions, Grounding.
3. For every contradiction and tension run `nous gellish why <relation> <filter>` and read
   the proof tree down to its leaves (`row …` = a table row, `dict …` = a dictionary fact).
   Classify each finding:
   - **encoder error** (wrong intention, double negation, invented phrase, second-order row
     on a thing, wrong name for the same thing) → fix the row(s) in the block;
   - **source inconsistency** (the text really says both) → leave the rows, add a
     `gellish-residual` row `F… | other | source-inconsistency | "<quote>"` and, if asked to
     edit prose, a marked note in the prose;
   - **theory disagreement** (the proof passes through a `dict coll: … 100800000` leaf) →
     not an error of the document; report it under a separate heading;
   - **dictionary limitation** (role tension from a Gellish role definition that does not fit
     the domain) → report; propose an extension row if it recurs.
4. Spec violations are always encoder errors: fix them all. Residual phrases with count ≥ 3
   are candidates for the phrase reference — list them; do not invent phrases to absorb them.
5. Re-run until the report is clean or every remaining finding is classified and annotated.
   Report: what changed, what remains and why, the theory-disagreement list, and the
   candidate phrases.

## /gellish enrich <doc.md> [--out doc.enriched.md] [--depth 1] [--theory …]

1. `nous gellish enrich doc.md -o doc.enriched.md` — re-runs the check and writes one
   ```` ```gellish-derived <id> ```` block per section: rows the closure added about the
   section's entities, intention by derivation level, context = provenance (`derived:
   closure`, `theory: Synthea`, `field: depth 1`, `gellish: depth 1`, `…: definition`).
2. Read the derived blocks as a reviewer, not as an author: drop rows that are true but
   useless for this document (upper-ontology leftovers the top-cut missed, engineering senses
   of homonyms such as `Transformer → electrical equipment item`), keep rows that a reader of
   the section would want stated, and note rows that are *surprising* — those are the
   enrichment's value and go into the report.
3. Never edit a derived row into a `gellish` block by hand; if a derived fact should become
   part of the document's own claims, write it as a new stated row with its own intention.
4. A decode of an enriched document renders derived rows only per `decoding.md` rule 3.

## /gellish decode <doc.md> [--out prose.md]

Per section, under `decoding.md` — including its **hard bans** (no narrated stance, no
meta-commentary, no narrated definitions, no added qualifiers, ±10 % length): rewrite the prose
above the block from the block's rows at their stated commitment, using second-order rows only
to set register; keep the shell verbatim wherever the rows it renders are unchanged; never write
a fact UID; ignore `gellish-derived` blocks unless asked for a review rendering. Then remove the
fences for the pure-prose output (`--out`), keeping the hybrid document untouched. Decode from
the *checked* document, not the enriched one.

## /gellish ask "<node>" · /gellish why <relation> [filters]

`nous gellish ask "<node>"` prints everything the closure knows about a node (stated and
derived, with commitment level); `nous gellish why …` prints proof trees. Use them to answer
questions about a checked document instead of re-reading it.

## Judgement calls

- One name per thing, document-wide. If the text uses two, pick one and add
  `A | is identical to | B` once (it is a stated identity, level 4).
- When in doubt about intention, hedge; `assertion` is the marked choice.
- Never put a negative phrase under `denial` (double negation is the most common v2 error).
- Persons are persons (`Dennett`), citations go to `context`.
- An empty residual block is a claim; make it deliberately.
