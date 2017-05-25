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
from pyessv._utils.compat import str



def decode(obj):
    """Decodes a term from a dictionary.

    :param dict obj: Dictionary to be decoded.

    :returns: Decoded term.
    :rtype: pyessv.Term

    """
    typeof = _get_type(obj)
    instance = typeof()
    _decode_node(obj, instance)
    _DECODERS[typeof](obj, instance)

    return instance


def _get_type(obj):
    """Returns type to be decoded.

    """
    try:
        typekey = obj['_type']
    except KeyError:
        raise TypeError('Decoding type key not found')
    else:
        try:
            return _TYPE_MAP[typekey]
        except KeyError:
            raise TypeError('Decoding type unsupported: {}'.format(typekey))


def _decode_authority(obj, instance):
    """Decodes a termset from a dictionary.

    """
    for scope in [decode(i) for i in obj['scopes']]:
        scope.authority = instance
        instance.scopes.append(scope)


def _decode_scope(obj, instance):
    """Decodes a termset from a dictionary.

    """
    for collection in [decode(i) for i in obj['collections']]:
        collection.scope = instance
        instance.collections.append(collection)


def _decode_collection(obj, collection):
    """Decodes a termset from a dictionary.

    """
    collection.term_regex = obj.get('term_regex')


def _decode_term(obj, instance):
    """Decodes a term from a dictionary.

    """
    instance.alternative_name = obj.get('alternative_name')
    instance.alternative_url = obj.get('alternative_url')
    instance.associations = obj.get('associations', [])
    instance.idx = obj['idx']
    instance.status = obj['status']
    if instance.parent:
        instance.parent = uuid.UUID(str(obj['parent']))


def _decode_node(obj, instance):
    """Decodes a node instance from a dictionary representation.

    """
    instance.create_date = arrow.get(obj['create_date']).datetime
    instance.data = obj.get('data', dict())
    instance.description = obj.get('description')
    instance.label = obj['label']
    instance.canonical_name = obj['canonical_name']
    instance.raw_name = obj.get('raw_name')
    instance.synonyms = obj.get('synonyms', [])
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
