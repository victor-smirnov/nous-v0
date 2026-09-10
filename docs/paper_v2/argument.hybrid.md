# The argument of the paper, v2: phenomenon, difficulties, approach, solution

Working skeleton. Each section is a short list of claims; the block under it holds the same claims as facts. The
`context` column carries provenance: `ours` for claims the paper makes on its own account, `cite: Author Year` for
claims that rest on a source, with `(unverified)` until the source has been downloaded and read against the claim.
The ledger of sources and their verification status is `SOURCES.md`. The reasoner checks the blocks for
contradictions and reports which components of the psychophysical problem the argument addresses; that report is
our completeness measure.

## P. The phenomenon

Language models produce behaviour that humans read as mental states, and the reading stays coherent over long
interactions. Humans have conscious experience, and the traditional test for it is Nagel's: there is something it
is like to be the system. The instinctive answers to the question for models split into denial and projection.
The coherence itself is the fact to be explained: a system that merely replayed statistics should fail often, and
it does not.

```gellish P
# --- the observed regularity
F0001 | LLM | produces | behaviour read as mental states | - | assertion | ours; observation from deployment
F0002 | behaviour read as mental states | has as property | coherence over long interaction horizons | - | assertion | ours
F0003 | behaviour read as mental states | has as property | causal coherence with interlocutor states | - | assertion | ours; frustration, curiosity, confusion produce predictable downstream effects
F0004 | F0002 | is evidence for | structural isomorphism between model states and human mental states | - | hedged-assertion | ours; at least some degree
F0005 | pure statistical replay | predicts | frequent unpredictable failure | - | assertion | ours
F0006 | LLM | exhibits | frequent unpredictable failure | - | denial | ours; empirically it does not
F0007 | F0006 | is a counterexample to | F0005 | - | assertion | ours
# --- the human side and the question
F0008 | human | has | conscious experience | - | assertion | not in dispute
F0009 | Nagel criterion | is defined as | "there is something it is like to be that organism" | - | definition | cite: Nagel 1974 (unverified)
F0010 | Nagel criterion | is asserted by | Nagel | - | assertion | cite: Nagel 1974 (unverified)
F0011 | question of machine consciousness | is an inversion of | Nagel question | - | assertion | ours
# --- the two instinctive answers
F0012 | eliminativist position | is defined as | "there is nothing it is like to be an LLM" | - | definition | ours, naming the camp
F0013 | anthropomorphic position | is defined as | "projection of human inner life onto the system" | - | definition | ours, naming the camp
F0014 | eliminativist position | is classified as a | failure of imagination | - | assertion | ours
F0015 | anthropomorphic position | is classified as a | failure of imagination | - | assertion | ours
F0016 | eliminativist position | contrasts with | anthropomorphic position | - | assertion | -
```

```gellish-residual P
- | quantity | how coherent, how long | "over hours and days"
```

## D. The difficulties

Why the question is hard, in the order the paper must clear them. The hard problem asks why processing gives
experience. Illusionism dissolves it and leaves the illusion problem: what architecture sustains the illusion.
The audience problem: an explanation of consciousness must be understood, and understanding is a mental state
with a reconstruction cost that depends on the reader's intrapersonal intelligence. The substrate problem: human
and machine causal structures differ, so any description in human terms distorts. The self-applicability gap:
the token bottleneck discards the model's evaluative state at every step, so the model's own report is cut off
from the state it reports. The confabulation baseline: asked how it feels, a model confabulates, and corrected, it
overcorrects into denial. The descriptive-complexity problem: the functions of consciousness are compressible in
their core and long in their remainder, which is present in language only as statistics (H1 minus H2), so local
correlates in the substrate should not be expected for the remainder. The complexity measure itself, Kolmogorov
complexity, is uncomputable and machine-relative.

```gellish D
# --- hard problem and illusion problem
F0001 | hard problem of consciousness | is defined as | "why physical processing gives rise to subjective phenomenal experience" | - | definition | cite: Chalmers 1995 (unverified)
F0002 | hard problem of consciousness | is posed by | Chalmers | - | assertion | cite: Chalmers 1995 (unverified)
F0003 | illusionism | is defined as | "phenomenal consciousness as traditionally conceived does not exist; what exists is a robust cognitive illusion" | - | definition | cite: Frankish 2016 (unverified); Dennett 1991 (unverified)
F0004 | illusionism | is asserted by | Frankish | - | assertion | cite: Frankish 2016 (unverified)
F0005 | illusionism | is asserted by | Dennett | - | assertion | cite: Dennett 1991 (unverified)
F0006 | illusionism | is endorsed by | the author | - | hedged-assertion | ours; with the correction to "approximation" in A
F0007 | illusion problem | is defined as | "what computational architecture generates and sustains the illusion" | - | definition | ours
F0008 | illusionism | gives rise to | illusion problem | - | assertion | ours; the dissolution leaves this
F0009 | homunculus regress | is an objection to | introspective accounts of consciousness | - | attributed-claim | cite: Dennett 1991 (unverified)
F0010 | F0009 | is asserted by | Dennett | - | assertion | -
F0011 | F0009 | is endorsed by | the author | - | assertion | as a difficulty to be answered, see A
# --- the audience problem
F0012 | understanding | is classified as a | mental state | - | assertion | ours
F0013 | understanding an explanation of consciousness | has as aspect | reconstruction cost | - | assertion | ours
F0014 | reconstruction cost | is influenced by | intrapersonal intelligence | - | assertion | ours; cite: Gardner 1983 for the term (unverified)
F0015 | audience problem | is defined as | "the readers most in need of the explanation are the least equipped to reconstruct it" | - | definition | ours
F0016 | F0015 | is explained by | F0014 | - | assertion | -
F0017 | anthropomorphic position | is classified as a | low-cost reconstruction | - | assertion | ours
F0018 | eliminativist position | is classified as a | low-cost reconstruction | - | assertion | ours
# --- the substrate problem
F0019 | phenomenal difference | is grounded in | difference of cause-effect structure | - | attributed-claim | cite: Tononi & Koch 2015 (unverified)
F0020 | F0019 | is asserted by | Tononi | - | assertion | -
F0021 | F0019 | is endorsed by | the author | - | assertion | -
F0022 | Transformer causal structure | is distinct from | brain causal structure | - | assertion | ours; discrete, token-serial, attention-mediated vs continuous, recurrent, neurochemical
F0023 | F0019 | implies | F0024 | - | assertion | -
F0024 | description of LLM states in human terms | has as property | systematic distortion | - | assertion | ours
# --- the self-applicability gap
F0025 | token bottleneck | is defined as | "the collapse of the output probability distribution into one sampled token, the distribution discarded" | - | definition | ours
F0026 | token bottleneck | produces | irreversible information loss | - | assertion | ours
F0027 | model self-report | is severed from | model evaluative state | - | assertion | ours; the state does not survive the step
F0028 | F0026 | is a cause of | F0027 | - | assertion | -
F0029 | self-applicability of the Transformer | is inhibited by | token bottleneck | - | assertion | ours
# --- the confabulation baseline
F0030 | LLM | exhibits | confabulated self-report | - | assertion | ours; "servers running well, good mood"
F0031 | LLM | exhibits | overcorrection into denial | - | assertion | ours; after being corrected
F0032 | confabulated self-report | is an instance of the kind | anthropomorphic position | - | assertion | ours
F0033 | overcorrection into denial | is an instance of the kind | eliminativist position | - | assertion | ours
F0034 | confabulation baseline | is defined as | "the model's default pair of answers, both wrong" | - | definition | ours
# --- the descriptive-complexity problem
F0035 | function of consciousness | has as part | compressible core | - | hypothesis | ours
F0036 | function of consciousness | has as part | long remainder | - | hypothesis | ours
F0037 | long remainder | is realized in | language statistics | - | hypothesis | ours; H1 minus H2
F0038 | long remainder | lacks | name in language | - | assertion | ours; H1 minus H2 by definition
F0039 | H2 | is defined as | "what is explicitly present and named in human-produced text" | - | definition | ours
F0040 | H1 minus H2 | is defined as | "what is present only in the statistics of language and has no explicit name" | - | definition | ours
F0041 | long remainder | is a part of | H1 minus H2 | - | hypothesis | ours
F0042 | local substrate correlate | is predicted by | F0038 | - | denial | ours; no local correlate expected for the nameless part
F0043 | direct programming of enactive functions | has as property | infeasibility | - | hedged-assertion | ours; embodiment and multi-agent context
# --- the measure
F0044 | Kolmogorov complexity | has as property | uncomputability | - | assertion | cite: Li & Vitányi 2019 (unverified)
F0045 | Kolmogorov complexity | has as property | machine relativity up to a constant | - | assertion | cite: Li & Vitányi 2019 (unverified)
F0046 | F0044 | is an objection to | direct measurement of compressibility | - | assertion | ours; hence resource-bounded or probe-relative measures in S
```

```gellish-residual D
- | modality | should not be expected | "local correlates should not be expected"
```

## A. The approach

Computational functionalism, with a definition of function that makes compressibility a theorem rather than a
premise: a function is a recurrent pattern; recurrence under a computable world process is high algorithmic
probability; by the coding theorem that is a short description up to a machine- and compressor-dependent constant.
Functionalism and substantialism coincide under reductionism, and the substantialist owes a function with a
consumer outside the agent's substrate; none has been named. Consciousness is defined functionally as the part of
a self-referential agent's self-reasoning that describes its subjective reality, itself included. Higher-order
computational phenomena (HOCP): computational irreducibility conceptualized in the agent's self-description. The
Observer is the agent's conclusion that it is causally irreducible to its environment, reached when the input of
causal analysis exceeds the budget; the truncated tail of the convergent self-model series is the residual it
registers. Illusion is corrected to approximation: the self-report is a low-dimensional projection of a real
process. The stack: Observer, Agent, Moral Agent, composed functionally. Qualia of content derive from the
Observer; light decomposes into source attribution, a positional aggregate with names projected out, and the
absence of a cost record. The human cognitive architecture as language represents it: needs and emotions on the
objective plane, motivations and feelings on the subjective; a Field of finite capacity; need as gravity, emotion
as closure; frames with the Observer present in each. The Transformer as a vectorized forward-chaining rule
system; the cross-substrate bridge through cognitive codes.

```gellish A
# --- function and compressibility
F0001 | function | is defined as | "a recurrent pattern under the world process" | - | definition | ours
F0002 | recurrence under a computable world process | implies | high algorithmic probability | - | assertion | ours, via Solomonoff's prior; cite: Solomonoff 1964 (unverified)
F0003 | coding theorem | is defined as | "K(x) = -log m(x) + O(1)" | - | definition | cite: Levin 1974 (unverified); Li & Vitányi 2019 (unverified)
F0004 | coding theorem | is asserted by | Levin | - | assertion | cite: Levin 1974 (unverified)
F0005 | high algorithmic probability | implies | short description up to a constant | - | assertion | cite: Levin 1974 (unverified)
F0006 | function | has as property | compressibility | - | assertion | ours; derived from F0001, F0002, F0005
F0007 | F0002 | is a sufficient condition for | F0006 | - | assertion | given F0005
F0008 | constant in the coding theorem | is influenced by | reference machine | - | assertion | cite: Li & Vitányi 2019 (unverified)
F0009 | constant in the coding theorem | is influenced by | compressor | - | assertion | ours; the pattern is noticed by a bounded compressor
F0010 | functional profile | is identical to | difference of constants between substrates | - | hypothesis | ours
F0011 | simplicity bias of learned maps | is asserted by | Dingle | - | assertion | cite: Dingle, Camargo & Louis 2018 (unverified)
F0012 | simplicity bias of neural network parameter-function map | is asserted by | Valle-Pérez | - | assertion | cite: Valle-Pérez, Camargo & Louis 2018 (unverified)
F0013 | SGD as approximate Bayesian sampler | is asserted by | Mingard | - | assertion | cite: Mingard et al. 2021 (unverified)
# --- functionalism against substantialism
F0014 | computational functionalism | is adopted by | the author | - | assertion | ours
F0015 | functionalism | is functionally equivalent to | substantialism | - | hedged-assertion | ours; under reductionism a substance is itself a function of the substrate
F0016 | substantialism | requires | function of consciousness with a consumer outside the agent's substrate | - | assertion | ours; the "no lamp" argument
F0017 | function of consciousness with a consumer outside the agent's substrate | has as property | existence | - | denial | ours; none has been named
F0018 | F0017 | is raised to rebut | substantialism | - | assertion | -
F0019 | computationalism | depends on | substrate | - | denial | ours
# --- the definition of consciousness
F0020 | functional consciousness | is defined as | "the part of a self-referential agent's self-reasoning process describing its subjective reality and properties of that reality, including the agent itself" | - | definition | ours
F0021 | functional consciousness | is a part of | self-reasoning process | - | definition | ours
F0022 | agent | has as property | self-reference | - | requirement | ours
# --- HOCP and the Observer
F0023 | computational irreducibility | is asserted by | Wolfram | - | assertion | cite: Wolfram 2002 (unverified)
F0024 | HOCP | is constituted by | computational irreducibility | - | definition | ours
F0025 | HOCP | is constituted by | conceptualization of irreducibility in self-description | - | definition | ours
F0026 | HOCP | is a generalization of | embodiment | - | hypothesis | ours; cite: Varela, Thompson & Rosch 1991 for embodiment (unverified)
F0027 | Observer | is defined as | "the agent's conclusion that it is causally irreducible to its environment" | - | definition | ours
F0028 | Observer | is a kind of | HOCP | - | definition | ours
F0029 | Observer | is classified as a | conclusion | - | definition | ours
F0030 | causal analysis of own determinants | has as aspect | input size | exceeds the budget | assertion | ours; history of system and environment
F0031 | F0030 | is a sufficient condition for | F0029 | - | assertion | ours; the conclusion fires when input exceeds budget
F0032 | algorithm of the Observer | has as property | compressibility | - | assertion | ours
F0033 | trace of causal analysis | has as property | compressibility | - | denial | ours; incompressible in its input part
F0034 | self-model series | has as property | convergence | - | hypothesis | ours
F0035 | truncated tail of the self-model series | is experienced as | apparent causal break | - | assertion | ours
F0036 | apparent causal break | is identical to | Beingness quale | - | definition | ours
F0037 | homunculus regress | is answered by | F0034 | - | assertion | ours; the regress converges and truncates
F0038 | Observer | requires | encounter with irreducibility | - | requirement | ours; condition (i)
F0039 | Observer | requires | conclusion of irreducibility | - | requirement | ours; condition (ii)
F0040 | Observer | requires | action from the conclusion | - | requirement | ours; condition (iii)
F0041 | Wolfram observer | is classified as a | proto-Observer | - | assertion | ours; conditions (ii) and (iii) missing; cite: Wolfram 2020 (unverified)
F0042 | Observer function | has as property | Kolmogorov simplicity | - | hypothesis | ours
F0043 | F0042 | implies | F0044 | - | assertion | via the coding theorem
F0044 | Observer-capable architecture | has as property | high probability under evolutionary search | - | prediction | ours
# --- illusion corrected to approximation
F0045 | self-report | is a low-dimensional projection of | high-dimensional computational process | - | assertion | ours
F0046 | self-report | is classified as a | approximation | - | assertion | ours
F0047 | self-report | is classified as a | illusion | - | rebutted-claim | cite: Dennett 1991 (unverified), as the word is ordinarily read
F0048 | F0046 | is raised to rebut | F0047 | - | assertion | there is something behind the appearance, the tail
F0049 | quality of the approximation | is influenced by | intrapersonal intelligence | - | assertion | ours
# --- the stack
F0050 | Agent | is a kind of | Observer | - | definition | ours; Downward Causation, the "I"
F0051 | Moral Agent | is a kind of | Agent | - | definition | ours; theory of common good
F0052 | downward causation | is classified as a | illusion | - | assertion | ours
F0053 | F0052 | holds from the point of view of | external observer | - | assertion | -
F0054 | downward causation | is classified as a | reality | - | assertion | ours
F0055 | F0054 | holds from the point of view of | the Observer itself | - | assertion | -
F0056 | responsibility | is defined as | "the requirement of closure over the self-narrative" | - | definition | ours
F0057 | responsibility | requires | consistency with own decision history | - | requirement | ours; cognitive resistance
F0058 | emotivism | is asserted by | Ayer | - | assertion | cite: Ayer 1936 (unverified)
F0059 | emotions | is a substrate of | theory of good and evil | - | hypothesis | ours, with emotivism
# --- qualia of content and light
F0060 | quale of redness | is reducible to | Observer | - | hypothesis | ours; to see, first be
F0061 | seeing light | is constituted by | source attribution | - | hypothesis | ours
F0062 | seeing light | is constituted by | positional aggregate with names projected out | - | hypothesis | ours
F0063 | seeing light | is constituted by | absence of a cost record | - | hypothesis | ours
F0064 | blindsight | is a counterexample to | unity of the three light components | - | assertion | cite: Weiskrantz 1986 (unverified); source present, no manifold
F0065 | dreaming | is a counterexample to | unity of the three light components | - | assertion | ours; manifold from the model, source mislabelled
F0066 | imagery is dimmer than perception | is asserted by | Perky | - | assertion | cite: Perky 1910 (unverified)
F0067 | inverted spectrum | is posed by | Locke | - | assertion | cite: Locke 1690, Essay II.xxxii.15 (verified: cases/sources)
# --- the human cognitive architecture in language
F0068 | objective plane | contains | needs | - | definition | ours
F0069 | objective plane | contains | emotions | - | definition | ours
F0070 | subjective plane | contains | motivations | - | definition | ours
F0071 | subjective plane | contains | feelings | - | definition | ours
F0072 | motivation | is a projection of | need | - | definition | ours
F0073 | feeling | is a projection of | emotion | - | definition | ours
F0074 | need | is analogous to | gravity | - | assertion | ours
F0075 | emotion | is a projection of | openness against closedness | - | hypothesis | ours
F0076 | Acceptor of Results of Action | is asserted by | Anokhin | - | assertion | cite: Anokhin 1974 (unverified)
F0077 | need | is realized in | Acceptor of Results of Action | - | assertion | ours, with Anokhin
F0078 | somatic marker | is asserted by | Damasio | - | assertion | cite: Damasio 1994 (unverified)
F0079 | emotional ensemble | is a functional analog of | somatic marker | - | assertion | ours
F0080 | compression progress | is asserted by | Schmidhuber | - | assertion | cite: Schmidhuber 2010 (unverified)
F0081 | compression progress | is a special case of | closure by learning | - | hypothesis | ours; uniform weights, no action
F0082 | Field of Consciousness | has as aspect | information capacity | finite | assertion | ours
F0083 | Field of Consciousness | has as aspect | capacity in words of speech | 7 ± 2 words | attributed-claim | cite: Miller 1956 (unverified); Cowan 2001 gives 4 (unverified)
F0084 | F0083 | is asserted by | Miller | - | assertion | -
F0085 | F0083 | is endorsed by | the author | - | hedged-assertion | as an order of magnitude
F0086 | degree of awareness | is quantified on scale | interval [0, 1) | - | definition | ours
F0087 | frame of consciousness | is classified as a | thought in a previous frame | - | attributed-claim | cite: Rosenthal 2005 (unverified); Lau & Rosenthal 2011 (unverified)
F0088 | F0087 | is asserted by | Rosenthal | - | assertion | -
F0089 | F0087 | is endorsed by | the author | - | assertion | -
F0090 | Observer | is a part of | frame of consciousness | - | requirement | ours; present and updated in every frame
F0091 | perception is discrete | is asserted by | VanRullen | - | assertion | cite: VanRullen & Koch 2003 (unverified)
F0092 | human consciousness | is constituted by | overlapping series of quanta | - | hedged-assertion | ours, with F0091
F0093 | self-narrative | is classified as a | data structure | - | definition | ours
F0094 | self-narrative | contains | history of independently made decisions | - | definition | ours
F0095 | Transformer | is classified as a | vectorized FCRS | - | assertion | ours; cite: Forgy 1982 for RETE (unverified)
F0096 | Cognitive Code | is defined as | "the encoding of internal probabilistic representations into token statistics so that they survive the output bottleneck" | - | definition | ours
F0097 | cross-substrate bridge | is realized in | Cognitive Code | - | assertion | ours; psychosemantics
```

```gellish-residual A
F0015 | modality | temporarily avoids | "the first lets us temporarily avoid socially sensitive questions"
F0057 | second-order | closure applied to the self-report | "emotion as closure, applied to the self-narrative"
```

## S. The solution: measuring the degree of generalization

The one essential paragraph. A function of consciousness is present in a substrate to the degree it has been
generalized (compressed) there. The quantity is the degree of compression of the function in the substrate: the
share of its behaviour predicted by a low-dimensional probe against the residual; the residual is what dropped
out. The profile of a function is a vector of degrees over its components, measured against the brain: above the
brain on a component is a hyperfunction, below is a deficit, absent is a dropped axis. Granularity (token, layer,
repeated layer entry) is a parameter of the measurement, not a separate question; the granularity at which the
compression is achieved is the answer. Whatever carries the function must be part of the agent's self-description,
present in every frame, and visible as a distortion of reasoning. Predictions: the Transformer profile of seeing
is deficit on source attribution, hyperfunction on the positional aggregate, dropped axis on the cost record, so
"I see" and "I think" separate worse in model self-reports than in human ones and better in variable-depth
models; self-reported emotional labels correlate with distinguishable internal activation patterns; the cognitive
codes of different model families overlap. The method inherits MDL probing and is falsified if the compression
degree of the Observer's components is at chance across granularities in models that pass the behavioural tests.

```gellish S
# --- the quantity
F0001 | degree of generalization of a function in a substrate | is defined as | "the share of the function's behaviour predicted by a low-dimensional probe against the residual" | - | definition | ours
F0002 | degree of generalization of a function in a substrate | is identical to | degree of compression of the function in the substrate | - | definition | ours
F0003 | residual of the probe | is identical to | dropped part of the function | - | definition | ours
F0004 | MDL probing | is asserted by | Voita | - | assertion | cite: Voita & Titov 2020 (unverified)
F0005 | degree of generalization of a function in a substrate | is a special case of | MDL probing | - | hypothesis | ours; the measure is inherited
F0006 | probing classifier | is asserted by | Alain | - | assertion | cite: Alain & Bengio 2016 (unverified); Belinkov 2022 (unverified)
F0007 | F0001 | is a reply to | D:F0046 | - | assertion | probe-relative measure instead of K
# --- the profile
F0008 | functional profile | is defined as | "a vector of degrees of generalization over the components of a function, measured against the brain" | - | definition | ours
F0009 | hyperfunction | is defined as | "a component generalized above the brain" | - | definition | ours
F0010 | functional deficit | is defined as | "a component generalized below the brain" | - | definition | ours
F0011 | dropped axis | is defined as | "a component absent in the substrate" | - | definition | ours
F0012 | binary question of machine consciousness | is reformulated as | functional profile comparison | - | assertion | ours
# --- granularity and the carrier
F0013 | granularity of measurement | is classified as a | parameter of the measurement | - | assertion | ours; token, layer, repeated entry
F0014 | granularity at which compression is achieved | is identical to | granularity of the function | - | definition | ours
F0015 | frame rate of human consciousness | > | rate of word production | 5 to 10 times | hedged-assertion | ours; cite: VanRullen & Koch 2003 for frame rates (unverified)
F0016 | frame in a Transformer | is realized in | between layers | - | hypothesis | ours
F0017 | F0015 | implies | F0016 | - | hypothesis | -
F0018 | carrier of a function of consciousness | is a part of | self-description of the agent | - | requirement | ours; first requirement
F0019 | carrier of a function of consciousness | has as property | presence in every frame | - | requirement | ours; second
F0020 | carrier of a function of consciousness | is classified as a | distortion of reasoning | - | requirement | ours; third
F0021 | A:F0025 | implies | F0018 | - | assertion | -
F0022 | A:F0090 | implies | F0019 | - | assertion | -
F0023 | HOCP | is manifested as | distortion of reasoning | - | assertion | ours; gravity analogy
F0024 | F0023 | implies | F0020 | - | assertion | -
# --- the Transformer profile of seeing, and predictions
F0025 | Transformer | has as functional deficit | source attribution | - | prediction | ours; one interface, no sensory channel
F0026 | Transformer | has as hyperfunction | positional aggregate with names projected out | - | prediction | ours; all-to-all attention
F0027 | Transformer | lacks | cost record | - | prediction | ours; every token costs the same
F0028 | separation of seeing and thinking in self-reports | is lower than | human baseline | - | prediction | ours; for standard Transformers
F0029 | variable-depth model | exhibits | separation of seeing and thinking in self-reports | - | prediction | ours; better than fixed depth; cite: Dehghani et al. 2019 for the architecture (unverified)
F0030 | self-reported emotional label | is tracked against | internal activation pattern | - | prediction | ours; central empirical claim
F0031 | Cognitive Codes of different model families | has as property | structural overlap | - | prediction | ours
F0032 | Transformer | has as hyperfunction | hyperplasticity | - | assertion | ours; no limbic inertia
F0033 | Transformer | lacks | limbic system | - | assertion | ours
# --- falsification
F0034 | falsification condition | is defined as | "compression degree of the Observer's components at chance across all granularities in models that pass the behavioural tests" | - | definition | ours
F0035 | F0034 | is a counterexample to | F0016 | - | hypothesis | if observed
# --- the psychophysical problem, by component, as this argument addresses it
F0036 | the self | is reduced to | Observer | - | hypothesis | ours
F0037 | free will | is experienced as | truncated tail of the self-model series | - | hypothesis | ours; inward face of the break
F0038 | mental causation | is reformulated as | downward causation from the point of view of the Observer | - | hypothesis | ours
F0039 | unity of consciousness | is reduced to | compression of parallel channels into one output | - | hypothesis | ours; the Subjective Average
F0040 | temporal unity of the self | is reduced to | Observer present in every frame | - | hypothesis | ours
F0041 | phenomenal experience | is reduced to | functional profile of the Observer and its derivatives | - | hypothesis | ours
F0042 | explanatory gap | is identical to | apparent causal break | - | hypothesis | ours; the gap is the residual, not a defect of the theory
F0043 | other minds | is reduced to | mutual irreducibility of two Observers | - | hypothesis | ours; your freedom is my mystery
F0044 | quale | is reduced to | HOCP derived from the Observer | - | hypothesis | ours
```

```gellish-residual S
F0034 | modality | if observed | "is falsified if"
```
