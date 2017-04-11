# -*- coding: utf-8 -*-

"""
.. module:: pyessv._cache.memory.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Simple in-memory cache store.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Cached loaded vocabulary authorities objects.
_DATA = {}


def cache(authority):
    """Caches authority vocabularies.

    """
    _DATA[authority.name] = authority


def get_cached(authority_name=None):
    """Caches authority vocabularies.

    :param str authority_name: Authority name.

    :returns: A pointer to a cached authority.
    :rtype: pyessv.Authority

    """
    if authority_name is not None:
        try:
            return _DATA[authority_name]
        except KeyError:
            pass
    else:
        return _DATA.values()


def uncache(authority_name):
    """Uncaches authority vocabularies.

    :param str authority_name: Authority name.

    """
    try:
        del _DATA[authority_name]
    except KeyError:
        pass
