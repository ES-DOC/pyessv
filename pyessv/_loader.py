# -*- coding: utf-8 -*-

"""
.. module:: pyessv._loader.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Orchestrates reading & caching of entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import random
import uuid

from pyessv._cache import cache
from pyessv._cache import get_cached
from pyessv._constants import PARSING_NODE_FIELDS
from pyessv._factory import create_term
from pyessv._model import Authority
from pyessv._model import Term
from pyessv._utils import logger
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
from pyessv._utils.formatter import format_string



def load(identifier=None, verbose=True):
    """Loads a vocabulary node from archive.

    :param str identifier: Vocabulary node identifier.

    :return: A vocabulary node.
    :rtype: pyessv.Node | None

    """
    assert isinstance(identifier, (type(None), basestring))

    if identifier is None:
        return set(get_cached(Authority))

    identifier = identifier.strip()
    result = _load_by_namespace(identifier)
    if result is None:
        result = _load_by_uid(identifier)
        if result is None and verbose:
            logger.log_warning('Cannot map identifier to a vocabulary entity: {}'.format(identifier))

    return result


def _load_by_namespace(identifier):
    """Loads a vocabulary node from archive by trying to match it's namespace.

    :param str identifier: Vocabulary node namespace.

    :returns: First matching vocabulary node.
    :rtype: pyessv.Node | None

    """
    # Skip if identifier is not a namespace.
    ns = str(identifier).split(':')
    if len(ns) == 0:
        return get_cached(Authority)
    if len(ns) > 4:
        return None

    # Unpack.
    authority = scope = collection = term = None
    if len(ns) == 1:
        authority = ns[0]
    elif len(ns) == 2:
        authority, scope = ns
    elif len(ns) == 3:
        authority, scope, collection = ns
    elif len(ns) == 4:
        authority, scope, collection, term = ns

    # Walk nodes returning deepest match.
    for a in get_cached(Authority):
        if not _is_matched(a, authority):
            continue
        if scope is None:
            return a
        # ... scopes
        for s in a:
            if not _is_matched(s, scope):
                continue
            if collection is None:
                return s
            # ... collections
            for c in s:
                if not _is_matched(c, collection):
                    continue
                if term is None:
                    return c
                # ... terms (concrete)
                for t in c:
                    if _is_matched(t, term):
                        return t
                # ... terms (virtual)
                if c.is_matched(term):
                    return create_term(c, term)


def _load_by_uid(identifier):
    """Loads a vocabulary node from archive by trying to match it's unique identifier.

    :param str identifier: Vocabulary node unique identifier.

    :returns: First matching vocabulary node.
    :rtype: pyessv.Node | None

    """
    try:
        uuid.UUID(identifier)
    except ValueError:
        pass
    else:
        return get_cached(str(identifier))


def _is_matched(node, identifier):
    """Returns flag indicating whether node identifier is a match.

    """
    identifier = format_string(identifier).lower()

    # Matched by canonical name.
    if identifier == node.canonical_name:
        return True

    # Matched by raw name.
    if identifier == node.raw_name.lower():
        return True

    # Matched by uid.
    elif identifier == format_string(node.uid).lower():
        return True

    # Matched by alternative names.
    elif identifier in [format_string(i).lower() for i in node.alternative_names]:
        return True

    return False


def load_random(namespace, field='canonical_name'):
    """Returns a random term.

    :param str namespace: Namespace of collection from which a term will be loaded.

    :returns: A random term's canonical name.
    :rtype: str

    """
    collection = load(namespace)
    if collection is None:
        raise ValueError('Collection not found: {}'.format(namespace))
    if field not in PARSING_NODE_FIELDS:
        raise ValueError('Invalid field name')

    if collection.is_virtual:
        return str(uuid.uuid4()).split('-')[0]

    term = random.choice(collection.terms)

    return getattr(term, field)
