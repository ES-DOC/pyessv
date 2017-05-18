# -*- coding: utf-8 -*-

"""
.. module:: pyessv._archive.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._cache import cache
from pyessv._cache import get_cached
from pyessv._io_manager import write
from pyessv._utils.formatter import format_canonical_name



def load(authority, scope=None, collection=None, term=None):
    """Loads a CV authority from archive.

    :param str authority: Vocabulary authority, e.g. wcrp.
    :param str scope: Vocabulary scope, e.g. global.
    :param str collection: Vocabulary collection, e.g. institute-id.
    :param str term: Vocabulary term, e.g. ipsl.

    """
    # Format names.
    names = [authority, scope, collection, term]
    names = [format_canonical_name(i) for i in names if i is not None]

    # Set authority (JIT loads cache).
    result = get_cached(names[0])
    if result is None:
        return

    # Return last loaded sub-collection.
    try:
        for name in names[1:]:
            result = result[name]
    except KeyError:
        pass
    else:
        return result


def add(authority):
    """Adds an authority to the archive.

    """
    cache(authority)


def save():
    """Persists archive to file system.

    """
    for authority in get_cached():
        write(authority)

