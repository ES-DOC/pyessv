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
def test_parse():
    """Test parsing of anmes at various levels.

    """
    def _get_config(typeof, name, synonym=None):
        target = synonym or name
        return [
            (typeof, target, name, False),
            (typeof, target, LIB.ParsingError if synonym else name, True),
            (typeof, target.upper(), name, False),
            (typeof, target.upper(), LIB.ParsingError, True),
            (typeof, target.title(), name, False),
            (typeof, target.title(), LIB.ParsingError, True)
        ]


    def _test_parse_names(cfg):
        """Inner test.

        """
        typeof, name, expected, strict = cfg

        try:
            if typeof == 'authority':
                result = LIB.parse(name, strict=strict)
            elif typeof == 'scope':
                result = LIB.parse(tu.TEST_AUTHORITY_NAME, name, strict=strict)
            elif typeof == 'collection':
                result = LIB.parse(tu.TEST_AUTHORITY_NAME, tu.TEST_SCOPE_NAME, name, strict=strict)
            elif typeof == 'term':
                result = LIB.parse(tu.TEST_AUTHORITY_NAME, tu.TEST_SCOPE_NAME, tu.TEST_COLLECTION_NAME, name, strict=strict)
        except LIB.ParsingError:
            result = LIB.ParsingError

        assert result == expected, \
               'Parsing error: typeof={}.  name={}.  actual = {}.  expected {}.'.format(typeof, name, result, expected)


    def _test_parse_namespace(cfg):
        """Inner test.

        """
        typeof, name, expected, strict = cfg

        if typeof == 'authority':
            parts = []
        elif typeof == 'scope':
            parts = [tu.TEST_AUTHORITY_NAME]
        elif typeof == 'collection':
            parts = [tu.TEST_AUTHORITY_NAME, tu.TEST_SCOPE_NAME]
        elif typeof == 'term':
            parts = [tu.TEST_AUTHORITY_NAME, tu.TEST_SCOPE_NAME, tu.TEST_COLLECTION_NAME]
        parts.append(name)

        try:
            result = LIB.parse_namespace(':'.join(parts), strict)
        except LIB.ParsingError:
            result = LIB.ParsingError

        assert result == expected, \
               'Parsing error: typeof={}.  name={}.  actual = {}.  expected {}.'.format(typeof, name, result, expected)


    for typeof, name, synonym in [
        (LIB.NODE_TYPE_AUTHORITY, tu.TEST_AUTHORITY_NAME, None),
        (LIB.NODE_TYPE_SCOPE, tu.TEST_SCOPE_NAME, None),
        (LIB.NODE_TYPE_COLLECTION, tu.TEST_COLLECTION_NAME, None),
        (LIB.NODE_TYPE_TERM, tu.TEST_TERM_NAME, tu.TEST_TERM_SYNONYMS[0]),
        ]:
        config = _get_config(typeof, name)
        if synonym:
            config += _get_config(typeof, name, synonym)

        for cfg in config:
            desc = 'parse --> {}: {} [strict={}]'.format(cfg[0], cfg[1], cfg[3])
            tu.init(_test_parse_names, desc)
            yield _test_parse_names, cfg


    for typeof, name, synonym in [
        (LIB.NODE_TYPE_AUTHORITY, tu.TEST_AUTHORITY_NAME, None),
        (LIB.NODE_TYPE_SCOPE, tu.TEST_SCOPE_NAME, None),
        (LIB.NODE_TYPE_COLLECTION, tu.TEST_COLLECTION_NAME, None),
        (LIB.NODE_TYPE_TERM, tu.TEST_TERM_NAME, tu.TEST_TERM_SYNONYMS[0]),
        ]:
        config = _get_config(typeof, name)
        if synonym:
            config += _get_config(typeof, name, synonym)

        for cfg in config:
            desc = 'parse namespace --> {}: {} [strict={}]'.format(cfg[0], cfg[1], cfg[3])
            tu.init(_test_parse_namespace, desc)
            yield _test_parse_namespace, cfg
