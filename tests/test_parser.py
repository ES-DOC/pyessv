# -*- coding: utf-8 -*-

"""
.. module:: test_parsing.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv parsing tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import nose

import pyessv as LIB
import tests.utils as tu


# Test authority.
_AUTHORITY = 'test-authority'

# Test scope.
_SCOPE = 'test-scope'

# Test collection.
_COLLECTION = 'test-collection'

# Test term.
_TERM = 'test-term'

# Test term.
_TERM_SYNONYM = 'test-term-synonym-1'


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
            if typeof == "authority":
                result = LIB.parse(name, strict=strict)
            elif typeof == "scope":
                result = LIB.parse(_AUTHORITY, name, strict=strict)
            elif typeof == "collection":
                result = LIB.parse(_AUTHORITY, _SCOPE, name, strict=strict)
            elif typeof == "term":
                result = LIB.parse(_AUTHORITY, _SCOPE, _COLLECTION, name, strict=strict)
        except LIB.ParsingError:
            result = LIB.ParsingError

        assert result == expected, \
               "Parsing error: typeof={}.  name={}.  actual = {}.  expected {}.".format(typeof, name, result, expected)


    def _test_parse_namespace(cfg):
        """Inner test.

        """
        typeof, name, expected, strict = cfg

        if typeof == "authority":
            parts = []
        elif typeof == "scope":
            parts = [_AUTHORITY]
        elif typeof == "collection":
            parts = [_AUTHORITY, _SCOPE]
        elif typeof == "term":
            parts = [_AUTHORITY, _SCOPE, _COLLECTION]
        parts.append(name)

        try:
            result = LIB.parse_namespace(":".join(parts), strict)
        except LIB.ParsingError:
            result = LIB.ParsingError

        assert result == expected, \
               "Parsing error: typeof={}.  name={}.  actual = {}.  expected {}.".format(typeof, name, result, expected)


    for typeof, name, synonym in [
        (LIB.ENTITY_TYPE_AUTHORITY, _AUTHORITY, None),
        (LIB.ENTITY_TYPE_SCOPE, _SCOPE, None),
        (LIB.ENTITY_TYPE_COLLECTION, _COLLECTION, None),
        (LIB.ENTITY_TYPE_TERM, _TERM, _TERM_SYNONYM),
        ]:
        config = _get_config(typeof, name)
        if synonym:
            config += _get_config(typeof, name, synonym)

        for cfg in config:
            desc = "parse --> {}: {} [strict={}]".format(cfg[0], cfg[1], cfg[3])
            tu.init(_test_parse_names, desc)
            yield _test_parse_names, cfg

            desc = "parse namespace --> {}: {} [strict={}]".format(cfg[0], cfg[1], cfg[3])
            tu.init(_test_parse_namespace, desc)
            yield _test_parse_namespace, cfg
