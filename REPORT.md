# Gellish reasoner report


## Stats

| metric | n |
|---|---:|
| theory level | 2 |
| dictionary concepts | 69395 |
| dictionary relation types | 8125 |
| dictionary phrases | 3302 |
| theory concepts | 67 |
| entities grounded in theory | 31 |
| facts | 2296 |
| facts via dictionary | 798 |
| facts via extension | 875 |
| facts residual | 623 |
| residual phrases | 460 |
| declared residual rows | 0 |
| second-order facts | 328 |
| entities | 2488 |
| entities grounded | 200 |
| entities ambiguous | 23 |
| entities in >1 table | 85 |
| facts committed (+) | 2080 |
| facts committed (-) | 203 |
| facts unresolved | 0 |
| facts usable | 2018 |
| facts figurative | 72 |
| holds closed | 34206 |
| subtype closed | 1243 |
| instance closed | 1407 |
| part_of closed | 260 |
| identity pairs | 142 |
| entailment stated | 192 |
| entailment closed | 202 |
| entailment truncated | 0 |
| kb size | 4385 |
| kb from dictionary | 2118 |
| contradictions | 6 |
| role tensions | 13 |
| commitment tensions | 7 |
| cap tensions | 1 |
| violations | 146 |

## Contradictions


### entailment (3)

- C02:F0249 ⟨epistemic-quale concepts resist precise definition⟩ (hedge… ⟂ C02:F0252 ⟨Observer cannot compute own truncated tail⟩ (denial) — witness C02:F0252 ⟨Observer cannot compute own truncated tail⟩ (denial) (level 3)
- C07:F0013 ⟨subjective causal break is reduced to physical computation… ⟂ C07:F0014 ⟨agent decides to stop being agent⟩ (denial) — witness C07:F0014 ⟨agent decides to stop being agent⟩ (denial) (level 3)
- C08:F0182 ⟨system lacking functional con… has hole in functional prof… ⟂ C08:F0184 ⟨system lacking functional con… is not equal to fully gener… — witness C08:F0184 ⟨system lacking functional con… is not equal to fully gener… (level 4)

### identity-vs-taxonomy (2)

- causal break ⟂ computational residual — witness C01:F0320 ⟨causal break is classified as a computational residual⟩ (a… (level 4)
- truncated tail ⟂ computational residual — witness C03:F0054 ⟨truncated tail is classified as a computational residual⟩ … (level 4)

### disjoint-relations (1)

- intuition ⟂ observer — witness is endorsed by / is rejected by (level 4)

## Commitment tensions (stated weaker than what committed premises entail)

- C02:F0123 ⟨evolution will find Observer-capable designs at high likel…: stated **conjectured**, entailed **asserted** via C02:F0125 ⟨simple structures dominate search landscape⟩ (as…
- C02:F0128 ⟨Observers are classified as probable outcomes of evolution…: stated **conjectured**, entailed **asserted** via C02:F0120 ⟨Observer-capable architecture is classified as K…
- C02:F0128 ⟨Observers are classified as probable outcomes of evolution…: stated **conjectured**, entailed **asserted** via C02:F0122 ⟨Observer-capable architecture occupies exponenti…
- C02:F0240 ⟨every human culture will develop corresponding concepts⟩ (…: stated **conjectured**, entailed **asserted** via C02:F0239 ⟨every human Observer encounters same causal brea…
- C02:F0243 ⟨framework is predicted by cross-cultural universality⟩ (pr…: stated **conjectured**, entailed **asserted** via C02:F0238 ⟨epistemic-quale instances is instantiated in dif…
- C03:F0111 ⟨epistemic system judging solely by rationalization quality…: stated **conjectured**, entailed **asserted** via C03:F0110 ⟨rationality-as-CCode-quality is classified as a …
- C08:F0246 ⟨evolution, gradient descent, and search process converge o…: stated **conjectured**, entailed **asserted** via C08:F0245 ⟨coding theorem predicts dominance of simple stru…

## Cap tensions (`has commitment` disagrees with intention)

- C06:F0196 ⟨automatism is observed as post-hoc observation⟩ (hedged-as…: intention hedged, declared conjectured

## Spec violations

| kind | n |
|---|---:|
| double-negation | 76 |
| second-order-on-non-fact | 35 |
| figurative-in-taxonomy | 21 |
| bare-copula | 11 |
| fact-ref-in-taxonomy | 3 |

**double-negation**
- C02:F0013 ⟨physics-and-mathematics domain lacks privileged vantage po… — lacks
- C02:F0014 ⟨physics-and-mathematics domain lacks intrinsic insideness⟩… — lacks
- C02:F0017 ⟨Beingness-quale is not classified as sensory quality⟩ (den… — not_classified_as
- C02:F0027 ⟨Beingness-quale is not classified as substance⟩ (denial) — not_classified_as
- C02:F0028 ⟨Beingness-quale is not classified as field⟩ (denial) — not_classified_as
- C02:F0029 ⟨Beingness-quale is not classified as emergent physical pro… — not_classified_as

**second-order-on-non-fact**
- C01:F0036 ⟨Functional Profile is offered as alternative to consciousn… — offered_as
- C01:F0077 ⟨practical impossibility is endorsed by the author⟩ (assert… — endorsed_by
- C01:F0078 ⟨principled impossibility is rejected by the author⟩ (denia… — rejected_by
- C01:F0086 ⟨question about LLM experience is offered as analogy to Nag… — offered_as
- C01:F0094 ⟨third path is raised to rebut C01:F0087 ⟨eliminativist pos… — raised_to_rebut
- C01:F0095 ⟨third path is raised to rebut C01:F0088 ⟨anthropomorphic p… — raised_to_rebut

**figurative-in-taxonomy**
- C03:F0061 ⟨epistemic qualia is classified as a necessary byproduct of… — g:1225
- C03:F0128 ⟨logit vector is classified as a many subjects, mathematica… — g:1225
- C03:F0139 ⟨I self-report is identified with summarized log file⟩ (ass… — g:100701040
- C04:F0066 ⟨conditional probability densi… is classified as a emotiona… — g:1225
- C04:F0087 ⟨Cognitive Code (CCode) is classified as a bridge across sy… — g:1225
- C05:F0075 ⟨emotional ensemble is classified as a weighted-sum-neuron … — g:1225

**bare-copula**
- C05:F0006 ⟨need hierarchy is not static ordering⟩ (denial) — is not
- C05:F0060 ⟨system attention is not neutral⟩ (denial) — is not
- C05:F0086 ⟨probability-distribution-over-actions claim is not theoret… — is not
- C05:F0106 ⟨emotional response decay is not uniform across need catego… — is not
- C05:F0143 ⟨hedonic adaptation is not architecture bug⟩ (denial) — is not
- C05:F0176 ⟨emotion evaluative function is not luxury overlay on ratio… — is not

**fact-ref-in-taxonomy**
- C03:F0216 ⟨C03:F0211 ⟨audience with grea… is classified as a structur… — g:1225
- C04:F0062 ⟨causal break constitutes C04:F0061 ⟨system with HOCP k…⟩ (… — g:100701009
- C08:F0068 ⟨C08:F0066 ⟨reported frustrati… is a specialization of gene… — g:1146

## Residual relation phrases (extension backlog)

| phrase | n |
|---|---:|
| is not | 11 |
| must contain | 7 |
| provides | 5 |
| performs | 5 |
| maintains | 5 |
| exceeds | 5 |
| collapses | 4 |
| raises question of | 4 |
| is compared to | 3 |
| shifts with | 3 |
| diverges from | 3 |
| cannot trace | 3 |
| primes | 3 |
| constrains | 3 |
| acts as | 3 |
| computes | 3 |
| is annihilated at | 3 |
| must specify | 3 |
| maps to | 3 |
| share | 3 |
| undergoes | 3 |
| shifts upon | 3 |
| can activate | 3 |
| shapes | 3 |
| conflicts with | 3 |
| selects | 3 |
| satisfies | 3 |
| makes | 3 |
| projects as | 3 |
| sustains | 3 |
| switches between | 3 |
| is a test of | 3 |
| is edited by | 3 |
| traces | 2 |
| is applied to | 2 |
| relies on | 2 |
| serves | 2 |
| asks what | 2 |
| is independent of | 2 |
| resists reduction to | 2 |
| … 420 more | |

## Declared residual (what the encoder refused to encode)

none

## Truncated entailment chains (depth budget exhausted)

none

## Role tensions (grounded players vs. dictionary role kinds)

13 total; first 20:

- C01:F0060 ⟨physical process is a result of subjective experience⟩ (as…: role 1 player `physical process` grounded as *physical process*, expected *occurrence*
- C02:F0045 ⟨Downward Causation is described as subsequent-processing i…: role 1 player `Downward Causation` grounded as *downward causation*, expected *information*
- C02:F0171 ⟨system collides with own modeling limits toward wo…⟩ (asse…: role 1 player `system` grounded as *system*, expected *cognitive system*
- C02:F0183 ⟨system acts from Mystery-quale⟩ (assertion): role 1 player `system` grounded as *system*, expected *cognitive system*
- C03:F0195 ⟨reader reconstructs corresponding mental state⟩ (assertion): role 1 player `reader` grounded as *reader*, expected *cognitive system*
- C04:F0042 ⟨computation encounters resistance (latency spike, co…⟩ (as…: role 1 player `computation` grounded as *computing*, expected *cognitive system*
- C05:F0080 ⟨need conflict is a cause of negative-emotional-feedback v……: role 1 player `need conflict` grounded as *motivational conflict*, expected *occurrence*
- C06:F0010 ⟨consciousness describes subjective reality⟩ (definition): role 1 player `consciousness` grounded as *consciousness*, expected *information*
- C06:F0011 ⟨consciousness describes property of subjective reality⟩ (d…: role 1 player `consciousness` grounded as *consciousness*, expected *information*
- C06:F0205 ⟨environment fulfills expectation⟩ (denial): role 1 player `environment` grounded as *environment*, expected *relation between individual things*
- C06:F0218 ⟨reflection occurs during conflict-free process⟩ (denial): role 1 player `reflection` grounded as *metacognition*, expected *occurrence*
- C07:F0053 ⟨user steers model trajectory⟩ (assertion): role 1 player `user` grounded as *user*, expected *signal*
- C07:F0147 ⟨hyperplasticity is a cause of model diligence⟩ (hedged-ass…: role 1 player `hyperplasticity` grounded as *hyperplasticity*, expected *occurrence*

## Grounded entities (sample)

200 groundings; first 25:

- Acceptor → 100700022
- Acceptor of Results of Action → 100700022
- Action condition → 100800038
- Anokhin TFS 1974 → 100703011
- Anokhin, P. K. → 100703011
- consciousness → 100700032
- Baars, B. J. → 100703018
- behavior → 190387
- Beingness quale → 100800015
- Beingness → 100800015
- causal break → 100800039
- apparent causal break → 100800039
- cognitive code → 100800003
- Cognitive Code → 100800003
- Chalmers 1995 → 100703003
- Chalmers, D. J. → 100703003
- mind → 100700001
- cognitive process → 100700014
- mental state → 100700013
- compression → 190684
- computation → 190688
- Conclusion condition → 100800037
- context window → 100700015
- working memory → 100700015
- current Transformer → 250118

## Derived taxonomy (sample)

2228 derived classification/specialization facts; first 30:

- certain —is a kind of→ anything (level 2)
- certain —is a kind of→ concept (level 2)
- certain —is a kind of→ quality (level 2)
- certain —is a kind of→ communicative intent (level 2)
- certain —is a kind of→ individual thing (level 2)
- certain —is a kind of→ characteristic (level 2)
- certain —is a kind of→ aspect (level 2)
- certain —is a kind of→ certainty (level 2)
- certain —is a kind of→ intention (level 2)
- certain —is a kind of→ social attitude (level 2)
- certain —is a kind of→ attitude (level 2)
- probable —is a kind of→ anything (level 2)
- probable —is a kind of→ property (level 2)
- probable —is a kind of→ concept (level 2)
- probable —is a kind of→ ratio (level 2)
- probable —is a kind of→ probability (level 2)
- probable —is a kind of→ relative property (level 2)
- probable —is a kind of→ individual thing (level 2)
- probable —is a kind of→ characteristic (level 2)
- probable —is a kind of→ aspect (level 2)
- 1982 —is classified as a→ anything (level 2)
- 1982 —is classified as a→ time (level 2)
- 1982 —is classified as a→ period in time (level 2)
- 1982 —is classified as a→ concept (level 2)
- 1982 —is classified as a→ year in time (level 2)
- 1982 —is classified as a→ individual thing (level 2)
- 1982 —is classified as a→ characteristic (level 2)
- 1982 —is classified as a→ aspect (level 2)
- behavior —is a kind of→ anything (level 2)
- behavior —is a kind of→ occurrence (level 2)

## Longest entailment chains

- depth 2, level 4: Action condition ⇒ Encounter condition
- depth 2, level 4: closing self-model gap ⇒ gap nonexistence
- depth 2, level 4: common-good orientation ⇒ Beingness-level
- depth 2, level 4: freedom-and-rights reasoning ⇒ proto-Observer
- depth 2, level 4: freedom-and-rights reasoning ⇒ Encounter condition
- depth 2, level 4: freedom-and-rights reasoning ⇒ Conclusion condition
- depth 2, level 4: freedom-and-rights reasoning ⇒ Action condition
- depth 2, level 4: C02:F0120 ⟨Observer-capable architecture is classified as K… ⇒ C02:F0128 ⟨Observers are classified as probable outcomes of…
- depth 2, level 4: C05:F0064 ⟨need is not tracked by active Acceptor⟩ (asserti… ⇒ C05:F0066 ⟨system is emotionally indifferent to untracked-n…
- depth 2, level 2: C05:F0351 ⟨Transformer lacks FCRS inductive bias⟩ (hypothes… ⇒ C05:F0353 ⟨cognitive-architecture AI app… is failed approac…

## Cross-table entities (sample)

- the author: 8 tables
- figurative: 8 tables
- analogy: 6 tables
- literal: 6 tables
- causal break: 5 tables
- most consequential: 5 tables
- LLM: 4 tables
- truncated tail: 3 tables
- Transformer: 3 tables
- mental state: 3 tables
- intuition: 3 tables
- consciousness: 3 tables
- intrapersonal intelligence: 3 tables
- Observer: 3 tables
- model: 3 tables
- system: 3 tables
- Cognitive Code: 3 tables
- Downward Causation: 3 tables
- self-reference: 3 tables
- certain: 2 tables
