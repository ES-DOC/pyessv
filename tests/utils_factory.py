# -*- coding: utf-8 -*-

"""
.. module:: testutils_factory.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Exposes test factory utility functions.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import datetime as dt
import random
import uuid

from pyessv.utils.compat import str



def get_boolean():
    """Returns a random boolean for testing purposes.

    """
    return True


def get_date(value=None):
    """Returns a random date for testing purposes.

    """
    if not value:
        return dt.datetime.utcnow()

    # Supported parsing formats.
    formats = [
        '%Y',
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S'
    ]

    for format in formats:
        try:
            return dt.datetime.strptime(value, format)
        except ValueError:
            pass

    raise ValueError('Could not parse value to a date')


def get_int(lower=0, upper=9999999, existing=None):
    """Returns a random integer for testing purposes.

    """
    result = random.randint(lower, upper)
    while existing == result:
        result = random.randint(lower, upper)
    return result


def get_float():
    """Returns a random float for testing purposes.

    """
    return random.random()


def get_string(length=31, existing=None):
    """Returns a random string for testing purposes.

    """
    result = compat.str(uuid.uuid1())[:length]
    while existing == result:
        result = compat.str(uuid.uuid1())[:length]
    return result


def get_uuid():
    """Returns a uuid for testing purposes.

    """
    return compat.str(uuid.uuid1())
