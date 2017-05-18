# -*- coding: utf-8 -*-

"""
.. module:: test_utils_factory.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Exposes test factory utility functions.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import random
import uuid

import arrow

from pyessv._utils.compat import str



def get_boolean():
    """Returns a random boolean for testing purposes.

    """
    return True


def get_date(value=None):
    """Returns a random integer for testing purposes.

    """
    if value:
        if len(value) == 4:
            return arrow.get(value, 'YYYY').datetime
        else:
            return arrow.get(value).datetime
    else:
        return arrow.utcnow().datetime


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
    result = str(uuid.uuid1())[:length]
    while existing == result:
        result = str(uuid.uuid1())[:length]
    return result


def get_uuid():
    """Returns a uuid for testing purposes.

    """
    return string(uuid.uuid1())
