# -*- coding: utf-8 -*-

"""
.. module:: dict.decoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Decodes a term from a python dictionary.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

import arrow

from pyessv.model import Term
from pyessv.model import Authority
from pyessv.model import Scope
from pyessv.model import Collection



def decode(obj):
    """Decodes a term from a dictionary.

    :param dict obj: Dictionary to be decoded.

    :returns: Decoded term.
    :rtype: pyessv.Term

    """
    try:
        _DECODERS[obj['_type']]
    except KeyError:
        raise TypeError("Decoding type unsupported: {}".format(obj['_type']))

    return _DECODERS[obj['_type']](obj)


def _decode_authority(obj):
    """Decodes a termset from a dictionary.

    """
    instance = Authority()
    instance.description = obj['description']
    instance.label = obj['label']
    instance.name = obj['name']
    instance.scopes = [_decode_scope(i) if isinstance(i, dict) else i
                       for i in obj['scopes']]
    instance.url = obj['url']

    # Wire hierarchy.
    for scope in instance:
        if isinstance(scope, Scope):
            scope.authority = instance

    return instance


def _decode_scope(obj):
    """Decodes a termset from a dictionary.

    """
    instance = Scope()
    instance.collections = [_decode_collection(i) if isinstance(i, dict) else i
                            for i in obj['collections']]
    instance.description = obj['description']
    instance.idx = obj['idx']
    instance.label = obj['label']
    instance.name = obj['name']
    instance.uid = uuid.UUID(unicode(obj['uid']))
    instance.url = obj['url']

    # Wire hierarchy.
    for collection in instance:
        if isinstance(collection, Collection):
            collection.scope = instance

    return instance


def _decode_collection(obj):
    """Decodes a termset from a dictionary.

    """
    instance = Collection()
    instance.create_date = arrow.get(obj['create_date']).datetime
    instance.description = obj['description']
    instance.idx = obj['idx']
    instance.label = obj['label']
    instance.name = obj['name']
    instance.terms = [_decode_term(i) if isinstance(i, dict) else i
                      for i in obj['terms']]
    instance.uid = uuid.UUID(unicode(obj['uid']))
    instance.url = obj['url']

    # Wire hierarchy.
    for term in instance:
        if isinstance(term, Term):
            term.collection = instance

    return instance


def _decode_term(obj):
    """Decodes a term from a dictionary.

    """
    instance = Term()
    instance.alternative_name = obj['alternative_name']
    instance.alternative_url = obj['alternative_url']
    instance.create_date = arrow.get(obj['create_date']).datetime
    instance.data = obj['data']
    instance.description = obj['description']
    instance.idx = obj['idx']
    instance.label = obj['label']
    instance.name = obj['name']
    instance.status = obj['status']
    instance.synonyms = obj['synonyms']
    instance.uid = uuid.UUID(unicode(obj['uid']))
    instance.url = obj['url']
    if instance.parent:
        instance.parent = uuid.UUID(unicode(obj['parent']))

    return instance


# Map of supported type keys to decoding functions.
_DECODERS = {
    Authority.__module__: _decode_authority,
    Collection.__module__: _decode_collection,
    Scope.__module__: _decode_scope,
    Term.__module__: _decode_term
}
