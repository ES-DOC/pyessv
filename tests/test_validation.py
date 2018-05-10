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
import nose

import pyessv as LIB
import tests.utils as tu
import tests.utils_model as tum



# Node level test information.
_NODE_TEST_INFO = [
    ('create_date', ('', '  ', 123)),
    ('data', ('', '  ', 123)),
    ('description', ('', '  ')),
    ('canonical_name', (None, '', '  ', 'invalid-CANONICAL-name!')),
    ('url', ('', '  ', 'an-invalid-url')),
    ]


# Test information mapped by node type.
_TEST_INFO = {
    LIB.Authority: _NODE_TEST_INFO + [
        ('scopes', [None, '', '  ', [123]])
    ],
    LIB.Scope: _NODE_TEST_INFO + [
        ('collections', [None, '', '  ', [123]])
    ],
    LIB.Collection: _NODE_TEST_INFO + [
        ('terms', [None, '', '  ', [123]])
    ],
    LIB.Term: _NODE_TEST_INFO + [
        ('status', ('', '  ', [123])),
        ('alternative_names', ('', '  ', [123])),
    ],
}


@nose.with_setup(None, tu.teardown)
def test_node():
    """Tests node validation.

    """
    for node_factory in (
        tu.create_authority,
        tu.create_scope,
        tu.create_collection_01,
        tu.create_collection_02,
        tu.create_collection_03,
        tu.create_term_01,
        tu.create_term_02,
        tu.create_term_03
        ):
        node = node_factory()
        for attr, invalid in _TEST_INFO[type(node)]:
            tu.init(_test_node_attr, 'validate --> {}: {}'.format(node_factory.__name__[7:], attr))
            yield _test_node_attr, node, attr, invalid


def _test_node_attr(instance, attr, invalid_values):
    """Tests node attribute validation.

    """
    valid_value = getattr(instance, attr)
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
    collection = tu.create_collection_01()
    collection.term_regex = r'^[a-z\-]*$'
    term = tu.create_term_01(collection=collection)
    term.canonical_name = 'abc-def'
    assert LIB.is_valid(term) == True


def test_regex_collection_negative():
    """pyessv-tests: validate --> reg-ex collection --> negative

    """
    collection = tu.create_collection_01()
    collection.term_regex = r'^[a-z\-]*$'
    term = tu.create_term_01(collection=collection)
    term.canonical_name = 'ABC-DEF'
    assert LIB.is_valid(term) == False
