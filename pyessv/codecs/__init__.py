# -*- coding: utf-8 -*-

"""
.. module:: pyessv.codecs.__init__.py
   :copyright: Copyright "Sep 4, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates transformations of terms from one format to another.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.codecs import dictionary
from pyessv.codecs import json
from pyessv.constants import ENCODING_DICT
from pyessv.constants import ENCODING_JSON
from pyessv.model import TYPES



# Codecs mapped by encoding.
_CODECS = {
	ENCODING_DICT: dictionary,
	ENCODING_JSON: json
}

# Map of encodings to allowed input types when decoding.
_DECODE_TYPE_WHITELIST = {
    ENCODING_DICT : (dict, ),
    ENCODING_JSON : (str, unicode)
}


def _decode(target, encoding=ENCODING_JSON):
    """Returns a decoded domain model class instance.

    :param basestring|dict target: A domain model class instance representation.
    :param str encoding: A supported encoding (dict|json).

    :returns: A domain model class instance.
    :rtype: object

    """
    if target is None:
        raise ValueError("Cannot decode a null pointer.")
    if not encoding in _CODECS:
        raise NotImplementedError('Unsupported term encoding :: {0}.'.format(encoding))
    if not isinstance(target, _DECODE_TYPE_WHITELIST[encoding]):
        err = "Representation unsupported: must be one of {}."
        err = err.format(_DECODE_TYPE_WHITELIST[encoding])
        raise TypeError(err)

    return _CODECS[encoding].decode(target)


def _encode(target, encoding=ENCODING_JSON):
    """Returns an encoded domain model class instance|collection.

    :param object|list target: Domain model class instance|collection.
    :param str encoding: A supported encoding (dict|json).

    :returns: Target encoded accordingly.
    :rtype: unicode|dict|list

    """
    if target is None:
        raise ValueError("Null encoding error")
    if encoding not in _CODECS:
        raise NotImplementedError('Invalid encoding: {}'.format(encoding))

    if isinstance(target, TYPES):
        encoded = _CODECS[encoding].encode(target)
        if isinstance(encoded, basestring):
            encoded = encoded.strip()
        return encoded

    else:
        return [_encode(d, encoding) for d in target]


def from_json(representation):
    return _decode(representation, ENCODING_JSON)

def from_dict(representation):
    return _decode(representation, ENCODING_DICT)

def to_json(instance):
    return _encode(instance, ENCODING_JSON)

def to_dict(instance):
    return _encode(instance, ENCODING_DICT)
