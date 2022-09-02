import inspect

import pyessv
from pyessv.cache import encache
from pyessv.cache import decache
from pyessv.cache import get_cached
import tests.utils as tu


# Module level fixture teardown.
setup_module = tu.create_authority


def test_interface():
	"""pyessv-tests: caching: interface.

	"""
	assert inspect.isfunction(encache)
	assert inspect.isfunction(decache)
	assert inspect.isfunction(get_cached)


def test_cache():
	"""pyessv-tests: caching: cache

	"""
	assert isinstance(get_cached(tu.AUTHORITY_NAME), pyessv.Authority)


def test_decache():
	"""pyessv-tests: caching: decache

	"""
	decache(tu.AUTHORITY_NAME)

	assert get_cached(tu.AUTHORITY_NAME) is None
