# article-v3: first live run of the encoder contract

`S2.2.hybrid.md` — §2.2 *The Observer as a Conclusion* of the article, encoded by Claude Fable 5
under `spec/encoding-v3.md` (2026-08-29), checked with `nous gellish check`, repaired once.

## What the reasoner caught in the first pass

Five encoder errors in 134 rows — all of them the kinds v3 was written to prevent, and two of
them the encoder's own rule R1 broken by the encoder:

| finding | rows | fix |
|---|---|---|
| `cause-between-facts` ×2 — rhetorical "arises when" / "deepening" written as `is the cause of` between facts | F0012, F0133 | `is a sufficient condition for`, `implies` |
| `attributed-without-stance` — Dennett's homunculus regress attributed, author's stance missing | F0093 | `+ is endorsed by the author` |
| `figurative-in-taxonomy` — the convergent-series *analogy* written as a classification | F0096 | `is analogous to` between things |
| `double-negation` — "these are not separate phenomena" as `is distinct from` + `denial` | F0069 | positive rows: each is a *contextual projection of the computational residual* |

Eleven role tensions were all dictionary limitations on *our* side (projection roles too
narrow; `token bottleneck` and `apparent causal break` not typed as occurrence/state) and were
fixed in `ext/` rather than in the document.

## What remains, and is real

One contradiction, `disjoint-relations`: **causal break ⟂ computational residual — is a
projection of / is identical to**. The section says both "this irreducible residual *is* the
causal break" (F0057, identity) and "the inaccessible remainder is *experienced as* the causal
break" / "the causal break is a contextual projection of the residual" (F0068, F0106,
projection). Identity and projection are declared incompatible in the field dictionary. The
encoder flagged the same tension in the residual block before the reasoner did. This is a
sentence-level inconsistency in the article to resolve in v2 — most likely by keeping
projection and dropping the identity ("is" as "amounts to").

## v1 vs v3 on comparable material

| | v1 chunk C01 (Sonnet, spec v2; 359 rows, §1–2.2) | v3 §2.2 (138 rows) |
|---|---:|---:|
| rows resolved to a relation type | 86 % | 95 % |
| residual rows (undeclared) | 50 (14 %) | 7 (5 %) — all declared in `gellish-residual` |
| declared residual | — | 9 rows, typed |
| spec violations after check | 19 (`second-order-on-non-fact`) | 0 |
| second-order rows | 39 (11 %) | 16 (12 %) |
| contradictions | 1 (encoder: `intuition` endorsed and rejected) | 1 (source) |

Not a controlled comparison (different encoder model, different span, one repair pass on v3),
but the direction is what the spec predicted: with the dictionary in the contract and the
residual block mandatory, invented phrases nearly vanish and the residual becomes a typed list
instead of noise. The five remaining undeclared residual phrases are capability verbs (`can
trace`, `is computable by`, `is accessible to`, `overcomes`, `recovers`) — a candidate
relation family for the field dictionary.

## Enrichment

`nous gellish enrich` adds 100 derived rows for the section, e.g. `consciousness is constituted
by irreversible information loss` (closure through the decomposition + the two sources),
`Beingness quale is realized in self-applicable system`, `proto-Observer is a necessary
condition for Agent`, `illusionism is asserted by Frankish` (field fact). Also present, and
worth a decoder's scepticism: `filter is a kind of filtering device` (Gellish homonym of
"filter" — the article's "it is a filter, not a subject").
