# paper_v2

- `plan.md` — the working plan; dated decisions and notes.
- `frames.md` — the argument in frames (iteration 2); the text of the paper is written from it.
- `argument.hybrid.md` — the same claims as Gellish facts, checked by the reasoner (`nous gellish check`).
- `SOURCES.md` — every citation with the claim it has to support and its verification status.
- `verification/` — per-batch tasks for the source verification.
- `sources/` — obtained copies of sources (not committed; see `.gitignore`).
- `main.tex` — preamble, title, abstract; the sections are separate files:
  `sec-phenomenon.tex` (frames P), `sec-difficulties.tex` (D), `sec-approach.tex` (A),
  `sec-measurement.tex` (S). Frame ids are kept in comments next to the subsections they come from.
- `refs.bib` — the bibliography, keyed by surname and year.

Build: `tectonic -X compile main.tex` (tectonic 0.17 in `~/.local/bin`, no system TeX needed).
Current draft: 30 pages, 90 references.
