# Relation phrases for the encoder

Use these phrases in the relation column, exactly as written. A phrase from the *inverse* column
reads right-to-left (`A has as part B` ≡ `B is a part of A`); both are accepted. Roles say what
kind of thing may stand left → right. Anything not here goes to the `gellish-residual` block.

96 relation types.

## taxonomy & identity

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| classification of an individual thing (1225) | is a · is an · is classified as · is classified as a | classifies · is a classifier of | individual thing → concept | antisymmetric, intransitive | Gellish |
| equality of an aspect to a qualitative aspect (5020) | has as value · is equally high as · is qualified as · is qualified by | is a qualitative value that qualifies · is qualifier of |  | antisymmetric, intransitive | Gellish |
| equality relation (5828) | = · is equal to | is not different from |  |  | Gellish |
| inequality relation (5831) | is not equal to · is unequal to · ≠ | is different from |  |  | Gellish |
| specialisation relation between kinds (1146) | is a kind of · is a specialisation of · is a specialization of · is a subclass of · is a subtype of · is by definition a subtype of · is defined as a kind of | has as subtype · is a generalisation of · is a generalization of · is a supertype of |  | antisymmetric, transitive | Gellish |
| distinctness (100701041) | differs from · is distinct from · is not identical to · is not the same as | is distinct from |  | symmetric | field |
| identity (100701040) | is identical to · is identified with · is synonymous with · is the same as | is identical to |  | symmetric, transitive | field |
| negative classification (100701042) | is not a · is not an · is not an instance of · is not classified as · is not classified as a · is not classified as an | does not classify |  |  | field |

## part-whole & constitution

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| composition relation between an individual thing and a composed individual thing (1260) | is a component of · is a part of · is a subcomponent of · is part of · is the capital of | contains · has as capital · has as component · has as part · includes · is a totality of · is a whole of | · → individual thing |  | Gellish |
| constitution (100701009) | consists of · is composed of · is constituted by · is grounded in · is made up of | constitutes · grounds · makes up | anything → anything | transitive | field |

## projection & realization

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| modeling of an object (5776) | is a modeling of | is modelled as |  |  | Gellish |
| realization of a conceptual fact by an individual fact (5452) | is a realization of | is realized by |  |  | Gellish |
| approximation of a process (100701002) | approximates · is an approximation of | is approximated by | anything → anything |  | field |
| conceptualization (100701003) | is conceptualised as · is conceptualized as | is a conceptualization of | anything → concept |  | field |
| encoding (100701006) | encodes · is an encoding of | is encoded as · is encoded in | anything → anything |  | field |
| experiential projection (100701004) | is experienced as · is felt as | is the experience of | anything → anything |  | field |
| functional analogy (100701012) | is a functional analog of · is a functional analogue of · is functionally analogous to | is a functional analogue of |  | symmetric | field |
| functional equivalence (100701011) | is functionally equivalent to | is functionally equivalent to |  | symmetric, transitive | field |
| logical equivalence (100701039) | is a biconditional of · is equivalent to · is logically equivalent to | is logically equivalent to |  | symmetric, transitive | field |
| manifestation (100701005) | is manifested as · manifests as | is a manifestation of |  |  | field |
| metaphorical expression (100701014) | is a metaphor for · is figuratively expressed as | is expressed by the metaphor | metaphor → anything |  | field |
| projection of a state into a code (100701001) | is a low-dimensional projection of · is a projection of | is projected as · projects to | information → mental state |  | field |
| realization of a function in a substrate (100701007) | is implemented in · is realised in · is realized in · runs on | implements · is a substrate of · realises · realizes | anything → substrate |  | field |
| reduction (100701010) | is reduced to · is reducible to · reduces to | is a reduction base of |  | transitive | field |
| structural analogy (100701013) | is an analogy for · is analogous to · is structurally analogous to · parallels · resembles | is analogous to |  | symmetric | field |
| supervenience (100701008) | supervenes on | is a supervenience base of · subvenes | anything → anything | antisymmetric, transitive | field |

## causation, conditions & logic

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| implication relation between relations (6233) | entails · has as implication · implies · logically implies | follows from · is an implication of · is entailed by · is implied by |  |  | Gellish |
| counterexample (100701048) | is a counterexample to | has as counterexample |  |  | field |
| explanation (100701033) | accounts for · explains | is accounted for by · is explained by | information → anything |  | field |
| generalization (100701050) | generalises · generalizes · is a generalization of | is a special case of |  | transitive | field |
| necessary condition (100701037) | is a necessary condition for · is a necessary condition of · is a precondition for · is a prerequisite for · is necessary for · is presupposed by · is required for | depends on · has as necessary condition · presupposes · requires |  | transitive | field |
| prediction relation (100701034) | predicts | is predicted by | information → anything |  | field |
| sufficient condition (100701038) | guarantees · is a sufficient condition for · is a sufficient condition of · is sufficient for | has as sufficient condition |  | transitive | field |

## needs, signals & control

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| influencing relation (6208) | is influenced by | is influencing |  |  | Gellish |
| possession of a property (4798) | has as property · has property | is a property of |  |  | Gellish |
| possession of an aspect by an individual thing (1727) | has · has as aspect · has aspect · is bearer of · possesses | is an aspect of | individual thing → aspect |  | Gellish |
| acting from a conclusion (100801003) | acts from | is acted from by | cognitive system → anything |  | Synthea |
| amplification (100701022) | amplifies | is amplified by |  |  | field |
| conclusion from an encounter (100801002) | concludes | is concluded by | cognitive system → anything |  | Synthea |
| directedness (100701027) | is about · is directed at · is directed toward · is directed towards | is the object of | mental state → anything |  | field |
| encounter of a limit (100801001) | collides with · encounters | is encountered by | cognitive system → aspect |  | Synthea |
| evaluation (100701017) | evaluates | is evaluated by |  |  | field |
| exhibition of a property (100701032) | displays · exhibits · shows | is exhibited by |  |  | field |
| functional deficit possession (100801004) | has as functional deficit · lacks | is a functional deficit of · is absent in | cognitive system → anything |  | Synthea |
| functional role possession (100701031) | has as functional role · has functional role · plays the functional role of | is a functional role of | anything → role |  | field |
| gating (100701023) | gates | is gated by |  |  | field |
| generation (100701029) | generates · gives rise to · produces | arises from · is generated by |  |  | field |
| hyperfunction possession (100801005) | has as hyperfunction | is a hyperfunction of | cognitive system → anything |  | Synthea |
| influence (100701018) | acts on · influences | is influenced by |  |  | field |
| inhibition (100701021) | inhibits · suppresses | is inhibited by · is suppressed by |  |  | field |
| minimization (100701025) | minimises · minimizes | is minimized by |  |  | field |
| modulation (100701020) | modulates | is modulated by |  |  | field |
| monitoring (100701026) | monitors · observes | is monitored by · is observed by | cognitive system → anything |  | field |
| optimization (100701024) | maximizes · optimises · optimizes | is maximized by |  |  | field |
| persistence across (100701028) | persists across | is spanned by |  |  | field |
| reconstruction (100701030) | reconstructs | is reconstructed by · is reconstructed from | cognitive system → anything |  | field |
| signalling of need satisfaction (100701015) | is a signal of · signals | is signaled by · is signalled by | signal → anything |  | field |
| steering of attention (100701019) | directs · steers | is steered by | signal → anything |  | field |
| tracking (100701016) | is tracked against · tracks | is tracked by | anything → anything |  | field |

## dialectics & provenance

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| authorship of qualitative information (5126) | is author of | has as author · is authored by · is written by | person → · |  | Gellish |
| description relation (4682) | characterizes · describes · is a description of | has as description · is described as | information → anything |  | Gellish |
| assertion by a party (100701052) | is argued by · is asserted by · is claimed by · is held by · is posed by · is proposed by · is stated by | argues · asserts · claims · holds · poses · proposes | anything → anything |  | field |
| commitment level (100701057) | has as commitment · has commitment | is the commitment of |  |  | field |
| concession (100701047) | is conceded by | concedes |  |  | field |
| contrast (100701043) | contrasts with · is contrasted with · is in tension with · is opposed to · stands in contrast to | contrasts with |  | symmetric | field |
| elaboration (100701036) | is elaborated by · is exemplified by · is illustrated by | elaborates · exemplifies · illustrates |  |  | field |
| endorsement (100701053) | is accepted by · is adopted by · is affirmed by · is endorsed by | accepts · adopts · endorses | anything → anything |  | field |
| evidential support (100701035) | is evidence for · supports | is evidenced by · is supported by | anything → anything |  | field |
| exemplification (100701058) | is an example of · is an instance of the kind | has as example · has example | anything → anything |  | field |
| inversion of a question (100701049) | inverts · is an inversion of | is inverted by |  |  | field |
| objection (100701044) | challenges · is a critique of · is an objection to · is raised against | has as objection · is challenged by | anything → anything |  | field |
| offering as (100701055) | is intended as · is offered as · is presented as | is the mode of |  |  | field |
| qualification (100701056) | is characterised as · is characterized as · is qualified as | qualifies |  |  | field |
| rebuttal (100701045) | is a rebuttal of · is raised to rebut · rebuts · refutes | is rebutted by · is refuted by |  |  | field |
| reformulation (100701051) | is a reformulation of · restates | is reformulated as |  |  | field |
| rejection (100701054) | is denied by · is disputed by · is rejected by | denies · disputes · rejects | anything → anything |  | field |
| reply (100701046) | answers · is a reply to · responds to | is answered by |  |  | field |

## bibliographic

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| being publisher of a physical object (5751) | is publisher of · publishes | is published by |  |  | Gellish |
| citation (100701061) | cites · refers to | is cited by · is referred to by | information → information |  | field |
| dating (100701059) | is dated · is dated to · was published in the year | is the date of | information → anything |  | field |
| publication in a venue (100701060) | appears in · is published in · is reported in | contains the publication · publishes | information → anything |  | field |

## quantities, time & other

| relation type | phrases | inverse phrases | roles (left → right) | algebra | src |
|---|---|---|---|---|---|
| being in a state during a period (4872) | happens during · is the case during · lasts during · occurs during | is occurrence period of | occurrence → period in time |  | Gellish |
| being maker of a physical object (5160) | is the maker of · is the producer of | is made by · is produced by |  |  | Gellish |
| being the cause of a begin or an end of a state by an occurrence (1922) | brings about · causes · has as consequence · has as effect · is a cause of · is the cause of | has as cause · is a result of · is an effect of · is caused by · is consequence of · results from | occurrence → state |  | Gellish |
| classification of a quantification relation by a scale (1732) | is quantified in · is quantified on scale · will be quantified on scale | is the scale of | quantification of an aspect by a mathematical space → scale | antisymmetric, intransitive | Gellish |
| greater or equal relation (5830) | >= · is greater than or equal to | <= · is less than or equal to |  | transitive | Gellish |
| manufacturer's subtyping relation (5396) | is a brand · is a model · is a model of | has as manufacturer's model · is the nature of brand · is the nature of model |  | antisymmetric, transitive | Gellish |
| quantification of an aspect by a mathematical space (2044) | has as magnitude · is expressed as number · is mathematically expressed as · is quantified as · is quantified by | is quantification of | aspect → mathematical space |  | Gellish |
| relation between a greater and a smaller characteristic (5829) | > · is greater than | < · is smaller than |  | transitive | Gellish |
| relation between a start point and a period in time (1384) | begins at · has as begin point | is starting time of | period in time → point in time |  | Gellish |
| relation between the begin of occurrences (6012) | begins after the start of | starts after the begin of |  |  | Gellish |
| representation of an individual thing by an individual thing (2071) | has as representer · is represented by | is a representative of · is a representer of · is representing | anything → individual thing |  | Gellish |
| succession relation between objects (1385) | has as predecessor · is a successor of · is preceded by · succeeds | has as successor · is a predecessor of · is succeeded by · precedes | anything → anything |  | Gellish |
| temporal sequence relation between occurrences (1388) | occurs after | occurs before | occurrence → occurrence |  | Gellish |
| temporal sequence relation between states (5815) | is a successor in time of · succeeds | is a predecessor in time of · precedes | state → state |  | Gellish |
| value of an aspect being lower than a qualitative aspect (5023) | has a value that is less that · is less than · is lower than | is a qualitative value higher than |  | antisymmetric, intransitive | Gellish |
