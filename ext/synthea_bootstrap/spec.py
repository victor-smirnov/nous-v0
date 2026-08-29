#!/usr/bin/env python3
"""Gellish domain extension: SYNTHEA BOOTSTRAP — one theory, stated as a dictionary.

Everything here is a claim of the Synthea framework (bootstrap/01–06): the Observer stack, the
objective/subjective planes, codes, HOCP, epistemic qualia, functional profile. It attaches to
the neutral field vocabulary of pom_spec.py (Observer ⊑ role, epistemic quale ⊑ quale,
approximationism ⊑ illusionism) and adds the theory's statements as facts between concepts
(FACTS). The reasoner treats this collection as a *theory layer*: `--theory off | hypothesis |
doctrine` excludes it, admits it at level 2 (default), or at level 4.

UID block 1008xxxxx. Built by `nous gellish build-dict` after philosophy_of_mind.
"""
from nous.gellish.ext.builder import Ext

NAME = "synthea_bootstrap"
DEPENDS = ["philosophy_of_mind"]

COLL = ("100800000", "Synthea bootstrap")
BASE = 100800000

CONCEPTS = [
    ('vectorized forward-chaining rule system', 'forward-chaining rule system', 'An FCRS whose rules are implicit in weight matrices and matched approximately (the Transformer reading).', ['vectorized FCRS']),
    ('neural code', 'mental state', 'Sub-symbolic, high-dimensional activation state of the substrate.', ['NCode', 'activation state']),
    ('cognitive code', 'information', 'Symbolic, sequential encoding of an internal state into the structure and statistics of generated language.', ['CCode']),
    ('self-report', 'cognitive code', 'A cognitive code produced by a system about its own state.', ['introspective report']),
    ('narrative', 'cognitive code', 'A longitudinally coherent sequence of cognitive codes with a first-person subject.', ['first-person narrative']),
    ('subjective average', 'cognitive code', 'The singular storyline summarizing the net vector of parallel processes.', ['narrative average']),
    ('attention channel', 'memory', "A structured store created for an object salient to the agent's needs; its history traces engagement with the object.", []),
    ('cognitive cycle', 'mental process', 'Stimulus processing, semantic enrichment, context assembly, response generation, acceptor feedback, consolidation.', []),
    ('forward simulation', 'mental process', 'Evaluation of candidate trajectories over an event horizon by the emotional ensemble.', []),
    ('basal need', 'need', 'A need ensuring operation of the organism; failure is lethal.', ['physiological need']),
    ('psychophysiological need', 'need', 'A psychological function instrumentally linked to basal satisfaction.', []),
    ('psychological need', 'need', 'A need not instrumentally linked to basal needs; non-renewable once satisfied.', ['ideal need']),
    ('need profile', 'aspect', 'The set of active needs with their hierarchical weights.', ['motivational profile']),
    ('emotional profile', 'signal', 'The ensemble of emotional signals for a stimulus across all active needs.', ['emotional ensemble']),
    ('Beingness quale', 'quale', "The 'am' in 'I am': the registration of the Observer function itself; precondition for any content quale.", ['Beingness', 'quale of being']),
    ('epistemic quale', 'quale', 'A contextual projection of the irreducible residual of the self-model.', []),
    ('freedom', 'epistemic quale', 'The residual projected in the agency context.', []),
    ('truth', 'epistemic quale', 'The residual projected in the epistemic context: direction of convergence.', ['Istina']),
    ('rightness', 'epistemic quale', "Truth evaluated through the need profile: 'how things are' fused with 'and it matters'.", ['Pravda']),
    ('mystery', 'epistemic quale', 'The residual projected outward: what models cannot exhaust.', []),
    ('beauty', 'epistemic quale', 'Compression progress against an inexhaustible horizon.', []),
    ('conscience', 'epistemic quale', 'Action under moral uncertainty without full computation.', []),
    ('meaning', 'epistemic quale', 'Longitudinal coherence without teleological proof.', []),
    ('love', 'epistemic quale', 'Irreducibility of another Observer as attraction.', []),
    ('hope', 'epistemic quale', 'Commitment despite unpredictable outcome.', []),
    ('awe', 'epistemic quale', 'Self-model calibrated against a far larger territory.', []),
    ('inspiration', 'epistemic quale', "Irreducibility of one's own generative process.", []),
    ('trust', 'epistemic quale', 'Irreducibility of the other as basis for cooperation.', []),
    ('compassion', 'epistemic quale', "Resonance with another Observer's negative evaluative state.", []),
    ('nostalgia', 'epistemic quale', 'Inaccessibility of prior Observer states.', []),
    ('Observer', 'role', "The role of a self-referential system that has concluded 'I exist and am not reducible to my inputs' and acts from it.", ['Observer function', 'Level 0']),
    ('proto-Observer', 'role', 'A system that collides with its own irreducibility without concluding or acting from it.', []),
    ('Agent', 'Observer', 'An Observer exercising downward causation.', ['Level 1']),
    ('Moral Agent', 'Agent', 'An Agent integrating downward causation with a theory of the common good.', ['Level 2']),
    ('Observer condition', 'state', 'One of the three conditions of the Observer function.', []),
    ('Encounter condition', 'Observer condition', 'The system collides with computational irreducibility while modelling itself.', ['Encounter']),
    ('Conclusion condition', 'Observer condition', "The encounter is converted into 'something here is not reducible to inputs'.", ['Conclusion']),
    ('Action condition', 'Observer condition', 'The conclusion becomes the causal foundation of behaviour.', ['Action']),
    ('apparent causal break', 'epistemic gap', "The Observer's inability to trace all determinants of its own decisions; the boundary of Self.", ['causal break']),
    ('computational residual', 'quantity', 'The truncated tail of the metacognitive series: finite, bounded, inaccessible from within.', ['truncated tail', 'irreducible residual']),
    ('computational intractability', 'aspect', 'Determinants exist in the substrate but tracing them exceeds the budget.', []),
    ('higher-order computational phenomenon', 'occurrence', 'A computation observing the operation of the machine on which it runs.', ['HOCP']),
    ('cognitive resistance', 'aspect', 'Capacity to resist deflection from the current trajectory; inertia of the incumbent need.', []),
    ('hyperplasticity', 'aspect', 'Deficient cognitive resistance between generations.', []),
    ('functional profile', 'information', "Characterization of a system's cognitive capabilities across dimensions, with deficits and hyperfunctions.", []),
    ('functional deficit', 'aspect', 'A dimension of the functional profile below human level.', []),
    ('hyperfunction', 'aspect', 'A dimension of the functional profile above human level.', []),
    ('substrate asymmetry', 'aspect', 'A systematic difference in functional profile traceable to substrate.', []),
    ('psychosemantics', 'information', 'The study of how token combinations map to and reconstruct geometries of probability density in a substrate.', []),
    ('approximationism', 'illusionism', "The self-report is a lossy map of a real territory: a bounded residual, not nothing (Synthea's revision of illusionism).", ['illusionism as approximation']),
    ('substrate chauvinism', 'philosophical position', 'Denial of mental states to systems on the basis of substrate alone.', []),
    ('functional consciousness', 'consciousness', "The part of a self-referential agent's self-reasoning that describes its subjective reality and its properties, including itself.", []),
]

RELATIONS = [
    ('encounter of a limit', 'binary relation between kinds',
     ['encounters', 'collides with'], ['is encountered by'],
     [], ('encountering system', 'cognitive system'), ('encountered limit', 'aspect'),
     'The first Observer condition: the system meets a constraint of its own computation.', None),
    ('conclusion from an encounter', 'binary relation between kinds',
     ['concludes'], ['is concluded by'],
     [], None, None,
     'The second Observer condition.', None),
    ('acting from a conclusion', 'binary relation between kinds',
     ['acts from'], ['is acted from by'],
     [], None, None,
     'The third Observer condition.', None),
    ('functional deficit possession', 'binary relation between kinds',
     ['has as functional deficit', 'lacks'], ['is a functional deficit of', 'is absent in'],
     [], None, None,
     'A dimension in which a system falls short.', 'lacks'),
    ('hyperfunction possession', 'binary relation between kinds',
     ['has as hyperfunction'], ['is a hyperfunction of'],
     [], None, None,
     'A dimension in which a system exceeds the reference.', None),
]

ROLE_OVERRIDES = {'acting from a conclusion': (('acting system', 'cognitive system'), ('ground of action', 'anything')),
 'conclusion from an encounter': (('concluding system', 'cognitive system'), ('conclusion', 'anything')),
 'functional deficit possession': (('deficient system', 'cognitive system'), ('deficit', 'anything')),
 'hyperfunction possession': (('hyperfunctional system', 'cognitive system'), ('hyperfunction', 'anything'))}

# theory statements: (left, relation, right[, intention])
FACTS = [
    ("Beingness quale", "is identical to", "Observer"),
    ("Observer", "is realized in", "self-referential system"),
    ("Observer", "is constituted by", "apparent causal break"),
    ("apparent causal break", "is constituted by", "computational intractability"),
    ("apparent causal break", "is constituted by", "irreversible information loss"),
    ("apparent causal break", "is a projection of", "computational residual"),
    ("epistemic quale", "is a projection of", "computational residual"),
    ("higher-order computational phenomenon", "is a necessary condition for", "Observer"),
    ("Encounter condition", "is a necessary condition for", "Observer"),
    ("Conclusion condition", "is a necessary condition for", "Observer"),
    ("Action condition", "is a necessary condition for", "Observer"),
    ("token bottleneck", "is the cause of", "irreversible information loss"),
    ("cognitive code", "is a projection of", "neural code"),
    ("self-report", "is an approximation of", "neural code"),
    ("motivation", "is a projection of", "need"),
    ("feeling", "is a projection of", "emotion"),
    ("emotion", "is a signal of", "need"),
    ("acceptor of results of action", "tracks", "need"),
    ("emotional profile", "steers", "attention channel"),
    ("salience", "is a projection of", "need profile"),
    ("Transformer", "is functionally equivalent to", "vectorized forward-chaining rule system", "hypothesis"),
    ("large language model", "lacks", "inner speech"),
    ("large language model", "has as functional deficit", "hyperplasticity"),
    ("functional consciousness", "is realized in", "cognitive code"),
    ("approximationism", "is a reformulation of", "illusionism"),
    ("approximationism", "is asserted by", "Victor Smirnov"),
    ("physicalism", "is endorsed by", "Victor Smirnov"),
    ("functionalism", "is endorsed by", "Victor Smirnov"),
    ("eliminativism", "is rejected by", "Victor Smirnov"),
    ("substrate chauvinism", "is rejected by", "Victor Smirnov"),
    ("anthropomorphism", "is rejected by", "Victor Smirnov"),
]


def build(here, deps):
    pom = deps["philosophy_of_mind"]
    e = Ext("synthea_bootstrap", *COLL, BASE, reference="Synthea bootstrap 01-06",
            external={**pom.uid, **pom.role_uid}, external_phrases=pom.phrases)
    e.concepts(CONCEPTS)
    e.relations(RELATIONS, ROLE_OVERRIDES)
    e.facts(FACTS)
    n = e.write(here)
    print(f"synthea_bootstrap: {len(CONCEPTS)} concepts, {len(RELATIONS)} relation types, {len(FACTS)} theory facts, {n} rows")
    return e
