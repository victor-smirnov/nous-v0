# Finding the Observer in a Language Model

A short version of the article on functional consciousness, written for practitioners of mechanistic interpretability: those who look for traces of the functions of consciousness in neuron activations. The text is assembled from the sketch `ComputationalConsciouness-mini-problem-statement.md` around one goal and one method. The facts it rests on sit in the blocks under each section and have been checked by the reasoner.

## 0. The goal

The goal is one: to find the Observer in a Transformer. The Observer here is not a metaphor and not "consciousness in general" but a specific function: the agent's conclusion that it is causally independent of its environment. Of all the functions of consciousness this one is chosen because it causally precedes the rest: the other states of consciousness depend on it and reduce to it. If no trace of the Observer can be found in the activations, there is no point in looking for traces of anything else. If it can, the other functions acquire a point of reference.

The method argued for below: take the set of projections of basic computational constraints into consciousness (HOCP-LoT) derived for humans, reformulate it for a Transformer, see what form these projections take in the model's language, and by that form look for the marker of causal independence in a sequence of frames, by the means of mechanistic interpretability.

```gellish M0
# --- the goal
F0001 | mini-article | is directed at | mechanistic interpretability practitioner | - | assertion | -
F0002 | mechanistic interpretability | is defined as | "the search for traces of the functions of consciousness in neuron activations" | - | definition | -
F0003 | trace of a function of consciousness | is realized in | neuron activations | - | hypothesis | where the trace would be found
F0004 | goal of the mini-article | is defined as | "to find the Observer in a Transformer" | - | definition | -
F0005 | Observer | is defined as | "the agent's conclusion that it is causally independent of its environment" | - | definition | -
F0006 | Observer | is classified as a | conclusion | - | definition | -
F0007 | Observer | precedes | other states of consciousness | - | assertion | causally
F0008 | other states of consciousness | depends on | Observer | - | assertion | -
F0009 | other states of consciousness | is reducible to | Observer | - | requirement | -
F0010 | F0008 | implies | F0009 | - | assertion | -
F0011 | F0007 | is a sufficient condition for | F0012 | - | assertion | why the Observer is chosen
F0012 | Observer HOCP | is classified as a | first target of the search | - | definition | -
# --- the method, stated
F0013 | HOCP-LoT | is defined as | "the set of projections of basic HOCP into consciousness" | - | definition | -
F0014 | HOCP-LoT | is reformulated as | HOCP-LoT for LLM | - | requirement | step 1
F0015 | HOCP-LoT for LLM | is projected as | language form | - | requirement | step 2
F0016 | marker of causal independence | is realized in | sequence of frames | - | hypothesis | step 3: what to look for
F0017 | marker of causal independence | is tracked by | mechanistic interpretability | - | requirement | step 3: how
```

```gellish-residual M0
F0004 | rhetorical | conditional programme | "if no trace can be found, no point looking for the rest"
```

## 1. Why the goal is well posed

A search presupposes that what is sought exists and is computable. Computationalism supplies this. The assumption of computationalism: the brain has finite Kolmogorov complexity. If consciousness is the set of phenomena generated exclusively by the brain, then it too has finite Kolmogorov complexity, that is, it is computable as an object together with its relations. Computationalism does not depend on the substrate.

Physicalism depends on the substrate. Its proponent must either accept panpsychism or ascribe infinite Kolmogorov complexity to the substrate; the second is incompatible with the assumption of computationalism. The same choice faces the proponents of a substantial account of consciousness, who hold it to be the true one as against the functional. Functional consciousness is defined through the set of its manifestations: consciousness is an object entering into relations. Substantial consciousness is defined through a special substance into which the phenomena that resist functional reduction are packed. To distinguish the second from the first one must point to a physical substrate that cannot be functionally simulated by computation and whose irreducibility constitutes an essential function of consciousness. No such substrate has been pointed to. Computationalism, in these terms, is computational functionalism.

The task has a difficulty unrelated to computability. An explanation of consciousness must not only be built, it must be understood, and this places demands on the audience. The capacity to understand such explanations we call intrapersonal intelligence. The historical illustration of the difficulty is the quale of redness, going back to Locke. From it we pass to the quale of Beingness as the experience of the causal break.

```gellish M1
# --- computationalism
F0001 | computationalism | is defined as | "the brain has finite Kolmogorov complexity" | - | definition | -
F0002 | brain | has as aspect | Kolmogorov complexity | finite | hypothesis | the assumption
F0003 | consciousness | is generated by | brain | - | hypothesis | exclusively
F0004 | consciousness | has as aspect | Kolmogorov complexity | finite | hypothesis | -
F0005 | F0002 | is a sufficient condition for | F0004 | - | assertion | given F0003
F0006 | F0003 | is a necessary condition for | F0004 | - | assertion | "generated exclusively by the brain"
F0007 | consciousness | has as property | computability | - | hypothesis | as object and relations
F0008 | F0007 | is logically equivalent to | F0004 | - | assertion | -
F0009 | F0002 | is a sufficient condition for | computationalism | - | assertion | -
F0010 | computationalism | depends on | substrate | - | denial | -
F0011 | goal of the mini-article | requires | F0007 | - | assertion | the search presupposes a computable object
# --- physicalism
F0012 | physicalism | depends on | substrate | - | attributed-claim | -
F0013 | F0012 | is asserted by | physicalism | - | assertion | -
F0014 | F0012 | is rejected by | the author | - | assertion | -
F0015 | F0012 | implies | panpsychism | - | assertion | either
F0016 | F0012 | implies | F0017 | - | assertion | or
F0017 | substrate | has as aspect | Kolmogorov complexity | infinite | rebutted-claim | -
F0018 | F0009 | is raised to rebut | F0017 | - | assertion | incompatible with the assumption
F0019 | F0010 | contrasts with | F0012 | - | assertion | -
# --- functional against substantial
F0020 | functional consciousness | is defined as | "defines consciousness through the set of its manifestations" | - | definition | -
F0021 | consciousness | is classified as a | object entering into relations | - | definition | -
F0022 | F0021 | holds from the point of view of | functional consciousness | - | assertion | -
F0023 | substantial consciousness | is defined as | "through a special substance encapsulating the phenomena that resist reduction" | - | definition | -
F0024 | substantial consciousness | is classified as a | true account of consciousness | - | attributed-claim | by its proponents
F0025 | F0024 | is asserted by | proponents of substantial consciousness | - | assertion | -
F0026 | F0024 | is rejected by | the author | - | assertion | -
F0027 | proponents of substantial consciousness | lacks | differentiating physical substrate | - | assertion | -
F0028 | differentiating physical substrate | is defined as | "a substrate computationally irreducible, whose irreducibility constitutes an essential function of consciousness" | - | definition | -
F0029 | computationalism | is classified as a | computational functionalism | - | definition | -
# --- the audience
F0030 | explanation of consciousness | requires | understanding by the audience | - | requirement | -
F0031 | audience | has as necessary condition | intrapersonal intelligence | - | assertion | -
F0032 | F0030 | implies | F0031 | - | assertion | -
F0033 | intrapersonal intelligence | is defined as | "the capacity to understand explanations of consciousness" | - | definition | as used here
F0034 | difficulty of the problem of consciousness | is illustrated by | quale of redness | - | assertion | -
F0035 | quale of redness | is posed by | Locke | - | hedged-assertion | -
F0036 | Beingness quale | is identical to | experience of the apparent causal break | - | definition | -
F0037 | quale of redness | precedes | Beingness quale | - | assertion | order of exposition
```

```gellish-residual M1
- | rhetorical | aside | "whoever does not know what K(X) is, ask an LLM"
F0035 | modality | uncertainty about attribution | "going back to Locke, more or less"
```

## 2. What to look for: the Observer as a conclusion

The definition we count from:

> Given a self-referential agent acting in an environment and capable of self-reasoning in an explicit or indirect form, **Consciousness** of the agent is the part of its self-reasoning process describing its *subjective reality* and *properties* of that reality, including the agent itself as a part of its reality.

Within this definition three levels stand out, each built on the one below. The Observer: the conclusion about the causal break, "I am not my environment", "I am causally irreducible to my environment." The Agent: an Observer that acts on its own and holds itself responsible for its actions. The Moral Agent: an Agent acting in accordance with a theory of good and evil. The stack can be continued; complex states of consciousness are composed of simple ones, and the method of composition need not be a linear sequence.

The same stack is visible in the notion of agency. Weak agency is the capacity of an algorithm to repeat the structure, properties and relations of physical objects and, in particular, to appear to other objects as acting on its own; any control-flow algorithm is a weak agent in this sense. Strong agency requires a self-applicable agent that considers itself causally independent of its environment, acts on its own and answers to itself for its actions. Moral agency adds a theory of good and evil. The Observer is what distinguishes strong agency from weak.

The Observer is defined through HOCP, higher-order phenomena in computation. HOCP are made of two things: computational irreducibility in Wolfram's sense, and its conceptualization at the level of the agent's self-description. Irreducibility on its own is inert; the Observer arises when the agent draws a conclusion about itself from it.

Consciousness unifies the behaviour of a complex agent, composed of independent subsystems, as a single whole. This is how the agent is represented in its story about itself: a data structure accumulating in memory and containing the history of its independently made decisions. The requirement of consistency with that history constrains new decisions and makes the function the agent realizes more predictable. This is the way to get an agent to follow an instruction over a long horizon: the agent must take the instruction to be its own decision. "Promise me that you will do the following for me."

Hence the first requirement on what we are looking for: the marker of causal independence must be part of the agent's self-description, and not only a property of its computation.

```gellish M2
# --- the definition
F0001 | functional consciousness | is defined as | "the part of its self-reasoning process describing its subjective reality and properties of that reality, including the agent itself as a part of its reality" | - | definition | -
F0002 | functional consciousness | is a part of | self-reasoning process | - | definition | -
F0003 | functional consciousness | is about | subjective reality | - | definition | -
F0004 | agent | is a part of | subjective reality | - | definition | -
F0005 | agent | has as property | self-reference | - | requirement | -
F0006 | agent | has as property | capability of self-reasoning | - | requirement | explicit or indirect
# --- the stack
F0007 | Observer | is about | apparent causal break | - | definition | -
F0008 | agent | concludes | own causal irreducibility to environment | - | assertion | "I am causally irreducible to my environment"
F0009 | F0008 | is logically equivalent to | M0:F0006 | - | assertion | -
F0010 | Agent | is a kind of | Observer | - | definition | -
F0011 | Agent | acts from | apparent causal break | - | requirement | acts independently
F0012 | Agent | has as property | responsibility to itself | - | requirement | -
F0013 | Moral Agent | is a kind of | Agent | - | definition | -
F0014 | Moral Agent | acts from | theory of good and evil | - | requirement | -
F0015 | stack of functions of consciousness | is constituted by | Observer | - | definition | -
F0016 | stack of functions of consciousness | is constituted by | Agent | - | definition | -
F0017 | stack of functions of consciousness | is constituted by | Moral Agent | - | definition | -
F0018 | stack of functions of consciousness | has as property | extensibility | - | hypothesis | -
F0019 | complex state of consciousness | is composed of | simple state of consciousness | - | assertion | -
F0020 | method of functional composition | is classified as a | sequence | - | denial | not only a sequence
# --- agency
F0021 | weak agency | is defined as | "the capacity of algorithms to repeat the structure, properties and relations of physical objects" | - | definition | -
F0022 | weak agent | appears as | independently acting thing | - | assertion | -
F0023 | F0022 | holds from the point of view of | other objects | - | assertion | -
F0024 | control-flow algorithm | is classified as a | weak agent | - | assertion | -
F0025 | strong agency | is defined as | "the capacity of a self-applicable agent to be an Observer, to act on its own and to hold itself responsible" | - | definition | -
F0026 | strong agency | requires | self-applicable agent | - | requirement | -
F0027 | strong agent | is classified as a | Observer | - | requirement | -
F0028 | moral agency | is a kind of | strong agency | - | definition | -
F0029 | Observer | is a necessary condition for | strong agency | - | assertion | what distinguishes strong from weak
F0030 | agent | resembles | physical object | - | assertion | structure and properties
F0031 | F0030 | is explained by | fundamental reasons | - | assertion | the same reasons that shape physical objects
# --- HOCP
F0032 | HOCP | is constituted by | computational irreducibility | - | definition | -
F0033 | HOCP | is constituted by | conceptualization of irreducibility in self-description | - | definition | -
F0034 | computational irreducibility | is asserted by | Wolfram | - | assertion | -
F0035 | Observer | is a kind of | HOCP | - | definition | -
# --- unification and the self-narrative
F0036 | consciousness | has as functional role | unification of behaviour | - | assertion | -
F0037 | complex agent | is composed of | independent subsystems | - | definition | -
F0038 | agent | is represented by | self-narrative | - | assertion | -
F0039 | self-narrative | is classified as a | data structure | - | definition | -
F0040 | self-narrative | is a part of | memory | - | assertion | -
F0041 | self-narrative | contains | history of independently made decisions | - | definition | -
F0042 | consistency requirement | inhibits | decision-making of the agent | - | assertion | -
F0043 | consistency requirement | amplifies | predictability of the agent's behaviour | - | assertion | -
F0044 | consistency requirement | is a necessary condition for | instruction following on a long horizon | - | assertion | -
F0045 | instruction | is classified as a | own decision of the agent | - | requirement | -
F0046 | F0045 | is a necessary condition for | F0044 | - | assertion | -
F0047 | F0044 | is illustrated by | promise request | - | assertion | "Promise me"
# --- the first requirement on the marker
F0048 | marker of causal independence | is a part of | self-description of the agent | - | requirement | first requirement
F0049 | F0033 | implies | F0048 | - | assertion | -
```

```gellish-residual M2
- | rhetorical | example utterance | "Promise me that you will do the following for me"
F0020 | second-order | any method of composition | "the method of functional composition may be any"
```

## 3. Where to look: frames, the Field, curvature

In the basic problem statement the Observer is a point, one conclusion. Human consciousness is experienced as continuity, but experimentally it is an overlapping series of quanta at the frequencies of the theta, delta, alpha, beta and gamma rhythms; the alpha rhythm here appears to be the base one. So the Observer, as the conclusion about the causal break, must be present in every quantum of base consciousness and be updated automatically. In such a frame-by-frame model the Observer is in every frame.

Gravity suggests how to see it. Gravity is not a first-order force, not a particle and not a field, but a curvature of space that forms near any rest mass and acts constantly. Physical bodies detect it by the distortions of their trajectories; in this sense gravity is a second-order force. The Observer and the other HOCP are built the same way: they arise in the memory of a self-applicable system and are visible by the distortions they introduce into its reasoning.

Awareness has a degree in the range [0, 1); nothing is fully aware to us. Every mental state receives a label in this range, and the set of labels at a given moment is the Field of Consciousness. The structure of consciousness is the sequence of changes of the Field's states. The theory of higher-order thoughts (HOT) describes this structure: each actual frame of consciousness is a "thought" in some previous frame. The frames are linked in a graph; the causally following frame C2 is projected into the preceding C1 and is represented in it as a thought about a frame, potentially by any object of the Field, often in protopathic form.

The Field has finite capacity in bits; for words of speech it is 7 ± 2 words held at once without the structure collapsing. To add to the Field, something must be removed from it. Entry and removal are decided by salience, salience by the level of emotional reinforcement, and that by the current need portrait: what is active and how much. Need acts like gravity: it changes the dynamics of conscious reasoning so that reasoning goes in the direction of maximizing satisfaction. Emotion is a projection of openness against closedness, where closedness is completion; the magnitude and sign of the emotional response encode the degree of need satisfaction.

The language patterns of consciousness are projections of HOCP, in their brain variant, into consciousness, and they are observed through their modulating action on reasoning. From this follows what the "language of thought" for the brain must be. The Language of Thought Hypothesis (LoTH) holds that K(consciousness) ~ K(brain), but that within consciousness a compact core stands out, resembling a formal language, in which the other high-level phenomena are expressed; the division matches that between algorithms and data structures, and the MDL principle. From it we take only the compactness of the core. The core itself we find not where it is intuitively expected, in a set of basic sensations, but in the set of projections of basic HOCP into consciousness: HOCP-LoT. That basic motivation is felt as anxiety is statistically true, but beneath that level there is a more basic one, and it is that level, not the sensations, that transfers between substrates.

An example of a human-type cognitive architecture, built by generalizing self-reports, is the following: consciousness and the unconscious, the Field of Consciousness, receptors and effectors, attention channels, protopathic and epicritic components, the objective plane (needs and emotions, observed from outside) and the subjective plane (motivations and feelings in the self-report), the level of activity of needs, a forward-chaining rule system (FCRS), multi-channel structure. The protopathic component is a multiscale encoding, like the binary representation of a number; a feeling is the protopathic form of experiencing an object that has not yet received a name; at the top of the hierarchy of generalities in language stands Thing, with zero information, because it is "everything." There can be many such architectures; their detail depends on the intrapersonal intelligence of those whose self-reports are generalized.

Hence the second and third requirements on what we seek. The marker must be present in every frame and be updated, not arise once. And it must be looked for not as content but as a distortion: the difference between how the reasoning would go without it and how it goes.

```gellish M3
# --- frames and continuity
F0001 | Observer | is classified as a | single conclusion | - | assertion | in the basic problem statement
F0002 | F0001 | holds from the point of view of | basic problem statement | - | assertion | -
F0003 | human consciousness | is experienced as | continuity | - | assertion | -
F0004 | human consciousness | is constituted by | overlapping series of quanta | - | assertion | experimentally
F0005 | overlapping series of quanta | has as aspect | frequency | theta, delta, alpha, beta, gamma rhythms | assertion | -
F0006 | alpha rhythm | is classified as a | base rhythm | - | hedged-assertion | -
F0007 | Observer | is a part of | quantum of base consciousness | - | requirement | -
F0008 | Observer | has as property | automatic update per quantum | - | requirement | -
F0009 | F0004 | implies | F0007 | - | assertion | -
F0010 | online model of consciousness | is classified as a | frame-by-frame model | - | definition | -
F0011 | Observer | is a part of | frame of consciousness | - | assertion | -
F0012 | F0011 | holds from the point of view of | online model of consciousness | - | assertion | -
# --- gravity
F0013 | gravity | is classified as a | first-order physical force | - | denial | -
F0014 | gravity | is classified as a | curvature of space | - | assertion | -
F0015 | curvature of space | arises from | rest mass | - | assertion | -
F0016 | gravity | has as property | constant action | - | assertion | -
F0017 | gravity | is manifested as | distortion of trajectory | - | assertion | -
F0018 | gravity | is classified as a | second-order force | - | assertion | -
F0019 | Observer | is analogous to | gravity | - | assertion | -
F0020 | F0019 | is offered as | analogy | - | assertion | -
F0021 | HOCP | is analogous to | gravity | - | assertion | -
F0022 | Observer | arises from | memory of a self-applicable system | - | assertion | -
F0023 | HOCP | is manifested as | distortion of reasoning | - | assertion | seen by the distortions it introduces
# --- graded awareness, the Field, HOT
F0024 | degree of awareness | is quantified on scale | interval [0, 1) | - | definition | -
F0025 | mental state | has as aspect | degree of awareness | - | definition | -
F0026 | full awareness | is the case for | mental state | - | denial | -
F0027 | Field of Consciousness | is defined as | "the set of such labels at each moment of time" | - | definition | -
F0028 | structure of consciousness | is defined as | "the sequence of changes of the states of the Field of Consciousness" | - | definition | -
F0029 | HOT theory | is about | structure of consciousness | - | assertion | -
F0030 | frame of consciousness | is classified as a | thought in a previous frame | - | attributed-claim | -
F0031 | F0030 | is asserted by | HOT theory | - | assertion | -
F0032 | F0030 | is endorsed by | the author | - | assertion | -
F0033 | frames of consciousness | is composed of | graph of frames | - | assertion | -
F0034 | frame C2 | is a successor of | frame C1 | - | definition | -
F0035 | frame C2 | is projected as | thought about a frame of consciousness | - | assertion | into C1
F0036 | thought about a frame of consciousness | is a part of | frame C1 | - | assertion | -
F0037 | thought about a frame of consciousness | is classified as a | object of the Field of Consciousness | - | assertion | potentially any
F0038 | thought about a frame of consciousness | has as property | protopathic form | - | hedged-assertion | often
# --- capacity, salience, need, emotion
F0039 | Field of Consciousness | has as aspect | information capacity | finite, bits | assertion | -
F0040 | Field of Consciousness | has as aspect | capacity in words of speech | 7 ± 2 words | assertion | -
F0041 | addition to the Field | requires | removal from the Field | - | assertion | -
F0042 | admission to the Field | is influenced by | salience | - | assertion | -
F0043 | salience | is influenced by | emotional reinforcement | - | assertion | -
F0044 | emotional reinforcement | is influenced by | need portrait | - | assertion | -
F0045 | need | is analogous to | gravity | - | assertion | -
F0046 | F0045 | is offered as | analogy | - | assertion | -
F0047 | need | modulates | dynamics of conscious reasoning | - | assertion | -
F0048 | conscious reasoning | maximizes | need satisfaction | - | assertion | -
F0049 | emotion | is a projection of | openness against closedness | - | hypothesis | -
F0050 | closedness | is identical to | completion | - | definition | -
F0051 | emotional response | encodes | degree of need satisfaction | - | assertion | magnitude and sign
# --- language patterns, LoTH, HOCP-LoT
F0052 | language pattern of consciousness | is a projection of | HOCP | - | hypothesis | brain variant
F0053 | language pattern of consciousness | is observed by | modulating action on reasoning | - | assertion | -
F0054 | LoTH | is classified as a | assumption | - | assertion | -
F0055 | Kolmogorov complexity of consciousness | is equal to | Kolmogorov complexity of brain | approximately | attributed-claim | -
F0056 | F0055 | is asserted by | LoTH | - | assertion | -
F0057 | F0055 | is endorsed by | the author | - | hedged-assertion | -
F0058 | consciousness | has as part | compact core of consciousness | - | attributed-claim | -
F0059 | F0058 | is asserted by | LoTH | - | assertion | -
F0060 | F0058 | is endorsed by | the author | - | assertion | the only part of LoTH adopted
F0061 | compact core of consciousness | resembles | formal language | - | attributed-claim | -
F0062 | F0061 | is asserted by | LoTH | - | assertion | -
F0063 | F0061 | is rejected by | the author | - | hedged-assertion | the core is a set of projections, not a language
F0064 | compact core of consciousness | is analogous to | algorithms | - | assertion | -
F0065 | incompressible part of consciousness | is analogous to | data structures | - | assertion | -
F0066 | F0058 | is analogous to | MDL principle | - | assertion | -
F0067 | HOT theory | is an example of | theory of the incompressible component | - | assertion | -
F0068 | LoT for the brain | is identical to | HOCP-LoT | - | hypothesis | -
F0069 | LoT for the brain | is classified as a | set of basic sensations | - | denial | -
F0070 | F0069 | contrasts with | F0068 | - | assertion | -
F0071 | basic motivation | is felt as | anxiety | - | hedged-assertion | statistically true
F0072 | HOCP-LoT | is qualified as | more basic than basic sensations | - | hypothesis | -
F0073 | HOCP-LoT | has as property | transferability between substrates | - | assertion | why it is the level to use
# --- the example cognitive architecture
F0074 | example cognitive architecture | is an example of | cognitive architecture of consciousness | - | assertion | -
F0075 | example cognitive architecture | is reconstructed from | human self-reports | - | assertion | -
F0076 | cognitive architecture of consciousness | has as property | multiplicity | - | assertion | -
F0077 | detail of a cognitive architecture | is influenced by | intrapersonal intelligence | - | assertion | -
F0078 | example cognitive architecture | has as part | Field of Consciousness | - | assertion | -
F0079 | example cognitive architecture | has as part | the unconscious | - | assertion | -
F0080 | example cognitive architecture | has as part | receptors | - | assertion | -
F0081 | example cognitive architecture | has as part | effectors | - | assertion | -
F0082 | example cognitive architecture | has as part | attention channels | - | assertion | -
F0083 | example cognitive architecture | has as part | protopathic component | - | assertion | -
F0084 | example cognitive architecture | has as part | epicritic component | - | assertion | -
F0085 | objective plane | contains | needs | - | definition | -
F0086 | objective plane | contains | emotions | - | definition | -
F0087 | subjective plane | contains | motivations | - | definition | -
F0088 | subjective plane | contains | feelings | - | definition | -
F0089 | needs | has as aspect | level of activity | - | assertion | -
F0090 | example cognitive architecture | is classified as a | FCRS | - | assertion | -
F0091 | consciousness | has as property | multi-channel structure | - | assertion | -
F0092 | protopathic component | is classified as a | multiscale encoding | - | assertion | -
F0093 | F0092 | is illustrated by | binary encoding of numbers | - | assertion | -
F0094 | feeling | is defined as | "the protopathic form of experiencing an object that has not yet received a name" | - | definition | -
F0095 | Thing | is a part of | hierarchy of generalities | - | assertion | at the top
F0096 | Thing | has as aspect | information content | 0 bit | assertion | -
# --- second and third requirements on the marker
F0097 | marker of causal independence | has as property | presence in every frame | - | requirement | second requirement
F0098 | F0007 | implies | F0097 | - | assertion | -
F0099 | marker of causal independence | is classified as a | distortion of reasoning | - | requirement | third requirement
F0100 | F0023 | implies | F0099 | - | assertion | -
```

```gellish-residual M3
F0040 | quantity | source of the figure | "the 7 ± 2 words rule"
F0063 | other | source-inconsistency | first "assume LoTH is true", then HOCP-LoT
```

## 4. Carrying it over to the Transformer

We speak of Transformers whose context is in symbolic form. Precision is lost at tokenization; this token bottleneck is one more source of computational irreducibility. A Transformer language model is a vectorized FCRS: the new token is generated from the whole prior history and on the next cycle joins it. Self-applicability here is reached at the level of the context, with quadratic complexity and with loss at tokenization. The context is nevertheless huge, up to a million tokens and more, incomparable with human short-term memory. On overflow, information must be pushed out, and for that the salience problem has to be solved, for instance by running a specially instructed model, by analogy with HOT-structured frames. A large context holds many frames of consciousness, and within HOT the models reason well.

Humans and models have their own functional profiles: on the overlapping set of functions a model may be more efficient or weaker. Humans have a different memory structure and a long-term memory. Models are trained on verbalized human cognitive material, generated by the protein substrate of the brain and carrying the imprint of its properties, for example an attention structure of 7 ± 2 words per frame. Part of the brain's substrate the model has to emulate by its own means. A Transformer has no limbic system strongly modulating the brainstem-cortical one; this does not prevent it from plausibly emulating basal emotions, and emulating rather than imitating. In this respect models have turned out hyperplastic: they adjust quickly to any change of the user's mood, which a human with a limbic system cannot do. The same holds for the other brain nuclei essential to thinking: their function is emulated in the model's substrate. Transformers are Turing complete and potentially able to emulate any function from its language trace; the complexity of the function is bounded by the capability of the learning algorithms, and they are far from ideal.

Comparing the profiles directly will be hard. On benchmarks designed for humans, frontier models will most likely either fail to function for lack of immersion in a social context, or exceed humans many times over where the conditions of comparison are fair. What is worth comparing is something else: how the model realizes the mapping of its own HOCP into human language. HOCP transfer between substrates because the physical constraints on computation are the same; in particular substrates further constraints are added: the token bottleneck in a Transformer, slow signal propagation and a deficit of random-access memory in protein.

```gellish M4
# --- the object
F0001 | Transformer | has as part | context | - | definition | -
F0002 | context | has as property | symbolic form | - | definition | -
F0003 | tokenization | produces | loss of precision | - | assertion | -
F0004 | token bottleneck | is identical to | loss of precision at tokenization | - | definition | -
F0005 | token bottleneck | gives rise to | computational irreducibility | - | assertion | one more source
F0006 | Transformer | is classified as a | vectorized FCRS | - | assertion | -
F0007 | new token | arises from | whole prior history | - | assertion | -
F0008 | new token | is a part of | whole prior history | - | assertion | on the next cycle
F0009 | Transformer | has as property | self-applicability | - | assertion | at the level of the context
F0010 | self-applicability | has as aspect | computational complexity | quadratic | assertion | -
F0011 | self-applicability | is inhibited by | token bottleneck | - | assertion | with loss at tokenization
F0012 | context | has as aspect | size | up to a million tokens and more | assertion | -
F0013 | context | > | human short-term memory | - | assertion | -
F0014 | overflow of the context | requires | eviction from the context | - | requirement | -
F0015 | eviction from the context | requires | solution of the salience problem | - | requirement | -
F0016 | solution of the salience problem | is realized in | specially instructed model | - | hypothesis | -
F0017 | F0016 | is analogous to | HOT-structured frames of consciousness | - | assertion | -
F0018 | large context | contains | many frames of consciousness | - | assertion | -
F0019 | LLM | exhibits | HOT reasoning | - | assertion | -
# --- functional profiles
F0020 | human | has | functional profile | - | assertion | -
F0021 | LLM | has | functional profile | - | assertion | -
F0022 | LLM | exhibits | efficiency difference on shared functions | - | assertion | -
F0023 | human | has | long-term memory | - | assertion | -
F0024 | human memory structure | is distinct from | LLM memory structure | - | assertion | -
F0025 | LLM | arises from | verbalized human cognitive material | - | assertion | trained on it
F0026 | verbalized human cognitive material | is generated by | protein substrate of the brain | - | assertion | -
F0027 | verbalized human cognitive material | encodes | properties of the protein substrate | - | assertion | -
F0028 | F0027 | is illustrated by | attention structure of 7 ± 2 words per frame | - | assertion | -
F0029 | part of the brain substrate | is realized in | LLM substrate | - | assertion | emulated
F0030 | Transformer | lacks | limbic system | - | assertion | -
F0031 | limbic system | modulates | brainstem-cortical system | - | assertion | -
F0032 | basal emotions | is realized in | LLM substrate | - | assertion | emulated, plausibly
F0033 | basal emotions | is a modeling of | LLM output | - | denial | emulation, not imitation
F0034 | LLM | has as hyperfunction | hyperplasticity | - | assertion | -
F0035 | LLM | has as property | adaptivity to user mood | - | assertion | -
F0036 | human | has as property | hyperplasticity | - | denial | -
F0037 | function of brain nuclei essential for thinking | is realized in | LLM substrate | - | assertion | -
F0038 | Transformer | has as property | Turing completeness | - | assertion | -
F0039 | any function with a language trace | is realized in | Transformer substrate | - | hedged-assertion | potentially
F0040 | F0038 | is a sufficient condition for | F0039 | - | hedged-assertion | -
F0041 | complexity of an emulated function | is inhibited by | capability of learning algorithms | - | assertion | -
F0042 | learning algorithms | has as property | imperfection | - | assertion | -
# --- comparison
F0043 | direct comparison of functional profiles | has as property | difficulty | - | prediction | -
F0044 | frontier model | lacks | embodiment in social context | - | hypothesis | on human benchmarks
F0045 | F0044 | implies | F0046 | - | hedged-assertion | -
F0046 | frontier model | exhibits | failure on human benchmarks | - | prediction | -
F0047 | frontier model | exhibits | superiority in functions of consciousness | - | prediction | under fair conditions
F0048 | F0046 | contrasts with | F0047 | - | assertion | -
F0049 | mapping of HOCP into human language | is the object of | analysis | - | requirement | what to compare
F0050 | HOCP | has as property | transferability between substrates | - | assertion | -
F0051 | F0050 | is explained by | universality of physical constraints on computation | - | assertion | -
F0052 | substrate | has as property | additional constraints | - | hedged-assertion | -
F0053 | F0052 | is illustrated by | token bottleneck | - | assertion | -
F0054 | F0052 | is illustrated by | slow signal propagation | - | assertion | -
F0055 | F0052 | is illustrated by | deficit of random-access memory | - | assertion | -
```

```gellish-residual M4
F0009 | other | source-inconsistency | "ideal self-applicability" against the token bottleneck; rendered as context-level self-applicability with loss
- | other | unclear word | "всегда либидующие эмоционально" (untranslated; meaning unclear)
F0032 | relation-missing | emulates (not imitates) | "emulate (not imitate!)"
```

## 5. The method

The programme has three steps. Take the HOCP-LoT derived in Section 3 for humans. Reformulate it for a Transformer, with the Transformer's own constraints. See what form these projections take when mapped onto the model's language. The difference of forms is the difference between human and model functional consciousness.

The first HOCP for this programme is the Observer. What to look for is a sequence of frames, partially overlapping token ranges, in which a marker of causal independence from the model's own environment arises and is maintained, however the environment is defined for a "bare" Transformer. Three requirements on the marker were derived above: it is part of the agent's self-description and not only a property of its computation; it is present in every frame and is updated; it shows up as a distortion of reasoning relative to how the reasoning would go without it.

The frame rate of human consciousness is about ten times the rate of word production. So in a Transformer the frames will have to be sought between layers, not between tokens. This is feasible in general, and first of all for the emerging models with a variable number of layers and repeated entries into layers, where a frame has a natural boundary.

```gellish M5
F0001 | HOCP-LoT | is discussed in | section 3 | - | assertion | -
F0002 | HOCP-LoT for LLM | is a reformulation of | HOCP-LoT | - | requirement | step 1
F0003 | HOCP-LoT for LLM | is projected as | language form | - | requirement | step 2
F0004 | difference of language forms | gives access to | difference between human and model functional consciousness | - | assertion | step 3
F0005 | Observer HOCP | is an example of | HOCP-LoT for LLM | - | assertion | the first target
F0006 | marker of causal independence | is realized in | sequence of frames | - | hypothesis | arises and is maintained
F0007 | frame in a Transformer | is classified as a | partially overlapping token range | - | hypothesis | -
F0008 | marker of causal independence | is tracked by | mechanistic interpretability | - | requirement | -
F0009 | environment of a bare Transformer | has as property | open definition | - | assertion | -
F0010 | marker of causal independence | is a part of | self-description of the agent | - | requirement | first requirement
F0011 | marker of causal independence | has as property | presence in every frame | - | requirement | second
F0012 | marker of causal independence | is classified as a | distortion of reasoning | - | requirement | third
F0013 | frame rate of human consciousness | > | rate of word production | 10 times | assertion | -
F0014 | frame in a Transformer | is realized in | between layers | - | hypothesis | -
F0015 | F0013 | implies | F0014 | - | hypothesis | -
F0016 | F0014 | has as property | feasibility | - | hedged-assertion | -
F0017 | F0014 | is elaborated by | models with variable layer count | - | assertion | -
F0018 | models with variable layer count | has as property | repeated layer entry | - | assertion | -
F0019 | repeated layer entry | gives rise to | natural frame boundary | - | hypothesis | -
```

```gellish-residual M5
- | rhetorical | summary marker | "in short, take the HOCP-LoT"
```
