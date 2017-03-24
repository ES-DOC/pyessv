# -*- coding: utf-8 -*-

"""
.. module:: pyessv._cache.store.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Manages cache stores.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._cache import store_memory


# Collection of cache stores.
_STORES = (
	store_memory,
	)


def cache(authority):
    """Caches authority vocabularies.

    """
    for store in _STORES:
    	store.cache(authority)


def get_cached(authority_name):
    """Caches authority vocabularies.

    :param str authority_name: Authority name.

    :returns: A pointer to a cached authority.
    :rtype: pyessv.Authority

    """
    for store in _STORES:
    	authority = store.get_cached(authority_name)
    	if authority is not None:
    		return authority


def uncache(authority_name):
    """Uncaches authority vocabularies.

    :param str authority_name: Authority name.

    """
    for store in _STORES:
    	store.uncache(authority_name)
