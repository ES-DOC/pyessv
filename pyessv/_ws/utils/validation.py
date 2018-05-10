# -*- coding: utf-8 -*-

"""
.. module:: utils.validation.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Variable validation utilities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import uuid

import arrow
import requests
import pyessv

from pyessv._ws.utils import config
from pyessv._ws.utils import exceptions



def validate(validator):
    """Validation function decorator.

    """
    def decorate(func):
        """The decorator."""
        def wrapper(*args, **kwargs):
            """The wrapper."""
            validator(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorate


def _raise_value_error(val, var, var_type):
    """Raises a generic value error.

    """
    raise ValueError('{0} [{1}] is an invalid {2}'.format(var, val, var_type))


def validate_bool(val, var):
    """Validates a boolean.

    """
    if val is None:
        raise ValueError('{0} is undefined bool'.format(var))

    try:
        bool(val)
    except ValueError:
        _raise_value_error(val, var, bool)


def validate_enum(enum_values, val, var):
    """Validates an enumerable member.

    """
    if val not in enum_values:
        _raise_value_error(val, var, 'enum-member')


def validate_pyessv_enum(collection_id, val, var):
    """Validates an enumerable member.

    """
    namespace = '{}:{}'.format(collection_id, val)
    try:
        pyessv.parse(namespace)
    except pyessv.ParsingError:
        _raise_value_error(val, var, 'enum-member')


def validate_int(val, var):
    """Validates an integer.

    """
    if val is None:
        raise ValueError('{0} is undefined'.format(var))

    try:
        int(val)
    except ValueError:
        _raise_value_error(val, var, int)


def validate_float(val, var):
    """Validates a flaot.

    """
    if val is None:
        raise ValueError('{0} is undefined'.format(var))

    try:
        float(val)
    except ValueError:
        _raise_value_error(val, var, float)


def validate_date(val, var, date_format=None):
    """Validates a date.

    """
    if val is None:
        raise ValueError('{0} is undefined date'.format(var))

    try:
        if date_format is not None:
            arrow.get(val, date_format)
        else:
            arrow.get(val)
    except arrow.parser.ParserError:
        _raise_value_error(val, var, 'date')


def validate_str(val, var):
    """Validates a string.

    """
    if val is None:
        raise ValueError('{0} is undefined string'.format(var))

    try:
        val = str(val)
    except ValueError:
        _raise_value_error(val, var, str)

    if not len(val):
        raise ValueError('{0} is empty string'.format(var))


def validate_uid(val, var):
    """Validaes a universally unique identifier.

    """
    if not isinstance(val, uuid.UUID):
        try:
            uuid.UUID(val)
        except ValueError:
            _raise_value_error(val, var, uuid.UUID)


def validate_unicode(val, var):
    """Validates a unicode.

    """
    if val is None:
        raise ValueError('{0} is undefined unicode'.format(var))

    try:
        val = unicode(val)
    except ValueError:
        _raise_value_error(val, var, unicode)

    if not len(val):
        raise ValueError('{0} is empty unicode'.format(var))


def validate_iterable(val, var):
    """Validates an iterable.

    """
    if val is None:
        raise ValueError('{0} is undefined iterable'.format(var))

    try:
        iter(val)
    except TypeError:
        _raise_value_error(val, var, iter)


def validate_url(url):
    """Validates that a URL will not return a 404.

    :param str url: The url to validate.

    """
    if url in (None, ''):
        return

    if url.startswith('http'):
        if not config.validate_issue_urls:
            return
        response = requests.head(url)
        if response.status_code in [requests.codes.OK, 302]:
            return
        response = requests.get(url)
        if response.ok:
            return

    raise exceptions.InvalidURLError(url)
