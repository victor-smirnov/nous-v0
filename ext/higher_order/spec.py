#!/usr/bin/env python3
"""Gellish domain extension: HIGHER-ORDER THOUGHT — the layer that is visible in language.

HOT is not a rival account of consciousness here and must not be encoded on the axis that holds illusionism,
functionalism and eliminativism: it answers a different question. It is a theory of the *succession of conscious
states* — of what is conscious at a given moment — and its standing merit is that the graph it describes is
partially reduced to language, carried by the linguistic form of thoughts. That is what makes it usable by a tool
that reads text.

So this extension supplies notation, not mechanism. The selecting mechanism is already in the bootstrap
(`salience is a projection of need profile`, `emotional profile steers attention channel`); the relations below
record the selection where the text expresses it. The transitivity principle is admitted as a *principle of
selection* — which state is conscious now — and not as an explanation of consciousness: mechanically, taking a
state as one's own object is self-applicability, one tape and a few rules, and the residue it leaves untouched is
bracketed by approximationism rather than accounted for here.

Nodes are ordinary facts; edges are second-order facts over fact refs, which spec v3 rule R3 already allows. The
one relation that earns this extension on its own is `does not notice` — a state the case asserts and the subject
has no higher-order representation of. That is where the low-level layer and this one come apart, and the gap is
countable.

UID block 1011xxxxx. Built by `nous gellish build-dict` after philosophy_of_mind.
"""
from nous.gellish.ext.builder import Ext

NAME = "higher_order"
DEPENDS = ["philosophy_of_mind"]
COLL = ("101100000", "Higher-order thought")
BASE = 101100000

CONCEPTS = [
    ("higher-order representation", "mental state",
     "A state whose object is another state of the same system. Its presence is what a higher-order theory takes to make the target conscious.",
     ["higher-order thought", "HOR"]),
    ("assertoric higher-order thought", "higher-order representation",
     "A non-inferential, assertoric thought to the effect that one is in the target state (Rosenthal's actualist form).",
     ["actualist HOT"]),
    ("dispositional higher-order thought", "higher-order representation",
     "Availability of the target to higher-order thought, rather than an occurrent thought about it (Carruthers).", []),
    ("higher-order perception", "higher-order representation",
     "An inner-sense analogue: the target is monitored rather than thought about (Armstrong, Lycan).",
     ["inner sense", "HOP"]),
    ("self-representation", "higher-order representation",
     "The higher-order content belongs to the same state as its target rather than to a distinct one (Kriegel, Gennaro).",
     ["self-representationalism", "wide intrinsicality view"]),
    ("reality monitoring", "higher-order representation",
     "A judgement that a representation is signal rather than noise; higher-order in form but discriminative rather than descriptive (Lau).",
     ["perceptual reality monitoring", "PRR"]),
    ("empty higher-order representation", "higher-order representation",
     "A higher-order state with no target, or with content the target does not have. The case on which higher-order theories divide.",
     ["targetless HOT", "misrepresenting HOT"]),
    ("state consciousness", "consciousness",
     "A property of a particular mental state: this state, now, is one the subject is conscious of.", []),
    ("creature consciousness", "consciousness",
     "A property of the whole system rather than of any one of its states.", []),
    ("transitivity principle", "theory of mind",
     "A conscious state is a state one is conscious of. Taken here as a principle selecting which state is conscious now, not as an account of why there is consciousness at all.",
     []),
    ("unconscious determinant", "aspect",
     "A state that is operative in the system and has no higher-order representation in it: efficacious, and not visible in what the subject can say.",
     ["unnoticed determinant"]),
    ("state succession", "mental process",
     "The ordered series of what is conscious across a reading or an episode; the object a higher-order theory actually explains.",
     ["succession of conscious states"]),
]

RELATIONS = [
    ("awareness of a state", "binary relation between individual things",
     ["is aware that", "is conscious that"], ["is a state noticed by"],
     [], ("aware subject", "anything"), ("noticed state", "anything"),
     "An occurrent higher-order representation: the subject takes the target to be the case. The right side is normally a fact reference.",
     "hot_aware"),
    ("coming to awareness", "binary relation between individual things",
     ["becomes aware that", "comes to see that"], ["dawns on"],
     [], ("awakening subject", "anything"), ("newly noticed state", "anything"),
     "A transition rather than a standing state: the edge of the graph, where what is conscious changes.",
     "hot_becomes"),
    ("taking to be so", "binary relation between individual things",
     ["takes it that", "tells itself that"], ["is taken to be so by"],
     [], ("taking subject", "anything"), ("taken content", "anything"),
     "A higher-order representation the subject holds without its being so; the home of the empty or misrepresenting case.",
     "hot_takes"),
    ("questioning a state", "binary relation between individual things",
     ["wonders whether"], ["is questioned by"],
     [], ("questioning subject", "anything"), ("questioned content", "anything"),
     "Reality monitoring in its interrogative form: the target is held up for judgement rather than asserted.",
     "hot_wonders"),
    ("failure to notice", "binary relation between individual things",
     ["does not notice"], ["is unnoticed by"],
     [], ("unnoticing subject", "anything"), ("unnoticed state", "anything"),
     "Asserted of a state the case says is operative: it works and the subject has no higher-order representation of it. The relation this extension exists for.",
     "hot_blind"),
    ("position in a succession", "binary relation between individual things",
     ["occurs at position"], ["is the position of"],
     [], ("episode", "anything"), ("position", "anything"),
     "Where in the reading or episode this state falls; the value column carries an integer. A batch evaluation has no time of its own, so the text lends it one.",
     "hot_at"),
]

FACTS = [
    ("higher-order theory", "is a kind of", "theory of mind"),
    ("transitivity principle", "is a kind of", "theory of mind"),
    ("empty higher-order representation", "is a kind of", "higher-order representation"),
]
# NOTE: "a higher-order representation is realized in a cognitive code" is a claim of the Synthea framework, not
# of the neutral field, and `cognitive code` lives in the theory layer. Stating it here would smuggle doctrine
# into the vocabulary, so it belongs in ext/synthea_bootstrap if anywhere.


def build(here, deps):
    pom = deps["philosophy_of_mind"]
    e = Ext("higher_order", *COLL, BASE, reference="HOT as a theory of state succession",
            external={**pom.uid, **pom.role_uid}, external_phrases=pom.phrases)
    e.concepts(CONCEPTS)
    e.relations(RELATIONS)
    e.facts(FACTS)
    n = e.write(here)
    print(f"higher_order: {len(CONCEPTS)} concepts, {len(RELATIONS)} relation types, {n} rows")
    return e
