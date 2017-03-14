# -*- coding: utf-8 -*-

"""
.. module:: pyessv.utils.convert.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of library conversion functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import datetime
import json
import re
import types
import uuid

import arrow



# Default character set.
_JSON_CHARSET = "ISO-8859-1"

# Set of data types to be ignored when encoding.
_ENCODE_IGNOREABLE = (int, float, long, type(None), unicode)

# Set of data types to be converted to unicode when encoding.
_ENCODE_UNICODEABLE = (
    basestring,
    arrow.Arrow,
    datetime.datetime,
    uuid.UUID
    )

# ISO date formats.
_ISO_DATE_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]

# Values considered to be abbreviations.
_ABBREVIATIONS = ("id", "uid", "uuid")

# Default string encoding.
_UNICODE = "utf-8"


def str_to_unicode(val):
    """Converts string input to a unicode literal.

    :param object val: arget to be converted to a unicode literal.

    :returns: A unicode literal.
    :rtype: unicode

    """
    if val is None:
        return unicode()
    if isinstance(val, unicode):
        return val

    val = str(val).decode(_UNICODE).strip()
    if not len(val):
        return unicode()

    return unicode(val)


def str_to_camel_case(target, separator='_'):
    """Converts passed name to camel case.

    :param target: A string to be converted.
    :type target: str

    :param separator: A separator used to split target string into constituent parts.
    :type separator: str

    :returns: The target string converted to camel case.
    :rtype: str

    """
    r = ''
    if target is not None and len(target):
        # Convert to pascal case.
        s = str_to_pascal_case(target, separator)

        # Preserve initial separator
        if s[0:len(separator)] == separator:
            r += separator
            s = s[len(separator):]

        # Lower case abbreviations.
        if s.lower() in _ABBREVIATIONS:
            r += s.lower()

        # Lower case initial character.
        elif len(s):
            r += s[0].lower()
            r += s[1:]

    return r


def str_to_underscore_case(target):
    """Helper function to convert a from camel case string to an underscore case string.

    :param target: A string for conversion.
    :type target: str

    :returns: A string converted to underscore case, e.g. account_number.
    :rtype: str

    """
    if target is None or not len(target):
        return ''

    r = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', target)
    r = re.sub('([a-z0-9])([A-Z])', r'\1_\2', r)
    r = r.lower()

    return r


def str_to_pascal_case(target, separator='_'):
    """Converts passed name to pascal case.

    :param target: A string to be converted.
    :type target: str

    :param separator: A separator used to split target string into constituent parts.
    :type separator: str

    :returns: The target string converted to pascal case.
    :rtype: str

    """
    r = ''
    if target is not None and len(target):
        # Preserve initial separator
        if target[0:len(separator)] == separator:
            r = separator

        # Iterate string parts.
        s = target.split(separator)
        for s in s:

            # Upper case abbreviations.
            if s.lower() in _ABBREVIATIONS:
                r += s.upper()

            # Upper case initial character.
            elif (len(s) > 0):
                r += s[0].upper()
                if (len(s) > 1):
                    r += s[1:]

    return r


def _to_encodable(obj, key_formatter=str_to_camel_case):
    """Converts data to encodeable representation.

    """
    if isinstance(obj, _ENCODE_IGNOREABLE):
        return obj

    elif isinstance(obj, _ENCODE_UNICODEABLE):
        return unicode(obj)

    elif isinstance(obj, collections.Mapping):
        return {unicode(key_formatter(k)): _to_encodable(v) for k, v in iter(obj.items())}

    elif isinstance(obj, collections.Iterable):
        return [_to_encodable(i) for i in obj]


class _JSONDecoder(json.JSONDecoder):
    """Extends json decoder so as to handle extended types.

    """
    def __init__(self, key_formatter, to_namedtuple=False):
        """Instance constructor.

        """
        json.JSONDecoder.__init__(self,
                                  encoding=_JSON_CHARSET,
                                  object_hook=self.dict_to_object)
        self.key_formatter = key_formatter
        self.to_namedtuple = to_namedtuple
        self.value_parsers = [
            self.unicode_to_datetime,
            self.unicode_to_uuid
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
            d = dict_keys(d, self.key_formatter)

        # Return dictionary | named tuple.
        return d


    def unicode_to_datetime(self, d, k, v):
        """Converts a unicode value to datetime.

        """
        if isinstance(v, unicode) and len(v):
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


    def unicode_to_uuid(self, d, k, v):
        """Converts a unicode value to uuid.UUID.

        """
        if isinstance(v, unicode) and len(v):
            try:
                v = uuid.UUID(v)
            except ValueError:
                pass
            else:
                d[k] = v
                return True

        return False


def json_to_dict(as_json, key_formatter=None):
    """Converts a json encoded string to a dictionary.

    :param unicode as_json: A json encoded string.
    :param function key_formatter: Dictionary key formatter.

    :returns: A dictionary.
    :rtype: dict

    """
    return _JSONDecoder(key_formatter).decode(as_json)


def dict_to_json(as_dict):
    """Converts a dictionary to json.

    :param dict as_dict: A dictionary.

    :returns: A json encoded text blob.
    :rtype: unicode

    """
    return json.dumps(_to_encodable(as_dict), indent=4, sort_keys=True)


def dict_keys(as_dict, key_formatter=str_to_pascal_case):
    """Converts keys of a dictionary using the passed key formatter.

    :param dict as_dict: A dictionary.
    :param function key_formatter: A dictionary key formatter function pointer.

    :returns: A dictionary with it's keys formatted accordingly.
    :rtype: dict

    """
    if not isinstance(as_dict, dict):
        return as_dict

    result = {}
    for key, val in as_dict.items():
        if isinstance(val, collections.Mapping):
            result[key_formatter(key)] = dict_keys(val, key_formatter)
        elif isinstance(val, types.ListType):
            result[key_formatter(key)] = [dict_keys(i, key_formatter) for i in val]
        else:
            result[key_formatter(key)] = val

    return result
