from pyessv.cache import store_memory as _memory_store
from pyessv.constants import CACHE_STORE_MEMORY
from pyessv.constants import CACHE_STORE_TYPES
from pyessv.model import Node

# Cache stores.
_STORES = {
    CACHE_STORE_MEMORY: _memory_store
}


def decache(identifier):
    """Uncaches a node.

    :param str identifier: A vocabulary node identifier.

    """
    for store in _STORES.values():
        store.decache(identifier)


def encache(node):
    """Caches a vocabulary node.

    :param pyeesv.Node: Node to be cached.

    """
    assert isinstance(node, Node), 'Invalid node'

    for store in _STORES.values():
        store.cache(node)


def get_cached(identifier=None, store_type=CACHE_STORE_MEMORY):
    """Returns a cached node.

    :param str|None|class filter: Cache filter expression.
    :param str store_type: Cache store type.

    :returns: A pointer to a vocabulary node or a set of nodes.
    :rtype: pyessv.Node | list[Authority]

    """
    assert store_type in CACHE_STORE_TYPES, 'Invalid cache store type'

    return _STORES[store_type].get_cached(identifier)
