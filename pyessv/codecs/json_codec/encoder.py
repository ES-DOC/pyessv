"""
.. module:: json.encoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes a term to JSON.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import datetime

from pyessv.codecs.dict_codec import encoder as dict_encoder
from pyessv.utils import compat
from pyessv.utils import convert



# Set of data types to be ignored when encoding.
_ENCODE_IGNOREABLE = tuple(list(compat.numeric_types) + [type(None), compat.str])

def encode(instance):
    """Encodes an instance of a domain model class as a JSON text blob.

    :param pyessv.Node instance: A domain model class instance to be encoded as a JSON text blob.

    :returns: Instance encoded as a JSON text blob.
    :rtype: str

    """
    # Convert to dictionary.
    obj = dict_encoder.encode(instance)

    # Return JSON.
    as_json = compat.str(dict_to_json(obj))

    return as_json


def dict_to_json(obj):
    """Converts a dictionary to json.

    :param dict obj: A dictionary.

    :returns: A json encoded text blob.
    :rtype: str

    """
    return compat.json.dumps(_to_encodable(obj), indent=4, sort_keys=True)


def _to_encodable(obj, key_formatter=lambda k: k):
    """Converts data to encodeable representation.

    """
    if isinstance(obj, _ENCODE_IGNOREABLE):
        return obj

    elif isinstance(obj, compat.basestring):
        return compat.str(obj)

    elif isinstance(obj, datetime.datetime):
        return '{}+00:00'.format(compat.str(obj)[:19])

    elif isinstance(obj, compat.Mapping):
        return { compat.str(key_formatter(k)): _to_encodable(v) for k, v in iter(obj.items()) }

    elif isinstance(obj, compat.Iterable):
        return [_to_encodable(i) for i in obj]
