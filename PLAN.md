# Plan: the reasoner as a standalone project and a Claude (then Codex) skill

Goal (Victor, 2026-08-29): a tool + skill for *unloading* reasoning from prose into ontological
structure (Gellish) and *loading it back*: prose → hybrid prose+Gellish document → pipeline
(consistency, enrichment, …) → optionally prose again. First real use: article v2 of
`docs/what_is_it_like_to_be_a_language_model.md`.

## 1. Shape of the product

Three layers, each usable without the next:

| layer | what | who runs it |
|---|---|---|
| **core** (deterministic) | dictionary build, parse, Soufflé closure, checks, enrichment export, provenance, diff | scripts, no model |
| **skill** (LLM-driven) | encode prose → hybrid doc; repair loop over reasoner findings; decode hybrid → prose | Claude / Codex following the skill's specs |
| **domain dictionaries** | Gellish standard + field extensions (`philosophy_of_mind`) + project theories (`synthea_bootstrap`) | live with their projects, plugged in by path |

The **hybrid document** is the central artifact: Markdown with the prose shell kept (addressee,
modality, first person — what the round-trip study showed Gellish cannot carry) and one fenced
```gellish``` block per section holding the v3 table. Fact UIDs are document-global
(`S3:F0012` — section 3). A hybrid doc is at once readable, diffable, and machine-checkable.

## 2. Repository: `nous-v0`, package `nous` (M1 done 2026-08-29)

```
nous-v0/
  nous/cli.py            `nous gellish build-dict | check | ask | why | report`  (+ enrich | diff | extract | inject — M3)
  nous/gellish/          dictionary.py  parse.py  reasoner.dl  run.py  report.py  ask.py  why.py  paths.py
  nous/gellish/ext/builder.py   the extension builder
  ext/<name>/spec.py     philosophy_of_mind (field, neutral) and synthea_bootstrap (the theory) — both live here
  bootstrap/             Synthea bootstrap 01–06 (source of synthea_bootstrap)
  data/                  gellish.net release + Soufflé export (git-ignored; build-dict --fetch)
  work/                  per-run facts/out/prov (git-ignored)
  spec/                  hybrid-format.md, encoding-v3.md, decoding.md, phrases.md (generated)
  .claude/skills/gellish/   the Claude skill (SKILL.md + references → spec/); symlinked into ~/.claude/skills
  tests/                 golden regression on tables/article-v1
```

Soufflé is a runtime dependency, checked at startup with a clear message.

CLI contract (all deterministic):
- `gellish check doc.md [--theory off|hypothesis|doctrine] [--ext DIR…]` → `out/` + REPORT.md
- `gellish enrich doc.md` → `doc.enriched.md` (derived rows appended with provenance; top-cut; definitions)
- `gellish why doc.md <relation> [filters…]` → proof trees
- `gellish diff a.md b.md` → semantic diff of the two closures (added / removed / level-changed edges)
- `gellish extract doc.md` → bare tables; `gellish inject doc.md tables/` → hybrid doc

## 3. The skill

`skill/SKILL.md` (frontmatter: name `gellish`, description, user-invocable) with subcommands
expressed as workflows for the model:

- `/gellish encode <file>` — chunk by section; for each section produce the ```gellish``` block
  under `spec/encoding-v3.md`, with the dictionary phrase list (generated from `dictfacts`,
  ~3 300 phrases grouped by family) in context; residual goes to a mandatory `untranslatable`
  list, never to invented phrases. Output: hybrid doc.
- `/gellish check <doc>` — runs the CLI, then *reads* REPORT.md and `why` output and proposes
  repairs: classify each finding as encoder error (fix the table), source inconsistency (flag
  in prose with a marker), or theory disagreement (`--theory` diff). Repairs are edits to the
  ```gellish``` blocks; re-run until clean or every remaining finding is annotated.
- `/gellish enrich <doc>` — CLI export, then the model reviews derived rows and drops noise the
  top-cut missed.
- `/gellish decode <doc>` — per section, prose from table + shell under `spec/decoding.md`:
  use second-order rows to choose register (hedge, attribute, mark figurative), never narrate
  them; keep the prose shell verbatim where it carries addressee/modality.
- `/gellish roundtrip <file>` — encode → check → enrich → decode, with the existing judges
  (first-order fidelity, second-order inversion probe) run on demand.

`references/` holds the specs and the phrase list; `scripts/` the CLI wrappers. Codex later:
same scripts, instructions moved into `AGENTS.md` / its skills directory — the deterministic
core is identical, only the prompt container changes.

## 4. Spec v3 (what changes vs v2, all from measured findings)

1. **Positive-proposition rule.** The triple always states the positive proposition;
   `denial` negates it. Negative phrasing (`cannot`, `lacks`, `is not`) with `denial` is an error.
2. **Second-order relations only over fact UIDs.** `is offered as`, `is endorsed by`, …
   require a `S#:F#` on the left.
3. **Dictionary in the contract.** The encoder receives the phrase list and must use it;
   anything else goes to `untranslatable` as `(anchor F#, category, needed relation, quote)`.
4. **Section anchoring + global UIDs**, so cross-section references and diffs work.
5. **Persons and works as individuals**, cited as `Dennett 1991` → alias rows or the people
   dictionary; no citation strings in the object columns.
6. Keep from v2: mandatory intention enum, reification, `is a cause of` ban (now enforced by
   Gellish 1922 roles), figurative rows.

## 4b. Spec v3.1 backlog (from the article run, 2026-08-29)

- Internal cross-references: a row type or residual category for "(Section 4.2)" / document links — C lost all of them.
- Reconcile "≤ 5 consecutive source words" with quoted definitions: quotes allowed only in `is defined as` and residual `quote`.
- (Dropped, Victor 2026-08-29: style/register is a separate channel, its loss through the ontology is expected and
  desirable. Decode C is the intended behaviour.) A rows-vs-prose *first-order* self-check before returning may still be useful.
- Encoders write unicode comment markers («, ＃) and occasionally truncate the first row — assembler now normalises; spec
  should say ASCII `#` only.
- Enrichment output is for review, not for decoding; document in decoding.md (done) and in enrich --for-review default.

## 5. Article v2 — the first run (work lives in `experiments/article/`, git-ignored; moves to Synthea later)

1. Chunk `docs/what_is_it_like_to_be_a_language_model.md` by section (≈ the 9 chunks used before, but section-aligned).
2. Encode with the v3 spec, Opus (the cost study found amplified Opus dominant); result: `article.hybrid.md`.
3. `check --theory off` (does the article contradict itself?) and `check --theory doctrine
   --ext synthea` (**does the article agree with the bootstrap?** — this is the first time the
   article can be checked against its own theory mechanically).
4. Repair loop with `why`; every surviving finding becomes a footnote in the prose.
5. `enrich` → `article.enriched.md`; review derived rows.
6. `decode` → `article-v2.md`; judge against v1 with the v2-experiment judges; the
   inversion probe is the acceptance metric (target: inversion mass below the v2 experiment's 785).
7. Keep both: the hybrid doc is the *source of truth* from now on; prose is a rendering.

## 6. Order of work and effort

| milestone | content | effort |
|---|---|---|
| M1 | extract repo, package, CLI, golden tests, Soufflé check | done 2026-08-29 |
| M2 | hybrid format, spec v3, phrase list generator, skill (encode/check/decode) | done 2026-08-29 |
| M3 | enrich export (top-cut, definitions, provenance column), diff, decode spec | done 2026-08-29 |
| M4 | article run: encode → check → repair → enrich → decode → judge | done 2026-08-29 (A/B/C decodes; report in experiments/article/REPORT.md) |
| M5 | Codex port | ½ day |

## 7. Decisions to confirm

- ~~Repo name~~ `nous-v0`, package `nous`, MIT. Both dictionaries live here.
- Encoding model for the article run: Opus (cost study) — unless Fable is preferred for frugality.
- ~~Hybrid container~~ fences (done).
