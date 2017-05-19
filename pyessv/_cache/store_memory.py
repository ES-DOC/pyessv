# -*- coding: utf-8 -*-

"""
.. module:: pyessv._cache.memory.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Simple in-memory cache store.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._utils.compat import str



# Cached loaded vocabulary authorities objects.
_DATA = {}


def cache(authority):
    """Caches authority vocabularies.

    """
    _DATA[authority.canonical_name] = authority


def get_cached(identifier=None):
    """Caches authority vocabularies.

    :param str identifier: Authority identifier.

    :returns: A pointer to a cached authority.
    :rtype: pyessv.Authority

    """
    if identifier is None:
        return _DATA.values()

    for authority in _DATA.values():
        if authority.canonical_name == identifier:
            return authority
        elif authority.raw_name == identifier:
            return authority
        elif str(authority.uid) == identifier:
            return authority


def uncache(authority_name):
    """Uncaches authority vocabularies.

    :param str authority_name: Authority name.

    """
    try:
        del _DATA[authority_name]
    except KeyError:
        pass
