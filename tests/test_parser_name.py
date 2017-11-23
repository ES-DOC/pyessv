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



# Test inputs.
_INPUTS = (
    (LIB.NODE_TYPEKEY_AUTHORITY, tu.AUTHORITY_NAME, tu.AUTHORITY_SYNONYMS, None),
    (LIB.NODE_TYPEKEY_SCOPE, tu.SCOPE_NAME, tu.SCOPE_SYNONYMS, None),
    (LIB.NODE_TYPEKEY_COLLECTION, tu.COLLECTION_01_NAME, tu.COLLECTION_01_SYNONYMS, None),
    (LIB.NODE_TYPEKEY_COLLECTION, tu.COLLECTION_02_NAME, tu.COLLECTION_02_SYNONYMS, None),
    (LIB.NODE_TYPEKEY_COLLECTION, tu.COLLECTION_03_NAME, tu.COLLECTION_03_SYNONYMS, None),
    (LIB.NODE_TYPEKEY_TERM, tu.TERM_01_NAME, tu.TERM_01_SYNONYMS, tu.COLLECTION_01_NAME),
    (LIB.NODE_TYPEKEY_TERM, tu.TERM_02_NAME, tu.TERM_02_SYNONYMS, tu.COLLECTION_02_NAME),
    # (LIB.NODE_TYPEKEY_TERM, tu.TERM_03_NAME, tu.TERM_03_SYNONYMS, tu.COLLECTION_03_NAME),
    )


@nose.with_setup(tu.setup, tu.teardown)
def test_parse_name():
    """Test parsing of names at various levels.

    """
    for typekey, canonical_name, synonyms, parent in _INPUTS:
        for synonym in synonyms:
            for name, expected, strictness in _get_config(canonical_name, synonym):
                for func in (_test_parse_name, ):
                    target = func.__name__.split('_')[-1]
                    desc = 'parse --> {}: {} [strictness={}, target={}]'.format(
                        typekey, name, strictness, target
                        )
                    tu.init(func, desc)
                    yield func, typekey, name, expected, strictness, parent


def _test_parse_name(typekey, name, expected, strictness, parent):
    """Asserts name test.

    """
    s = c = t = None
    if typekey == LIB.NODE_TYPEKEY_AUTHORITY:
        a = name
    elif typekey == LIB.NODE_TYPEKEY_SCOPE:
        a = tu.AUTHORITY_NAME
        s = name
    elif typekey == LIB.NODE_TYPEKEY_COLLECTION:
        a = tu.AUTHORITY_NAME
        s = tu.SCOPE_NAME
        c = name
    elif typekey == LIB.NODE_TYPEKEY_TERM:
        a = tu.AUTHORITY_NAME
        s = tu.SCOPE_NAME
        c = parent
        t = name

    try:
        result = LIB.parse(a, s, c, t, strictness=strictness)
    except LIB.ParsingError:
        result = LIB.ParsingError

    assert result == expected, \
           'Name parsing error: node-type={}.  name={}.  actual = {}.  expected {}.'.format(typekey, name, result, expected)


def _test_parse_namespace(typekey, name, expected, strictness, parent):
    """Asserts namespace test.

    """
    if typekey == LIB.NODE_TYPEKEY_AUTHORITY:
        ns = name
    elif typekey == LIB.NODE_TYPEKEY_SCOPE:
        ns = "{}:{}".format(tu.AUTHORITY_NAME, name)
    elif typekey == LIB.NODE_TYPEKEY_COLLECTION:
        ns = "{}:{}:{}".format(tu.AUTHORITY_NAME, tu.SCOPE_NAME, name)
    elif typekey == LIB.NODE_TYPEKEY_TERM:
        ns = "{}:{}:{}:{}".format(tu.AUTHORITY_NAME, tu.SCOPE_NAME, parent, name)

    try:
        result = LIB.parse_namespace(ns, strictness)
    except LIB.ParsingError:
        result = LIB.ParsingError

    assert result == expected, \
           'Namespace parsing error: node-type={}.  name={}.  actual = {}.  expected {}.'.format(typekey, name, result, expected)


def _get_config(canonical_name, synonym):
    """Returns node test configuration.

    """
    return [
        (canonical_name, canonical_name, 0),
        # (canonical_name.upper(), LIB.ParsingError, 1),
        # (canonical_name.upper(), LIB.ParsingError, 2),
        # (canonical_name.upper(), canonical_name, 3),
        # (synonym, LIB.ParsingError, 0),
        # (synonym, LIB.ParsingError, 1),
        # (synonym.upper(), LIB.ParsingError, 2),
        # (synonym, canonical_name, 2)
    ]

