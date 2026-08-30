#!/usr/bin/env python3
"""Gellish domain extension: DOCUMENT STRUCTURE — the parts of a document and references between them.

Encoders lose internal cross-references ("as argued in Section 4.2", "see the table above", links to other
documents) because no relation carries them; the shell-withheld decode dropped every one of them. This tiny
extension gives them a home. Not philosophy of mind, not a theory: the document as an object.

UID block 1010xxxxx. Built by `nous gellish build-dict` after philosophy_of_mind.
"""
from nous.gellish.ext.builder import Ext

NAME = "document"
DEPENDS = ["philosophy_of_mind"]
COLL = ("101000000", "Document structure")
BASE = 101000000

CONCEPTS = [
    ("document section", "information", "A numbered or titled part of a document.", ["section", "chapter", "subsection"]),
    ("document element", "information", "A figure, table, list, footnote or equation of a document.", ["figure", "table of a document", "footnote", "equation"]),
    ("external document", "information", "A document other than this one, referred to by this one.", []),
]

RELATIONS = [
    ("treatment in a section", "binary relation between individual things",
     ["is discussed in", "is treated in", "is introduced in", "is elaborated in"], ["discusses", "treats", "introduces"],
     [], ("subject matter", "anything"), ("section", "document section"),
     "The claim or thing is developed in the named section of this document — the home of '(Section 4.2)'.", None),
    ("reference to a document element", "binary relation between individual things",
     ["is shown in", "is listed in", "is stated in"], ["shows", "lists"],
     [], ("subject matter", "anything"), ("element", "document element"),
     "The claim is presented in a figure, table or footnote of this document.", None),
    ("reference to another document", "binary relation between individual things",
     ["is set out in", "refers for detail to"], ["sets out"],
     [], ("subject matter", "anything"), ("document", "external document"),
     "The claim is developed elsewhere: a link or a citation used as a pointer, not as provenance.", None),
]


def build(here, deps):
    pom = deps["philosophy_of_mind"]
    e = Ext("document", *COLL, BASE, reference="spec v3.1 cross-reference rule",
            external={**pom.uid, **pom.role_uid}, external_phrases=pom.phrases)
    e.concepts(CONCEPTS)
    e.relations(RELATIONS)
    n = e.write(here)
    print(f"document: {len(CONCEPTS)} concepts, {len(RELATIONS)} relation types, {n} rows")
    return e
