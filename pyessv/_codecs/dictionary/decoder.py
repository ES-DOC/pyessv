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

from pyessv._model import Term
from pyessv._model import Authority
from pyessv._model import Scope
from pyessv._model import Collection



def decode(obj):
    """Decodes a term from a dictionary.

    :param dict obj: Dictionary to be decoded.

    :returns: Decoded term.
    :rtype: pyessv.Term

    """
    # Set type key.
    try:
        typekey = obj['_type']
    except KeyError:
        raise TypeError('Decoding type key not found')

    # Set type.
    try:
        typeof = _TYPE_MAP[typekey]
    except KeyError:
        raise TypeError('Decoding type unsupported: {}'.format(typekey))
    else:
        decoder = _DECODERS[typeof]

    # Instantite & set attributes.
    instance = typeof()
    _decode_entity(obj, instance)
    decoder(obj, instance)

    return instance


def _decode_authority(obj, instance):
    """Decodes a termset from a dictionary.

    """
    instance.scopes = [decode(i) for i in obj['scopes']]

    # Wire hierarchy.
    for scope in instance:
        if isinstance(scope, Scope):
            scope.authority = instance


def _decode_scope(obj, instance):
    """Decodes a termset from a dictionary.

    """
    instance.collections = [decode(i) for i in obj['collections']]

    # Wire hierarchy.
    for collection in instance:
        if isinstance(collection, Collection):
            collection.scope = instance


def _decode_collection(obj, instance):
    """Decodes a termset from a dictionary.

    """
    instance.terms = [decode(i) if isinstance(i, dict) else i for i in obj['terms']]
    instance.term_name_regex = obj.get('term_name_regex')

    # Wire hierarchy.
    for term in [instance]:
        if isinstance(term, Term):
            term.collection = instance


def _decode_term(obj, instance):
    """Decodes a term from a dictionary.

    """
    instance.alternative_name = obj.get('alternative_name')
    instance.alternative_url = obj.get('alternative_url')
    instance.associations = obj.get('associations', [])
    instance.idx = obj['idx']
    instance.status = obj['status']
    instance.synonyms = obj.get('synonyms', [])
    if instance.parent:
        instance.parent = uuid.UUID(str(obj['parent']))


def _decode_entity(obj, instance):
    """Decodes an entity instance from a dictionary representation.

    """
    instance.create_date = arrow.get(obj['create_date']).datetime
    instance.data = obj.get('data', dict())
    instance.description = obj['description']
    instance.label = obj['label']
    instance.name = obj['name']
    instance.uid = uuid.UUID(str(obj['uid']))
    instance.url = obj.get('url')


# Map of supported types to decoding functions.
_DECODERS = {
    Authority: _decode_authority,
    Collection: _decode_collection,
    Scope: _decode_scope,
    Term: _decode_term
}

# Map of supported type keys to types.
_TYPE_MAP = {
    Authority.__module__: Authority,
    Collection.__module__: Collection,
    Scope.__module__: Scope,
    Term.__module__: Term
}