# -*- coding: utf-8 -*-

"""
.. module:: pyessv._codecs.json_codec.decoder.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Decodes a term from a JSON text blob.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import datetime
import uuid

from pyessv._codecs.dict_codec import decoder as dict_decoder
from pyessv._utils import convert
from pyessv._utils.compat import json
from pyessv._utils.compat import str



# ISO date formats.
_ISO_DATE_FORMATS = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']

# Default string encoding.
_UTF8 = 'utf-8'



def decode(as_json):
    """Decodes a document from a UTF-8 encoded json text blob.

    :param str as_xml: Term JSON representation.

    :returns: A term instance.
    :rtype: pyessv.Term

    """
    # Decode raw text blob.
    as_json = _decode_blob(as_json)

    # Convert to dictionary.
    as_dict = _JSONDecoder().decode(as_json)

    # Decode from dictionary.
    return dict_decoder.decode(as_dict)


class _JSONDecoder(json.JSONDecoder):
    """Extends json decoder so as to handle extended types.

    """
    def __init__(self, key_formatter=lambda k:k, to_namedtuple=False):
        """Instance constructor.

        """
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)
        self.key_formatter = key_formatter
        self.to_namedtuple = to_namedtuple
        self.value_parsers = [
            self._to_datetime,
            self._to_uuid
            ]


    def dict_to_object(self, d):
        """Converts a dictionary to an object.

        """
        # Parse values.
        for k, v in d.items():
            for parser in self.value_parsers:
                if parser(d, k, v):
                    break

        # Format keys.
        if self.key_formatter is not None:
            d = convert.dict_keys(d, self.key_formatter)

        # Return dictionary | named tuple.
        return d


    def _to_datetime(self, d, k, v):
        """Converts a value to datetime.

        """
        if isinstance(v, str) and len(v):
            try:
                float(v)
            except ValueError:
                for format in _ISO_DATE_FORMATS:
                    try:
                        v = datetime.datetime.strptime(v, format)
                    except (ValueError, TypeError):
                        pass
                    else:
                        d[k] = v
                        return True

        return False


    def _to_uuid(self, d, k, v):
        """Converts a value to uuid.UUID.

        """
        if isinstance(v, basestring) and len(v):
            try:
                v = uuid.UUID(v)
            except ValueError:
                pass
            else:
                d[k] = v
                return True

        return False


def _decode_blob(val):
    """Converts input to a string literal.

    :param object val: value to be converted to a string literal.

    :returns: A string literal.
    :rtype: str

    """
    if val is None:
        return str()
    if isinstance(val, str):
        return val

    val = str(val).decode(_UTF8).strip()
    if not len(val):
        return str()

    return str(val)
