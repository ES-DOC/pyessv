# -*- coding: utf-8 -*-

"""
.. module:: pyessv._codecs.dict.encoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes a term to a python dictionary.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Node
from pyessv._model import Scope
from pyessv._model import Term
from pyessv._utils.compat import str



def encode(instance):
    """Encodes an instance of a domain model class as a dictionary.

    :param pyessv.Node instance: A domain model class instance to be encoded as a dictionary.

    :returns: Instance encoded as a simple dictionary.
    :rtype: dict

    :raises TypeError: If instance is a domain model class instance.

    """
    assert isinstance(instance, Node), 'Invalid type'

    encoders = {
        Authority: _encode_authority,
        Collection: _encode_collection,
        Scope: _encode_scope,
        Term: _encode_term
        }
    encoder = encoders[type(instance)]

    return encoder(instance)


def _encode_authority(instance):
    """Encodes a term authority as a dictionary.

    """
    obj = _encode_node(instance)
    obj['scopes'] = [encode(i) for i in instance]

    return obj


def _encode_scope(instance):
    """Encodes a term scope as a dictionary.

    """
    obj = _encode_node(instance)
    obj['collections'] = [encode(i) for i in instance]

    return obj


def _encode_collection(instance):
    """Encodes a collection as a dictionary.

    """
    obj = _encode_node(instance)
    obj['terms'] = ['{}:{}'.format(i.canonical_name, i.label) for i in instance]
    obj['term_regex'] = instance.term_regex

    return obj


def _encode_term(instance):
    """Encodes a term as a dictionary.

    """
    obj = _encode_node(instance)
    obj['status'] = instance.status
    if bool(instance.parent):
        obj['parent'] = instance.parent.uid
    if bool(instance.associations):
        obj['associations'] = [i.uid for i in instance.associations]

    return obj


def _encode_node(instance):
    """Encodes a node instance to a dictionary representation.

    """
    obj = dict()
    obj['_type'] = instance.typekey
    obj['canonical_name'] = instance.canonical_name
    obj['create_date'] = instance.create_date
    obj['namespace'] = instance.namespace
    obj['uid'] = instance.uid
    if bool(instance.label) and instance.label != instance.canonical_name:
        obj['label'] = instance.label
    if bool(instance.raw_name) and instance.raw_name != instance.canonical_name:
        obj['raw_name'] = instance.raw_name
    if bool(instance.data):
        obj['data'] = instance.data
    if bool(instance.description):
        obj['description'] = instance.description
    if bool(instance.alternative_names):
        obj['alternative_names'] = instance.alternative_names
    if bool(instance.url):
        obj['url'] = instance.url

    return obj
