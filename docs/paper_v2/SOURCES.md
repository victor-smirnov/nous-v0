# Sources ledger for paper v2

One row per key in `refs.bib`. A source counts as **verified** only when the copy has been obtained, opened, and the
claim the paper makes located in it. Statuses:

- `verified` — read against the claim, with the locus noted;
- `obtained` — a copy is in `sources/`, not yet read against the claim;
- `substitute` — the copy in `sources/` is a précis, chapter or later edition rather than the cited item; usable, and
  the citation may need to change to what was actually read;
- `unverified` — no copy obtained yet.

The batch verification started on 2026-09-11 with three agents was stopped after the download stage, so most rows
are `obtained` rather than `verified`. Files marked `-` still need a copy. Verification continues per section as the
text is revised; the claim column is what has to be checked, and nothing else.

| key | what it must support | status | file |
|---|---|---|---|
| nagel1974 | the bat question marks a limit on description from outside | obtained | nagel1974.pdf |
| chalmers1995 | the easy/hard split; the hard problem asks why processing is accompanied by experience | obtained | chalmers1995.pdf |
| frankish2016 | illusionism; the illusion problem as successor of the hard problem | obtained | frankish2016.pdf |
| dennett1991 | user illusion; the regress objection; self-report as misrepresentation | unverified | - |
| ryle1949 | the regress objection against inner observation | unverified | - |
| rosenthal2005 | higher-order thought structure; a frame as a thought within a previous one | substitute | rosenthal2009.pdf (Oxford Handbook chapter) |
| lau2011 | empirical support for higher-order theories | unverified | - |
| tononi2015 | differences of experience follow differences of cause-effect structure | obtained | tononi2015.xml |
| metzinger2003 | phenomenal transparency: the self-model cannot be seen as a model | substitute | metzinger2005.pdf (Précis of Being No One) |
| graziano2011 | attention schema as the system's model of its own attention | obtained | graziano2011.pdf |
| graziano2013 | the same, book-length | unverified | - |
| varela1991 | constraints as the body of a computation (embodied cognition) | unverified | - |
| ayer1936 | emotivism: moral terms express attitude | obtained | ayer1936.pdf |
| locke1690 | the inverted spectrum, Essay II.xxxii.15, and Locke's closing it as idle | verified | - (Gutenberg text, locus checked) |
| fodor1987 | the word "psychosemantics" is taken for a different project | unverified | - |
| gardner1983 | intrapersonal intelligence as a distinct ability | unverified | - |
| solomonoff1964a | universal prediction with feedback; program induction; algorithmic probability | obtained | solomonoff1964a.pdf |
| solomonoff1964b | the same, Part II | obtained | solomonoff1964b.pdf |
| levin1974 | the coding theorem K(x) = -log m(x) + O(1) | obtained | levin1974.pdf (Russian original) |
| livitanyi2019 | uncomputability of K; machine-relativity up to a constant | unverified | - |
| turing1936 | a computable function has unboundedly many implementations | obtained | turing1936.pdf |
| siegelmann1995 | recurrent networks are Turing complete under idealized assumptions | obtained | siegelmann1995.pdf |
| perez2021 | attention is Turing complete | obtained | perez2021.pdf |
| forgy1982 | RETE caches matches incrementally, which a Transformer does not | obtained | forgy1982.pdf |
| muggleton1994 | program induction has a history independent of this paper | unverified | - |
| willems1995 | context-tree weighting: universality within a class of tree sources | obtained | willems1995.pdf |
| schmidhuber2010 | compression progress as intrinsic reward | obtained | schmidhuber2010.pdf |
| dingle2018 | input-output maps are biased toward simple outputs, with a bound | obtained | dingle2018.pdf |
| valleperez2019 | the parameter-function map of deep networks is biased toward simple functions | obtained | valleperez2018.pdf |
| mingard2021 | SGD lands on functions with near-Bayesian probabilities | obtained | mingard2021.pdf |
| wolfram2002 | computational irreducibility follows from bounded computation | obtained | wolfram2002.html |
| wolfram2020 | the Ruliad observer: bounded, coarse-graining, concluding nothing about itself | obtained | wolfram2020.html |
| wolfram2023 | a bounded observer sees a lawful world because of its bounds; the second law | obtained | wolfram2023.html |
| simon1955 | bounded rationality: limits deform choice systematically | obtained | simon1955.pdf |
| lieder2020 | resource-rational analysis: biases as optimal use of a limited budget | obtained | lieder2020.pdf |
| griffiths2015 | levels of analysis for rational use of cognitive resources | unverified | - |
| riemann1873 | the geometric idea voiced before a theory carried it | unverified | - |
| clifford1876 | space-theory of matter as a precursor of geometrized gravity | obtained | clifford1876.html |
| norton1992 | Nordström's scalar theory and where it failed | unverified | - |
| perky1910 | imagery is dimmer and less detailed than perception | obtained | perky1910.pdf |
| weiskrantz1986 | blindsight: source attribution without a manifold of elements | unverified | - |
| damasio1996 | somatic markers as an ensemble of bodily signals used in decision | obtained | damasio1996.pdf |
| cahill1998 | emotional arousal modulates lasting declarative memory | unverified | - |
| mcgaugh2000 | consolidation runs on minutes to hours and is modulated | unverified | - |
| schultz1997 | the reward signal has the form of a prediction error | obtained | schultz1997.pdf |
| scoville1957 | H.M.: real-time consciousness without accumulation | obtained | scoville1957.pdf |
| corkin2002 | the later characterization of H.M.'s deficit | unverified | - |
| miller1956 | capacity for material passing through speech, about seven items | obtained | miller1956.pdf |
| cowan2001 | the reconsidered capacity, about four | unverified | - |
| vanrullen2003 | perception is discrete and has a rate | unverified | - |
| nisbett1977 | humans misreport the causes of their own behaviour | obtained | nisbett1977.pdf |
| zwaan1998 | readers build situation models rather than storing sentences | unverified | - |
| tausczik2010 | function words and style predict psychological state | unverified | - |
| pennebaker2011 | the same, book-length | unverified | - |
| stephens2010 | speaker-listener neural coupling predicts comprehension | unverified | - |
| hasson2012 | brain-to-brain coupling as a mechanism of shared states | unverified | - |
| vygotsky1934 | inner speech as internalized dialogue | unverified | - |
| clark1998 | words as tools that reshape the computation using them | unverified | - |
| lupyan2012 | label feedback modulates perception | unverified | - |
| frank2008 | exact numerosity is impaired without number words | unverified | - |
| barsalou1999 | grounded cognition: concepts rebuilt from perceptual states | unverified | - |
| fedorenko2024 | the language network is dissociable from thought | unverified | - |
| mahowald2024 | the same distinction applied to language models | unverified | - |
| deletang2024 | prediction is compression, demonstrated with language models | obtained | deletang2023.pdf |
| nogueira2021 | Transformers do arithmetic approximately; tokenization and digit count matter | obtained | nogueira2021.pdf |
| dziri2023 | compositional tasks are solved by shortcut and degrade with depth | unverified | - |
| xie2022 | in-context learning as inference of a latent variable | unverified | - |
| vonoswald2023 | a self-attention layer can perform a gradient step on context examples | obtained | vonoswald2023.pdf |
| todd2024 | a function vector at middle depth carries an in-context mapping | obtained | todd2024.pdf |
| jastrzebski2018 | residual blocks make a network perform iterative inference | obtained | jastrzebski2018.pdf |
| nostalgebraist2020 | the logit lens decodes the residual stream at each block | obtained | nostalgebraist2020.html |
| belrose2023 | the tuned lens corrects the bias of that decoding | unverified | - |
| lad2024 | stages of inference recur across models; layers inside a stage are robust | obtained | lad2024.pdf |
| tenney2019 | a language model rediscovers the classical pipeline layer by layer | obtained | tenney2019.pdf |
| skean2025 | intermediate layers transfer best; compression against signal preservation | obtained | skean2025.pdf |
| dehghani2019 | recurrence in depth with per-position halting | obtained | dehghani2019.pdf |
| giannou2023 | looped Transformers with shared parameters | unverified | - |
| geiping2025 | a recurrent-depth model improves as it unrolls at test time, without more tokens | unverified | - |
| kohli2026 | depth extrapolation by scaling inference-time recurrence; dynamic recurrence extrapolates further; overthinking degrades predictions | verified | kohli2026.pdf (abstract; §on training strategies; overthinking in the abstract and §5) |
| hao2024 | continuous chain of thought: last hidden state fed back as input | obtained | hao2024.pdf |
| voita2020 | MDL probing charges for probe complexity; per-layer form | obtained | voita2020.pdf |
| alain2016 | linear probes on intermediate layers | obtained | alain2016.pdf |
| belinkov2022 | the methodological problems of probing | unverified | - |
| zou2023 | internal states are readable top-down | unverified | - |
| park2024 | representations of many features are linear | unverified | - |
| lanham2023 | episodes where chain of thought does not match the process | obtained | lanham2023.pdf |
| turpin2023 | unfaithful explanations in chain-of-thought prompting | unverified | - |
| roger2023 | models can hide information in generated text | unverified | - |
| schrimpf2021 | model states predict human brain responses to the same text | unverified | - |
| goldstein2022 | shared computational principles between humans and deep language models | unverified | - |
| caucheteux2022 | brains and algorithms partially converge | unverified | - |

Counts: 90 keys, 2 verified, 46 obtained, 2 substitutes, 40 unverified.

Procedure for the remaining rows: (1) find an open copy (author page, arXiv, PhilPapers, Internet Archive, publisher
OA); (2) save it as `sources/<key>.pdf` or `.html`; (3) read the passage that carries the claim in the column above;
(4) set the status and note the locus; (5) if the source does not support the claim, mark `not-supporting` and change
the sentence in the section file that cites it. A `substitute` row has to end either as a citation of what was read or
as a copy of the original.

`sources/webb2015.pdf` was downloaded by the verification agents and is not cited by the current text.
