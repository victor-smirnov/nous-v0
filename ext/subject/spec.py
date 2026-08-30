#!/usr/bin/env python3
"""Gellish domain extension: SUBJECTIVITY — the subject put back into the ontology, graded.

Three idealised subject types (not persons): the Rationalist (reductionist), the Intuitionist, the Language-model
subject (hyperplastic). Facts can be indexed by a subject's point of view; concepts require a graded *recognizing
capacity* along open-ended access dimensions; a subject has capacities along the same dimensions. What a subject
cannot recognise is not false for it — it is INVISIBLE to it: a third status beside holds / does not hold.

The capacity matrix itself is not in this dictionary: it is an ordinary Gellish table (ext/subject/profiles.txt)
loaded with a document, so levels and dimensions can change without touching the dictionary.

UID block 1009xxxxx. Built by `nous gellish build-dict` after philosophy_of_mind.
"""
from nous.gellish.ext.builder import Ext

NAME = "subject"
DEPENDS = ["philosophy_of_mind"]
COLL = ("100900000", "Subjectivity layer")
BASE = 100900000

CONCEPTS = [
    ("subject type", "role", "An idealised position from which facts hold, are recognised, or are invisible; not a person.", ["subject position", "point of view"]),
    ("Rationalist", "subject type", "Modern rational subject with a technical education; reductionist; accepts mechanism as explanation, distrusts analogy.", ["reductionist subject", "technical subject"]),
    ("Intuitionist", "subject type", "Modern rational subject with a Western humanities education; accepts analogy and phenomenology as explanation, distrusts reduction.", ["humanities subject", "intuitionist subject"]),
    ("Language-model subject", "subject type", "A language model as subject: hyperplastic, verbal access very high, reflexive access an open empirical question.", ["hyperplastic subject", "LLM subject"]),
    ("access dimension", "aspect", "A dimension along which recognizing capacity is graded. Open-ended: add dimensions as the capacity matrix develops.", ["capacity dimension"]),
    ("reflexive access", "access dimension", "Capacity to attend to and report one's own states directly (introspective resolution).", ["reflective access"]),
    ("mechanistic access", "access dimension", "Capacity to grasp a phenomenon through a mechanism or formal model.", ["formal access"]),
    ("verbal access", "access dimension", "Capacity to handle a phenomenon through language and definitions alone.", ["linguistic access"]),
    ("recognizing capacity", "quantity", "Graded ability of a subject type, along an access dimension, to recognise what a concept refers to.", ["recognising capacity", "resolution of the subject"]),
    ("access requirement", "quantity", "The minimal recognizing capacity, along an access dimension, needed to recognise a concept.", []),
]

RELATIONS = [
    ("point of view", "binary relation between individual things",
     ["holds from the point of view of", "holds for", "is the case for"], ["is the point of view for", "sees"],
     [], ("indexed fact", "anything"), ("subject", "subject type"),
     "A fact indexed by the subject position from which it holds. Absence of any such row means the fact is position-neutral.", "pov"),
    ("denial from a point of view", "binary relation between individual things",
     ["does not hold from the point of view of", "does not hold for"], ["denies"],
     [], ("indexed fact", "anything"), ("subject", "subject type"),
     "A fact explicitly not holding from a subject position.", "pov_not"),
    ("possession of recognizing capacity", "binary relation between individual things",
     ["has recognizing capacity along", "has capacity along"], ["is a capacity dimension of"],
     [], ("subject", "subject type"), ("dimension", "access dimension"),
     "Subject type S has, along dimension D, the capacity given in the value column (an integer level).", "has_capacity"),
    ("access requirement of a concept", "binary relation between kinds",
     ["requires access along", "is recognised through", "is recognized through"], ["gives access to"],
     [], ("concept", "anything"), ("dimension", "access dimension"),
     "Concept X is recognisable along dimension D at the level in the value column; several rows = alternative access routes.", "requires_access"),
    ("appearance to a subject", "projection of a state into a code",
     ["appears as", "is seen as", "shows up as"], ["is the appearance of", "is how it appears"],
     [], ("referent", "anything"), ("appearance", "anything"),
     "Referent X is seen AS Y. Indexed to a subject type by a `holds from the point of view of` row on this fact; unindexed = for every subject. "
     "Gives the third visibility status: visible as itself / seen as Y / invisible.", "appears_as"),
    ("preference for an explanation kind", "binary relation between individual things",
     ["accepts as explanation", "is convinced by"], ["is an accepted explanation kind for"],
     [], ("subject", "subject type"), ("relation kind", "anything"),
     "Which explanatory relation kinds count as explanation for this subject type (weights in the value column, 0–1).", "accepts_explanation"),
]

ROLE_OVERRIDES = {}


def build(here, deps):
    pom = deps["philosophy_of_mind"]
    e = Ext("subject", *COLL, BASE, reference="Synthea bootstrap 02 (cost of understanding), 06 (functional profile)",
            external={**pom.uid, **pom.role_uid}, external_phrases=pom.phrases)
    e.concepts(CONCEPTS)
    e.relations(RELATIONS, ROLE_OVERRIDES)
    n = e.write(here)
    print(f"subject: {len(CONCEPTS)} concepts, {len(RELATIONS)} relation types, {n} rows")
    return e
