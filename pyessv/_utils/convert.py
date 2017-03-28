# -*- coding: utf-8 -*-

"""
.. module:: pyessv._utils.convert.py
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

from pyessv._utils.compat import numeric_types
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str


# Values considered to be abbreviations.
_ABBREVIATIONS = ('id', 'uid', 'uuid')

# Default string encoding.
_UTF8 = 'utf-8'


def str_to_unicode(val):
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
        elif isinstance(val, list):
            result[key_formatter(key)] = [dict_keys(i, key_formatter) for i in val]
        else:
            result[key_formatter(key)] = val

    return result
