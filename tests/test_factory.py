# -*- coding: utf-8 -*-

"""
.. module:: test_authoring.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv authoring tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import nose
import pyessv as LIB

from pyessv import load
from pyessv._utils.compat import str
import tests.utils as tu



@nose.with_setup(None, tu.teardown)
def test_create():
    """Test creating an authority.

    """
    def _test(func, typeof):
        """Inner test.

        """
        node = func()
        tu.assert_object(node, typeof)
        assert node == load(node.namespace)


    for factory, typeof in (
        (tu.create_authority, LIB.Authority),
        (tu.create_scope, LIB.Scope),
        (tu.create_collection_01, LIB.Collection),
        (tu.create_collection_02, LIB.Collection),
        (tu.create_collection_03, LIB.Collection),
        (tu.create_term_01, LIB.Term),
        (tu.create_term_02, LIB.Term),
        (tu.create_term_03, LIB.Term)
        ):
        tu.init(_test, 'create --> {}'.format(factory.__name__[7:]))
        yield _test, factory, typeof
