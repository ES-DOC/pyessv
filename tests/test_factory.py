# -*- coding: utf-8 -*-

"""
.. module:: test_authoring.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv authoring tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pytest

from pyessv import load
from pyessv import Authority
from pyessv import Collection
from pyessv import Scope
from pyessv import Term
from . import utils as tu


# Module level fixture teardown.
teardown_module = tu.teardown


def _yield_parameterizations():
    """Test parameterizations.

    """    
    for factory, typeof in (
        (tu.create_authority, Authority),
        (tu.create_scope, Scope),
        (tu.create_collection_01, Collection),
        (tu.create_collection_02, Collection),
        (tu.create_collection_03, Collection),
        (tu.create_term_01, Term),
        (tu.create_term_02, Term),
        (tu.create_term_03, Term)
        ):
        yield factory, typeof


@pytest.mark.parametrize("node_factory, node_type", _yield_parameterizations())
def test_create(node_factory, node_type):
    """Test instantiation of domain entities.

    """
    node = node_factory()
    tu.assert_object(node, node_type)
    loaded = load(node.namespace)
    assert node.namespace == loaded.namespace
    assert repr(node) == repr(loaded)
