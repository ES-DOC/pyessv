# -*- coding: utf-8 -*-

"""
.. module:: test_parsing.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv parsing tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pyessv as LIB
import tests.utils as tu


# Test authority.
_AUTHORITY = 'wcrp'

# Test scope.
_SCOPE = 'cmip6'

# Test collection.
_COLLECTION = 'realm'

# Test term.
_TERM = 'ocnbgchem'

# Test term.
_TERM_SYNONYM = 'ocean-bgc'


def test_parse():
    """Test parsing of anmes at various levels.

    """
    def _get_config(typeof, name):
        return [
            (typeof, name, name, False),
            (typeof, name, name, True),
            (typeof, name.upper(), name, False),
            (typeof, name.upper(), LIB.ParsingError, True),
            (typeof, name.title(), name, False),
            (typeof, name.title(), LIB.ParsingError, True)
        ]


    def _test(cfg):
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


    for typeof, name, synonym in [
        (LIB.ENTITY_TYPE_AUTHORITY, _AUTHORITY, None),
        (LIB.ENTITY_TYPE_SCOPE, _SCOPE, None),
        (LIB.ENTITY_TYPE_COLLECTION, _COLLECTION, None),
        # (LIB.ENTITY_TYPE_TERM, _TERM, _TERM_SYNONYM),
        ]:

        config = _get_config(typeof, name)
        if synonym:
            config += _get_config(typeof, synonym)

        for cfg in config:
            desc = "parse {}: {} [strict={}]".format(cfg[0], cfg[1], cfg[3])
            tu.init(_test, desc)
            yield _test, cfg
