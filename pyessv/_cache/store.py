# -*- coding: utf-8 -*-

"""
.. module:: pyessv._cache.store.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Manages cache stores.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._cache import store_memory as _memory_store


# Collection of cache stores.
_STORES = (
	_memory_store,
	)


def cache(authority):
    """Caches authority vocabularies.

    """
    for store in _STORES:
    	store.cache(authority)


def get_cached(authority_name=None):
    """Caches authority vocabularies.

    :param str authority_name: Authority name.

    :returns: A pointer to a cached authority.
    :rtype: pyessv.Authority

    """
    return _memory_store.get_cached(authority_name)


def uncache(authority_name):
    """Uncaches authority vocabularies.

    :param str authority_name: Authority name.

    """
    for store in _STORES:
    	store.uncache(authority_name)
