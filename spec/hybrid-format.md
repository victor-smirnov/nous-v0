# Hybrid document format

A hybrid document is Markdown prose with the reasoning *unloaded* into Gellish fact tables that
sit next to the prose they formalise. The prose keeps what Gellish cannot carry — addressee,
modality, first person, rhetorical shape; the tables carry the propositional content, its
epistemic status, and the second-order structure (stance, entailment, figurativeness). The
hybrid document is the source of truth; prose-only renderings are derived from it.

## Container

```markdown
## 2.2 The Observer as a Conclusion

Prose of the section, unchanged or lightly edited …

```gellish S2.2
F0001 | Observer | is classified as a | conclusion | - | definition | -
F0002 | F0001 | is offered as | literal | - | assertion | -
```

```gellish-residual S2.2
F0001 | rhetorical | is raised as a challenge to | "not a process, but a conclusion" 
```
```

- A fenced block with info string `gellish <SECTION-ID>` holds one v3 fact table (seven
  pipe-separated columns, see `encoding-v3.md`). The section id is free text without spaces
  (`S1`, `S2.2`, `C03`, `intro`); if omitted, blocks are numbered `S1, S2, …` in order.
- Fact UIDs are local to the block (`F0001`). Globally a fact is `<SECTION-ID>:<F-uid>`.
  A row may reference a fact in *another* block by its global id (`S2.1:F0007`); bare `F0007`
  always means "this block".
- A block with info string `gellish-residual <SECTION-ID>` lists what the encoder could not
  state: `anchor | category | needed relation | quote`. `anchor` is a fact uid (local or
  global) or `-`; `category` ∈ {relation-missing, second-order, modality, quantity, temporal,
  rhetorical, other}; `quote` is the source span, ≤ 12 words. These rows are not reasoned
  over; they are counted, listed in the report, and are the backlog for dictionary revisions.
- A block with info string `gellish-derived <SECTION-ID>` is written by `nous gellish enrich`:
  rows the reasoner derived about the section's entities, with provenance in the context
  column. It is output, never input — the reasoner ignores it, `enrich` replaces it.
- Everything outside the fences is prose and is ignored by the reasoner.
- A document may carry YAML front matter with `gellish: {spec: 3, ext: [synthea_bootstrap]}`;
  currently informational.

## Sections and prose

- One block per heading section is the norm; a long section may have several blocks (`S4a`,
  `S4b`) and a short one may share a block with its neighbour.
- The prose above a block may be the original text (encode step) or a rendering of the block
  (decode step). A decode never edits the block; an encode never edits the prose except to
  insert the block.
- Cross-section references in prose ("as argued in §2.2") stay in prose; cross-section
  references between *facts* use global ids.

## Bare tables

Plain `.txt` tables (one block per file, section id = file stem) remain accepted; `nous
gellish extract` turns a hybrid document into such files and `inject` puts tables back into
a document — replacing blocks with matching section ids, appending blocks whose section has
no fence yet under the heading named in the block's first comment line `# heading: …`, or at
the end.
