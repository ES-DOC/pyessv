# -*- coding: utf-8 -*-

"""
.. module:: pyessv.archive.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

import pyessv
from pyessv._io import read_authority



# Cached loaded vocabulary authorities objects.
_CACHE = {}


def load(authority, scope=None, collection=None, term=None):
    """Loads a CV authority from archive.

    :param str authority: Vocabulary authority, e.g. wcrp.
    :param str scope: Vocabulary scope, e.g. global.
    :param str collection: Vocabulary collection, e.g. institute-id.
    :param str term: Vocabulary term, e.g. ipsl.

    """
    # Format names.
    names = [authority, scope, collection, term]
    names = [_format_name(i) for i in names if i is not None]

    # JIT cache authority vocabularies.
    if names[0] not in _CACHE:
        _set_cache(names[0])

    # Recursively load.
    result = _CACHE[names[0]]
    try:
        for name in names[1:]:
            result = result[name]
    except KeyError:
        pass
    else:
        return result


def _set_cache(name):
    """Caches set of  authority vocabs (if necessary).

    """
    # Set path to authority archive.
    dpath = os.path.expanduser(pyessv.DIR_ARCHIVE)
    dpath = os.path.join(dpath, name)
    if not os.path.isdir(dpath):
        raise ValueError("Authority ({}) archive not found".format(name))

    # Read vocab files from file system.
    authority = read_authority(dpath)
    if authority is None:
        raise ValueError("Authority ({}) archive not loaded".format(authority))

    _CACHE[name] = authority


def _format_name(name):
    """Formats a name prior to accessing archive.

    """
    if name is not None:
        return unicode(name).strip().lower()
