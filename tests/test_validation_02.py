# -*- coding: utf-8 -*-

"""
.. module:: test_validation.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv validation tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pyessv
import tests.utils as tu



def test_regex_collection():
    """pyessv-tests: validate --> reg-ex collection

    """
    collection = tu.create_collection_01()
    collection.term_regex = r'^[a-z\-]*$'
    term = tu.create_term_01(collection=collection)
    term.canonical_name = 'abc-def'
    assert pyessv.is_valid(term) == True


def test_regex_collection_negative():
    """pyessv-tests: validate --> reg-ex collection --> negative

    """
    collection = tu.create_collection_01()
    collection.term_regex = r'^[a-z\-]*$'
    term = tu.create_term_01(collection=collection)
    term.canonical_name = 'ABC-DEF'
    assert pyessv.is_valid(term) == False
