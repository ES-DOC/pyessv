# -*- coding: utf-8 -*-

"""
.. module:: pyessv._cache.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to simple in-memory cache of vocabulary objects.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

import pyessv



# Cached loaded vocabulary authorities objects.
_DATA = {}


def cache_authority(target):
    """Caches authority vocabularies.

    """
    if target in _DATA.keys() or target in _DATA.items():
        pass
    elif isinstance(target, pyessv.Authority):
        _DATA[target.name] = target
    else:
        authority = pyessv.read_authority(target)
        if authority is None:
            raise ValueError("Authority ({}) archive not loaded".format(target))
        _DATA[authority.name] = authority


def get_cached_authority(target):
    """Caches authority vocabularies.

    :param str target: Authority name.

    :returns: A pointer to a cached authority.
    :rtype: pyessv.Authority

    """
    cache_authority(target)
    try:
        return _DATA[target]
    except KeyError:
        pass


def uncache_authority(target):
    """Uncaches authority vocabularies.

    :param str target: Authority instance or name.

    """
    cache_key = target.name if isinstance(target, pyessv.Authority) else target
    try:
        del _DATA[cache_key]
    except KeyError:
        pass
