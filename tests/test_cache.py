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


def test_get_cached():
	"""pyessv-tests: caching: get_cached

	"""
	assert isinstance(get_cached('wcrp'), pyessv.Authority)


def test_cache():
	"""pyessv-tests: caching: cache

	"""
	cache(tu.create_authority())

	assert isinstance(get_cached(tu.TEST_AUTHORITY_NAME), pyessv.Authority)


def test_uncache():
	"""pyessv-tests: caching: uncache

	"""
	cache(tu.create_authority())
	uncache(tu.TEST_AUTHORITY_NAME)

	assert get_cached(tu.TEST_AUTHORITY_NAME) is None
