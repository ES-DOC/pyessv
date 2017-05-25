# -*- coding: utf-8 -*-

"""
.. module:: pyessv._codecs.dict.encoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes a term to a python dictionary.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._model import Term
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._utils.compat import str



def encode(instance):
    """Encodes an instance of a domain model class as a dictionary.

    :param pyessv.Node instance: A domain model class instance to be encoded as a dictionary.

    :returns: Instance encoded as a simple dictionary.
    :rtype: dict

    :raises TypeError: If instance is a domain model class instance.

    """
    try:
        encoder = _ENCODERS[type(instance)]
    except KeyError:
        raise TypeError('Type encoding unsupported: {}'.format(type(instance)))

    obj = dict()
    _encode_node(instance, obj)
    encoder(instance, obj)

    return obj


def _encode_authority(instance, obj):
    """Encodes a term authority as a dictionary.

    """
    obj['scopes'] = [encode(i) for i in instance]


def _encode_scope(instance, obj):
    """Encodes a term scope as a dictionary.

    """
    obj['collections'] = [encode(i) for i in instance.collections]


def _encode_collection(instance, obj):
    """Encodes a term collection as a dictionary.

    """
    obj['terms'] = ['{}:{}'.format(i.canonical_name, i.uid) for i in instance.terms]
    obj['term_regex'] = instance.term_regex


def _encode_term(instance, obj):
    """Encodes a term as a dictionary.

    """
    obj['idx'] = instance.idx
    obj['status'] = instance.status
    if instance.alternative_name is not None:
        obj['alternative_name'] = instance.alternative_name
    if instance.alternative_url is not None:
        obj['alternative_url'] = instance.alternative_url
    if instance.parent is not None:
        obj['parent'] = instance.parent.uid
    if len(instance.associations) > 0:
        obj['associations'] = [i.uid for i in instance.associations]


def _encode_node(instance, obj):
    """Encodes a node instance to a dictionary representation.

    """
    obj['_type'] = str(instance.__module__)
    obj['canonical_name'] = instance.canonical_name
    obj['create_date'] = instance.create_date
    obj['label'] = instance.label
    obj['raw_name'] = instance.raw_name
    obj['uid'] = instance.uid
    if instance.data is not None:
        obj['data'] = instance.data
    if instance.description is not None:
        obj['description'] = instance.description
    if len(instance.synonyms) > 0:
        obj['synonyms'] = instance.synonyms
    if instance.url is not None:
        obj['url'] = instance.url


# Map of supported types to encoding functions.
_ENCODERS = {
    Authority: _encode_authority,
    Collection: _encode_collection,
    Scope: _encode_scope,
    Term: _encode_term,
}
