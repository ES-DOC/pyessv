# -*- coding: utf-8 -*-

"""
.. module:: testmodel.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv model tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pytest

import pyessv as LIB

import tests.utils as tu
import tests.utils_model as tum


# Module level fixture teardown.
teardown_module = tu.teardown


def _yield_parameterizations():
    """Test parameterizations.

    """    
    for node_factory, keys in (
        (tu.create_authority, [tum.SCOPE_NAME]),
        (tu.create_scope, [tum.COLLECTION_01_NAME, tum.COLLECTION_02_NAME, tum.COLLECTION_03_NAME]),
        (tu.create_collection_01, [tum.TERM_01_NAME]),
        (tu.create_collection_02, [tum.TERM_02_NAME]),
        (tu.create_collection_03, [tum.TERM_03_NAME]),
        ):
        yield node_factory(), keys


@pytest.mark.parametrize("node, keys", _yield_parameterizations())
def test_iterability(node, keys):
    """Test iterability of domain model.

    """
    assert iter(node)
    assert len(node) == len(keys)
    for key in keys:
        assert key in node
        assert node[key] is not None
