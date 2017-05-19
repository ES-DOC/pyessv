# -*- coding: utf-8 -*-

"""
.. module:: test_parser_name.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv name parsing tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import nose

import pyessv as LIB
import tests.utils as tu



@nose.with_setup(tu.setup, tu.teardown)
def test_parse_name():
    """Test parsing of names at various levels.

    """
    for typeof, name, synonym in [
        (LIB.NODE_TYPEKEY_AUTHORITY, tu.TEST_AUTHORITY_NAME, tu.TEST_AUTHORITY_SYNONYMS[0]),
        (LIB.NODE_TYPEKEY_SCOPE, tu.TEST_SCOPE_NAME, tu.TEST_SCOPE_SYNONYMS[0]),
        (LIB.NODE_TYPEKEY_COLLECTION, tu.TEST_COLLECTION_NAME, tu.TEST_COLLECTION_SYNONYMS[0]),
        (LIB.NODE_TYPEKEY_TERM, tu.TEST_TERM_NAME, tu.TEST_TERM_SYNONYMS[0]),
        ]:
        for cfg in _get_config(name, synonym):
            desc = 'parse --> {}: {} [strictness={}]'.format(typeof, cfg[0], cfg[2])
            tu.init(_test_parse_names, desc)
            yield _test_parse_names, typeof, cfg


@nose.with_setup(tu.setup, tu.teardown)
def test_parse_namespace():
    """Test parsing of namespsace at various levels.

    """
    for typeof, name, synonym in [
        (LIB.NODE_TYPEKEY_AUTHORITY, tu.TEST_AUTHORITY_NAME, tu.TEST_AUTHORITY_SYNONYMS[0]),
        (LIB.NODE_TYPEKEY_SCOPE, tu.TEST_SCOPE_NAME, tu.TEST_SCOPE_SYNONYMS[0]),
        (LIB.NODE_TYPEKEY_COLLECTION, tu.TEST_COLLECTION_NAME, tu.TEST_COLLECTION_SYNONYMS[0]),
        (LIB.NODE_TYPEKEY_TERM, tu.TEST_TERM_NAME, tu.TEST_TERM_SYNONYMS[0]),
        ]:
        for cfg in _get_config(name, synonym):
            desc = 'parse namespace --> {}: {} [strictness={}]'.format(typeof, cfg[0], cfg[2])
            tu.init(_test_parse_namespace, desc)
            yield _test_parse_namespace, typeof, cfg


def _get_config(name, synonym):
    """Returns node test configuration.

    """
    return [
        (name, name, 0),
        (name.upper(), LIB.ParsingError, 1),
        (name.upper(), LIB.ParsingError, 2),
        (name.upper(), name, 3),
        (synonym, LIB.ParsingError, 0),
        (synonym, LIB.ParsingError, 1),
        (synonym.upper(), LIB.ParsingError, 2),
        (synonym, name, 2)
    ]


def _test_parse_names(typeof, cfg):
    """Asserts name test.

    """
    name, expected, strictness = cfg
    if typeof == LIB.NODE_TYPEKEY_AUTHORITY:
        a = name
        s = c = t = None
    elif typeof == LIB.NODE_TYPEKEY_SCOPE:
        a = tu.TEST_AUTHORITY_NAME
        s = name
        c = t = None
    elif typeof == LIB.NODE_TYPEKEY_COLLECTION:
        a = tu.TEST_AUTHORITY_NAME
        s = tu.TEST_SCOPE_NAME
        c = name
        t = None
    elif typeof == LIB.NODE_TYPEKEY_TERM:
        a = tu.TEST_AUTHORITY_NAME
        s = tu.TEST_SCOPE_NAME
        c = tu.TEST_COLLECTION_NAME
        t = name
    try:
        result = LIB.parse(a, s, c, t, strictness=strictness)
    except LIB.ParsingError:
        result = LIB.ParsingError
    assert result == expected, \
           'Parsing error: node-type={}.  name={}.  actual = {}.  expected {}.'.format(typeof, name, result, expected)


def _test_parse_namespace(typeof, cfg):
    """Asserts namespace test.

    """
    name, expected, strictness = cfg
    if typeof == LIB.NODE_TYPEKEY_AUTHORITY:
        ns = name
    elif typeof == LIB.NODE_TYPEKEY_SCOPE:
        ns = "{}:{}".format(tu.TEST_AUTHORITY_NAME, name)
    elif typeof == LIB.NODE_TYPEKEY_COLLECTION:
        ns = "{}:{}:{}".format(tu.TEST_AUTHORITY_NAME, tu.TEST_SCOPE_NAME, name)
    elif typeof == LIB.NODE_TYPEKEY_TERM:
        ns = "{}:{}:{}:{}".format(tu.TEST_AUTHORITY_NAME, tu.TEST_SCOPE_NAME, tu.TEST_COLLECTION_NAME, name)
    try:
        result = LIB.parse_namespace(ns, strictness)
    except LIB.ParsingError:
        result = LIB.ParsingError
    assert result == expected, \
           'Parsing error: node-type={}.  name={}.  actual = {}.  expected {}.'.format(typeof, name, result, expected)
