"""
.. module:: pyessv.codecs.json_codec.decoder.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Decodes a term from a JSON text blob.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import datetime

from pyessv.codecs.dict_codec import decoder as dict_decoder
from pyessv.utils import compat
from pyessv.utils import convert



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


class _JSONDecoder(compat.json.JSONDecoder):
    """Extends json decoder so as to handle extended types.

    """
    def __init__(self, key_formatter=lambda k:k, to_namedtuple=False):
        """Instance constructor.

        """
        compat.json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)
        self.key_formatter = key_formatter
        self.to_namedtuple = to_namedtuple
        self.valueparsers = [self._to_datetime]


    def dict_to_object(self, d):
        """Converts a dictionary to an object.

        """
        # Parse values.
        for k, v in d.items():
            for parser in self.valueparsers:
                if parser(d, k, v) == True:
                    break

        # Format keys.
        if self.key_formatter is not None:
            d = convert.dict_keys(d, self.key_formatter)

        # Return dictionary | named tuple.
        return d


    def _to_datetime(self, d, k, v):
        """Converts a value to datetime.

        """
        if isinstance(v, compat.str) and len(v):
            try:
                float(v)
            except (TypeError, ValueError):
                try:
                    as_datetime = compat.to_datetime(v)
                except (ValueError, TypeError):
                    pass
                else:
                    if as_datetime is not None:
                        d[k] = as_datetime
                        return True

        return False


def _decode_blob(val):
    """Converts input to a string literal.

    :param object val: value to be converted to a string literal.

    :returns: A string literal.
    :rtype: str

    """
    if val is None:
        return compat.str()
    if isinstance(val, compat.str):
        return val

    val = compat.str(val).decode(_UTF8).strip()
    if not len(val):
        return compat.str()

    return compat.str(val)
