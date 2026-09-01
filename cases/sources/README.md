# Source texts

The passages the cases encode, in the editions they were encoded from. All public domain; provenance is in
each file's header.

| file | work | edition | words |
|---|---|---|---:|
| `kafka-verwandlung-opening.txt` | Die Verwandlung, opening | PG #22367, German original (1915) | 2,936 |
| `kafka-verwandlung-opening.en.txt` | the same, English | **translated for this repository** | 3,244 |
| `dostoevsky-crime-part-one.txt` | Crime and Punishment, Part I | PG #2554, tr. Constance Garnett (1914) | 35,349 |
| `sophocles-antigone.txt` | Antigone | PG #31, tr. Francis Storr (1912) | 10,306 |
| `sophocles-oedipus-the-king.txt` | Oedipus the King | PG #31, tr. Francis Storr (1912) | 12,558 |
| `homer-odyssey-book-xii.txt` | Odyssey XII | PG #1727, tr. Samuel Butler (1900) | 4,601 |
| `gogol-the-cloak.txt` | The Overcoat | PG #1197 (Taras Bulba, and Other Tales) | 12,162 |

Kafka is here in the German original rather than in English because the Gutenberg translation (#5200, Wyllie)
carries a Project Gutenberg licence and is not public domain. The original is, and it is also what the encoding
should answer to.

The English beside it was translated for this repository. Its point is not convenience: the encoding in
`cases/metamorphosis.txt` is written in English, so a translation was happening anyway — silently, inside the
encoding, where nobody could inspect it. Written out, it becomes a step that can be disputed separately from the
encoding it feeds, and it is labelled as what it is, a model's output. Two decisions are flagged in its header
because the case turns on them: `Ungeziefer` is left unspecific ("monstrous vermin"), since "insect" or "beetle"
would decide what the German declines to decide and the encoding is about what Gregor does and does not
represent of his own state; and `Prokurist` is "chief clerk", keeping the rank and the authority the family
cannot refuse at the door.

## Why this directory exists

It was missing, and its absence was not a filing oversight. The five literary cases were encoded from
recollection of the texts, with no document read and no prose present. That is exactly the hole the rest of the
method is built to avoid: the discipline says approximations are rules rather than calls and the model is a
meter rather than a decider, and the whole claim about composition is that **the complexity arrives from the
environment**. With no source, what supplied the environment was a model's memory of it — so the claim was
unsupported for precisely the cases meant to demonstrate it.

It also broke the shape of the pipeline. Everywhere else the project keeps prose beside its encoding: the hybrid
document carries verbatim text next to its Gellish blocks, and a violation of that rule was found and fixed
earlier in this repository. The cases skipped the prose stage entirely.

And it bears hardest on the strongest results. The Metamorphosis numbers — 6 of 18 at fact level, 28% of the
graph left to the reader — depend on the inventory of operative facts being complete and right. That inventory
had no source anyone could check it against.

## The rule

**No case without its source passage.** A case file names the work, the edition and the scope, and the passage
lives here. An encoding is checkable only against the text it claims to encode.

## Verification status

The cases were written before these files existed, so none has yet been checked against its source. Until each
is, its results stand as **unverified**. Re-encoding against the text is worth doing for its own sake as well:
the difference between the recalled encoding and the sourced one measures what an encoder adds when no source
is present, which is a control on the error that produced this directory.
