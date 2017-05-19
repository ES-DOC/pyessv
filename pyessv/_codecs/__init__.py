# -*- coding: utf-8 -*-

"""
.. module:: pyessv._codecs.__init__.py
   :copyright: Copyright "Sep 4, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates transformations of terms from one format to another.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._codecs import dict_codec
from pyessv._codecs import json_codec
from pyessv._constants import ENCODING_DICT
from pyessv._constants import ENCODING_JSON
from pyessv._model import Node
from pyessv._utils.compat import basestring



# Codecs mapped by encoding.
_CODECS = {
	ENCODING_DICT: dict_codec,
	ENCODING_JSON: json_codec
    }

# Map of encodings to allowed input types when decoding.
_DECODE_TYPE_WHITELIST = {
    ENCODING_DICT : (dict, ),
    ENCODING_JSON : (basestring, )
    }


def decode(representation, encoding=ENCODING_JSON):
    """Returns a decoded domain model class instance.

    :param str|dict representation: A domain model class instance representation.
    :param str encoding: A supported encoding (dict|json).

    :returns: A domain model class instance.
    :rtype: object

    """
    if representation is None:
        raise ValueError('Cannot decode a null pointer.')
    if not encoding in _CODECS:
        raise NotImplementedError('Unsupported term encoding :: {0}.'.format(encoding))
    if not isinstance(representation, _DECODE_TYPE_WHITELIST[encoding]):
        err = 'Representation unsupported: must be one of {}.'
        err = err.format(_DECODE_TYPE_WHITELIST[encoding])
        raise TypeError(err)

    return _CODECS[encoding].decode(representation)


def encode(target, encoding=ENCODING_JSON):
    """Returns an encoded domain model class instance|collection.

    :param object|list target: Domain model class instance|collection.
    :param str encoding: A supported encoding (dict|json).

    :returns: Target encoded accordingly.
    :rtype: str|dict|list

    """
    if target is None:
        raise ValueError('Null encoding error')
    if encoding not in _CODECS:
        raise NotImplementedError('Invalid encoding: {}'.format(encoding))

    if isinstance(target, Node):
        encoded = _CODECS[encoding].encode(target)
        if isinstance(encoded, basestring):
            encoded = encoded.strip()
        return encoded
