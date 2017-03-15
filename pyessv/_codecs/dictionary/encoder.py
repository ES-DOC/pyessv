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



def encode(instance):
    """Encodes an instance of a domain model class as a dictionary.

    :param pyessv.Entity instance: A domain model class instance to be encoded as a dictionary.

    :returns: Instance encoded as a simple dictionary.
    :rtype: dict

    :raises TypeError: If instance is a domain model class instance.

    """
    try:
        _ENCODERS[type(instance)]
    except KeyError:
        raise TypeError("Type encoding unsupported: {}".format(type(instance)))

    obj = _ENCODERS[type(instance)](instance)
    obj['_type'] = unicode(instance.__module__)

    return obj


def _encode_authority(instance):
    """Encodes a term authority as a dictionary.

    """
    obj = dict()
    obj['description'] = instance.description
    obj['label'] = instance.label
    obj['name'] = instance.name
    obj['scopes'] = [_encode_scope(i) for i in instance.scopes]
    obj['url'] = instance.url

    return obj


def _encode_scope(instance):
    """Encodes a term scope as a dictionary.

    """
    obj = dict()
    obj['collections'] = [_encode_collection(i) for i in instance.collections]
    obj['description'] = instance.description
    obj['idx'] = instance.idx
    obj['label'] = instance.label
    obj['name'] = instance.name
    obj['uid'] = instance.uid
    obj['url'] = instance.url

    return obj


def _encode_collection(instance):
    """Encodes a term collection as a dictionary.

    """
    obj = dict()
    obj['create_date'] = instance.create_date
    obj['description'] = instance.description
    obj['idx'] = instance.idx
    obj['label'] = instance.label
    obj['name'] = instance.name
    obj['terms'] = ["{}:{}".format(i.name, i.uid) for i in instance.terms]
    obj['uid'] = instance.uid
    obj['url'] = instance.url

    return obj


def _encode_term(instance):
    """Encodes a term as a dictionary.

    """
    obj = instance.__dict__.copy()
    del obj['collection']
    del obj['io_path']
    obj['parent'] = None if instance.parent is None else instance.parent.uid
    obj['associations'] = [i.uid for i in instance.associations]

    return obj


# Map of supported types to encoding functions.
_ENCODERS = {
    Authority: _encode_authority,
    Collection: _encode_collection,
    Scope: _encode_scope,
    Term: _encode_term,
}
