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



@nose.with_setup(None, tu.teardown)
def test_iterability():
    """Test iterability of domain model.

    """
    def _test(node, count, key):
        """Inner test.

        """
        assert iter(node)
        assert len(node) == count
        assert key in node
        assert node[key] is not None


    _, collection, scope, authority = tu.create_test_entities()
    for node, count, key in (
        (collection, 1, tu.TEST_TERM_NAME),
        (scope, 1, tu.TEST_COLLECTION_NAME),
        (authority, 1, tu.TEST_SCOPE_NAME)
        ):
        desc = 'iterate --> {}'.format(str(type(node)).split('.')[-1][0:-2].lower())
        tu.init(_test, desc)
        yield _test, node, 1, key
