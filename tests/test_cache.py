import inspect

import pyessv

from pyessv.cache import cache
from pyessv.cache import uncache
from pyessv.cache import get_cached
import tests.utils as tu


# Module level fixture teardown.
setup_module = tu.create_authority


def test_interface():
	"""pyessv-tests: caching: interface.

	"""
	assert inspect.isfunction(cache)
	assert inspect.isfunction(uncache)
	assert inspect.isfunction(get_cached)


def test_cache():
	"""pyessv-tests: caching: cache

	"""
	assert isinstance(get_cached(tu.AUTHORITY_NAME), pyessv.Authority)


def test_uncache():
	"""pyessv-tests: caching: uncache

	"""
	uncache(tu.AUTHORITY_NAME)

	assert get_cached(tu.AUTHORITY_NAME) is None
