"""
.. module:: pyessv.cache.memory.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Simple in-memory cache store.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.model import NODE_TYPES
from pyessv.model import Authority



# Cached loaded vocabulary authorities objects.
_DATA = {}


def cache(node):
    """Caches a vocabulary node.

    :param pyeesv.Node: Node to be cached.

    """
    _DATA[node.namespace] = node
    try:
        iter(node)
    except TypeError:
        return
    else:
        for subnode in node:
            cache(subnode)


def get_cached(cache_filter):
    """Returns a cached node.

    :param str|class filter: Cache filter expression.

    :returns: A pointer to a vocabulary node or a set of nodes.
    :rtype: pyessv.Node | list[Authority]

    """
    if cache_filter in _DATA:
        return _DATA[cache_filter]
    elif cache_filter in NODE_TYPES:
        return [i for i in _DATA.values() if isinstance(i, cache_filter)]
    elif cache_filter is None:
        return get_cached(Authority)


def uncache(identifier):
    """Uncaches a node.

    :param str identifier: A vocabulary node identifier.

    """
    try:
        del _DATA[identifier]
    except KeyError:
        pass
