# -*- coding: utf-8 -*-

"""
.. module:: test_model.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv model tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import nose

import pyessv as LIB

from pyessv._utils.compat import str
import tests.utils as tu
import tests.utils_model as tum



@nose.with_setup(None, tu.teardown)
def test_iterability():
    """Test iterability of domain model.

    """
    def _test(node, keys):
        """Inner test.

        """
        assert iter(node)
        assert len(node) == len(keys)
        for key in keys:
            assert key in node
            assert node[key] is not None


    for node_factory, keys in (
        (tu.create_authority, [tum.SCOPE_NAME]),
        (tu.create_scope, [tum.COLLECTION_01_NAME, tum.COLLECTION_02_NAME, tum.COLLECTION_03_NAME]),
        (tu.create_collection_01, [tum.TERM_01_NAME]),
        (tu.create_collection_02, [tum.TERM_02_NAME]),
        (tu.create_collection_03, [tum.TERM_03_NAME]),
        ):
        desc = 'iterate --> {}'.format(node_factory.__name__[7:])
        tu.init(_test, desc)
        yield _test, node_factory(), keys
