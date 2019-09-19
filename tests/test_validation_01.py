# -*- coding: utf-8 -*-

"""
.. module:: test_validation.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv validation tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pytest

import pyessv
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
    pyessv.Authority: _NODE_TEST_INFO + [
        ('scopes', [None, '', '  ', [123]])
    ],
    pyessv.Scope: _NODE_TEST_INFO + [
        ('collections', [None, '', '  ', [123]])
    ],
    pyessv.Collection: _NODE_TEST_INFO + [
        ('terms', [None, '', '  ', [123]])
    ],
    pyessv.Term: _NODE_TEST_INFO + [
        ('status', ('', '  ', [123])),
        ('alternative_names', ('', '  ', [123])),
    ],
}


def _yield_parameterizations():
    """Test parameterizations.

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
            yield node, attr, invalid


@pytest.mark.parametrize("node, attr, invalid_values", _yield_parameterizations())
def test_node_attr(node, attr, invalid_values):
    """Tests node attribute validation.

    """
    valid_value = getattr(node, attr)
    for value in invalid_values:
        setattr(node, attr, value)
        assert pyessv.is_valid(node) == False, (attr, value)
        assert len(pyessv.get_errors(node)) >= 1, (pyessv.get_errors(node), attr, value)

    setattr(node, attr, valid_value)
    assert pyessv.is_valid(node) == True, (pyessv.get_errors(node), attr, valid_value)
    assert len(pyessv.get_errors(node)) == 0
