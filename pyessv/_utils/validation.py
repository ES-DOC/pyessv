# -*- coding: utf-8 -*-

"""
.. module:: pyessv.utils.validation.py
   :copyright: Copyright "December 01, 2016', IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validation utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import inspect
import re
import uuid

from pyessv._constants import PARSING_NODE_FIELDS
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
from pyessv._utils.compat import urlparse


def assert_iterable(val, modifier, typeof=list):
    """Asserts an iterable value.

    """
    assert isinstance(val, typeof)
    for i in val:
        if inspect.isfunction(modifier):
            modifier(i)
        else:
            assert isinstance(i, modifier)


def assert_regex(val, reg_ex):
    """Asserts a string value.

    """
    assert re.compile(reg_ex).match(val) is not None


def assert_string(val):
    """Asserts a string value.

    """
    assert isinstance(val, basestring)
    assert len(val.strip()) > 0


def assert_url(val):
    """Asserts a url value.

    """
    assert_string(val)
    url = urlparse(val)
    assert url.netloc and url.scheme


def assert_namespace(identifier, min_length=1, max_length=4):
    """Asserts a namespace.

    """
    assert_string(identifier)
    parts = str(identifier).split(':')
    assert len(parts) >= min_length and len(parts) <= max_length
    for part in parts:
        assert_string(part)


def assert_pattern(val, info):
    from pyessv._loader import load

    pattern = info[0]
    collections = []
    for defn in info[1:]:
        parts = defn.split(':')
        field = parts[-1] if parts[-1] in PARSING_NODE_FIELDS else 'canonical_name'
        collection = load(':'.join(parts[0:3]))
        collections.append((collection, field))
