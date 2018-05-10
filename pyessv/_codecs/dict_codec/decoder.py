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

from pyessv._constants import NODE_TYPEKEY_AUTHORITY
from pyessv._constants import NODE_TYPEKEY_COLLECTION
from pyessv._constants import NODE_TYPEKEY_SCOPE
from pyessv._constants import NODE_TYPEKEY_SET
from pyessv._constants import NODE_TYPEKEY_TERM
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._model import Term
from pyessv._utils import convert
from pyessv._utils.compat import str



def decode(obj):
    """Decodes a term from a dictionary.

    :param dict obj: Dictionary to be decoded.

    :returns: Decoded term.
    :rtype: pyessv.Term

    """
    assert '_type' in obj, 'Invalid type key'
    assert obj['_type'] in NODE_TYPEKEY_SET, 'Invalid type key'

    decoders = {
        NODE_TYPEKEY_AUTHORITY: _decode_authority,
        NODE_TYPEKEY_COLLECTION: _decode_collection,
        NODE_TYPEKEY_SCOPE: _decode_scope,
        NODE_TYPEKEY_TERM: _decode_term
        }
    decoder = decoders[obj['_type']]

    return decoder(obj)


def _decode_authority(obj):
    """Decodes a termset from a dictionary.

    """
    instance = _decode_node(obj, Authority)
    for scope in [decode(i) for i in obj['scopes']]:
        scope.authority = instance
        instance.scopes.append(scope)

    return instance


def _decode_scope(obj):
    """Decodes a termset from a dictionary.

    """
    instance = _decode_node(obj, Scope)
    for collection in [decode(i) for i in obj['collections']]:
        collection.scope = instance
        instance.collections.append(collection)

    return instance


def _decode_collection(obj):
    """Decodes a collection from a dictionary.

    """
    instance = _decode_node(obj, Collection)
    instance.term_regex = obj.get('term_regex')

    return instance


def _decode_term(obj):
    """Decodes a term from a dictionary.

    """
    instance = _decode_node(obj, Term)
    instance.associations = obj.get('associations', [])
    instance.status = obj['status']
    if instance.parent:
        instance.parent = uuid.UUID(str(obj['parent']))

    return instance


def _decode_node(obj, typeof):
    """Decodes a node instance from a dictionary representation.

    """
    instance = typeof()
    instance.alternative_names = obj.get('alternative_names', [])
    instance.create_date = arrow.get(obj['create_date']).datetime
    instance.data = obj.get('data', dict())
    instance.description = obj.get('description')
    instance.label = obj.get('label', obj['canonical_name'])
    instance.canonical_name = obj['canonical_name']
    instance.raw_name = obj.get('raw_name', obj['canonical_name'])
    instance.uid = uuid.UUID(str(obj['uid']))
    instance.url = obj.get('url')

    return instance
