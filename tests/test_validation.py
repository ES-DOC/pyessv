# -*- coding: utf-8 -*-

"""
.. module:: test_validation.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv validation tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import arrow

import pyessv as LIB
import tests.utils as tu



# Node level test information.
_NODE_TEST_INFO = [
    ('create_date', arrow.utcnow().datetime, ('', '  ', 123)),
    ('data', {'a': 1}, ('', '  ', 123)),
    ('description', tu.TEST_AUTHORITY_DESCRIPTION, ('', '  ')),
    ('canonical_name', tu.TEST_AUTHORITY_NAME, (None, '', '  ', 'invalid-CANONICAL-name')),
    ('url', tu.TEST_AUTHORITY_URL, ('', '  ', 'an-invalid-url')),
    ]


# Test information mapped by node type.
_TEST_INFO = {
    LIB.NODE_TYPEKEY_AUTHORITY: _NODE_TEST_INFO + [
        ('scopes', [], [None, '', '  ', [123]])
    ],
    LIB.NODE_TYPEKEY_SCOPE: _NODE_TEST_INFO + [
        ('collections', [], [None, '', '  ', [123]])
    ],
    LIB.NODE_TYPEKEY_COLLECTION: _NODE_TEST_INFO + [
        ('terms', [], [None, '', '  ', [123]])
    ],
    LIB.NODE_TYPEKEY_TERM: _NODE_TEST_INFO + [
        ('alternative_name', tu.TEST_AUTHORITY_ALTERNATIVE_NAME, ('', '  ')),
        ('alternative_url', tu.TEST_AUTHORITY_ALTERNATIVE_URL, ('', '  ')),
        ('idx', 1, ('', '  ', [123])),
        ('status', LIB.GOVERNANCE_STATUS_PENDING, ('', '  ', [123])),
        ('synonyms', tu.TEST_TERM_SYNONYMS, ('', '  ', [123])),
    ],
}


def test_node():
    """Tests node validation.

    """
    for typeof, factory in (
        (LIB.NODE_TYPEKEY_AUTHORITY, tu.create_authority),
        (LIB.NODE_TYPEKEY_SCOPE, tu.create_scope),
        (LIB.NODE_TYPEKEY_COLLECTION, tu.create_collection),
        (LIB.NODE_TYPEKEY_TERM, tu.create_term)
        ):
        for attr, valid, invalid in _TEST_INFO[typeof]:
            tu.init(_test_node_attr, 'validate --> {}: {}'.format(typeof, attr))
            yield _test_node_attr, factory, attr, valid, invalid


def _test_node_attr(factory, attr, valid_value, invalid_values):
    """Tests node attribute validation.

    """
    instance = factory()
    for value in invalid_values:
        setattr(instance, attr, value)
        assert LIB.is_valid(instance) == False, (attr, value)
        assert len(LIB.get_errors(instance)) >= 1, (LIB.get_errors(instance), attr, value)
    setattr(instance, attr, valid_value)
    assert LIB.is_valid(instance) == True, (LIB.get_errors(instance), attr, valid_value)
    assert len(LIB.get_errors(instance)) == 0


def test_regex_collection():
    """pyessv-tests: validate --> reg-ex collection

    """
    collection = tu.create_collection()
    collection.term_regex = r'^[a-z\-]*$'
    term = tu.create_term(collection=collection)
    term.canonical_name = 'abc-def'
    assert LIB.is_valid(term) == True


def test_regex_collection_negative():
    """pyessv-tests: validate --> reg-ex collection --> negative

    """
    collection = tu.create_collection()
    collection.term_regex = r'^[a-z\-]*$'
    term = tu.create_term(collection=collection)
    term.canonical_name = 'ABC-DEF'
    assert LIB.is_valid(term) == False
