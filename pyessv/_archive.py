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
from pyessv._model import Term
from pyessv._utils.formatter import format_canonical_name
from pyessv._utils.formatter import format_string



def load(authority, scope=None, collection=None, term=None):
    """Loads a CV authority from archive.

    :param str authority: Vocabulary authority, e.g. wcrp.
    :param str scope: Vocabulary scope, e.g. global.
    :param str collection: Vocabulary collection, e.g. institute-id.
    :param str term: Vocabulary term, e.g. ipsl.

    """
    for a in get_cached():
        if not _is_matched(a, authority):
            continue
        if scope is None:
            return a
        for s in a:
            if not _is_matched(s, scope):
                continue
            if collection is None:
                return s
            for c in s:
                if not _is_matched(c, collection):
                    continue
                if term is None:
                    return c
                for t in c:
                    if _is_matched(t, term):
                        return t


def load_by_namespace(identifier):
    """Loads a vocabulary node from archive by trying to match it's namespace.

    :param str identifier: Vocabulary node namespace.

    :returns: First matching vocabulary node.
    :rtype: pyessv.Node | None

    """
    return _load(identifier, lambda n, i: str(n.namespace) == i)


def load_by_uid(identifier):
    """Loads a vocabulary node from archive by trying to match it's unique identifier.

    :param str identifier: Vocabulary node unique identifier.

    :returns: First matching vocabulary node.
    :rtype: pyessv.Node | None

    """
    return _load(identifier, lambda n, i: str(n.uid) == i)


def _load(identifier, predicate):
    """Loads a vocabulary node from archive.

    """
    identifier = format_string(identifier).lower()
    for a in get_cached():
        if predicate(a, identifier):
            return a
        for s in a:
            if predicate(s, identifier):
                return s
            for c in s:
                if predicate(c, identifier):
                    return c
                for t in c:
                    if predicate(t, identifier):
                        return t


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

    # Matched by synonyms.
    elif identifier in [format_string(i).lower() for i in node.synonyms]:
        return True

    # Matched by idx.
    if isinstance(node, Term):
        try:
            int(identifier)
        except ValueError:
            pass
        else:
            if int(identifier) == node.idx:
                return True

    return False


def add(authority):
    """Adds an authority to the archive.

    """
    cache(authority)


def save():
    """Persists archive to file system.

    """
    for authority in get_cached():
        write(authority)

