# -*- coding: utf-8 -*-

"""
.. module:: test_cache.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv cache tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import nose

import pyessv

from pyessv._cache import cache
from pyessv._cache import uncache
from pyessv._cache import get_cached
import tests.utils as tu



def test_interface():
	"""pyessv-tests: caching: interface.

	"""
	assert inspect.isfunction(cache)
	assert inspect.isfunction(uncache)
	assert inspect.isfunction(get_cached)


@nose.with_setup(tu.create_authority, None)
def test_cache():
	"""pyessv-tests: caching: cache

	"""
	assert isinstance(get_cached(tu.AUTHORITY_NAME), pyessv.Authority)


@nose.with_setup(tu.create_authority, None)
def test_uncache():
	"""pyessv-tests: caching: uncache

	"""
	uncache(tu.AUTHORITY_NAME)

	assert get_cached(tu.AUTHORITY_NAME) is None
