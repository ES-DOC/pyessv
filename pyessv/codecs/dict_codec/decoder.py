"""
.. module:: dict.decoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Decodes a term from a python dictionary.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.constants import NODE_TYPEKEY_AUTHORITY
from pyessv.constants import NODE_TYPEKEY_COLLECTION
from pyessv.constants import NODE_TYPEKEY_SCOPE
from pyessv.constants import NODE_TYPEKEY_SET
from pyessv.constants import NODE_TYPEKEY_TERM
from pyessv.model import Authority
from pyessv.model import Collection
from pyessv.model import Scope
from pyessv.model import Term
from pyessv.utils import compat



def _decode_node(obj, typeof):
    """Decodes a node instance from a dictionary representation.

    """
    instance = typeof()
    instance.alternative_names = obj.get('alternative_names', [])
    instance.create_date = compat.to_datetime(obj['create_date'])
    instance.data = obj.get('data', dict())
    instance.description = obj.get('description')
    instance.label = obj.get('label', obj['canonical_name'])
    instance.canonical_name = obj['canonical_name']
    instance.raw_name = obj.get('raw_name', obj['canonical_name'])
    instance.url = obj.get('url')

    return instance


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

    return instance


# Map of node type to decoder.
_DECODERS = {
    NODE_TYPEKEY_AUTHORITY: _decode_authority,
    NODE_TYPEKEY_COLLECTION: _decode_collection,
    NODE_TYPEKEY_SCOPE: _decode_scope,
    NODE_TYPEKEY_TERM: _decode_term
    }


def decode(obj):
    """Decodes a term from a dictionary.

    :param dict obj: Dictionary to be decoded.

    :returns: Decoded term.
    :rtype: pyessv.Term

    """
    assert '_type' in obj, 'Invalid type key'
    assert obj['_type'] in NODE_TYPEKEY_SET, 'Invalid domain type key: {}'.format(obj['_type'])

    decoder = _DECODERS[obj['_type']]

    return decoder(obj)
