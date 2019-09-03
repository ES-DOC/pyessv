# -*- coding: utf-8 -*-

"""
.. module:: testcache.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv cache tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import nose

import pyessv

from pyessv.cache import cache
from pyessv.cache import uncache
from pyessv.cache import getcached
import tests.utils as tu



def test_interface():
	"""pyessv-tests: caching: interface.

	"""
	assert inspect.isfunction(cache)
	assert inspect.isfunction(uncache)
	assert inspect.isfunction(getcached)


@nose.with_setup(tu.create_authority, None)
def testcache():
	"""pyessv-tests: caching: cache

	"""
	assert isinstance(getcached(tu.AUTHORITY_NAME), pyessv.Authority)


@nose.with_setup(tu.create_authority, None)
def test_uncache():
	"""pyessv-tests: caching: uncache

	"""
	uncache(tu.AUTHORITY_NAME)

	assert getcached(tu.AUTHORITY_NAME) is None
