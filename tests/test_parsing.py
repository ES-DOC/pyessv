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
    def _get_config(typeof, name, synonym):
        result = [
            (typeof, name, name, False, False),
            (typeof, name, name, True, False),
            (typeof, name.upper(), LIB.ParsingError, False, False),
            (typeof, name.upper(), name, True, False),
            (typeof, name.title(), LIB.ParsingError, False, False),
            (typeof, name.title(), name, True, False)
        ]
        if synonym is not None:
            result += [
                (typeof, synonym, name, False, True),
                (typeof, synonym, name, True, True),
                (typeof, synonym.upper(), LIB.ParsingError, False, True),
                (typeof, synonym.upper(), name, True, True),
                (typeof, synonym.title(), LIB.ParsingError, False, True),
                (typeof, synonym.title(), name, True, True)
            ]

        return result


    def _test(cfg):
        """Inner test.

        """
        typeof, name, expected, reformat, parse_synonyms = cfg

        try:
            if typeof == "authority":
                result = LIB.parse(name, \
                                   reformat=reformat, parse_synonyms=parse_synonyms)
            elif typeof == "scope":
                result = LIB.parse(_AUTHORITY, name, \
                                   reformat=reformat, parse_synonyms=parse_synonyms)
            elif typeof == "collection":
                result = LIB.parse(_AUTHORITY, _SCOPE, name, \
                                   reformat=reformat, parse_synonyms=parse_synonyms)
            elif typeof == "term":
                result = LIB.parse(_AUTHORITY, _SCOPE, _COLLECTION, name, \
                                   reformat=reformat, parse_synonyms=parse_synonyms)
        except LIB.ParsingError:
            result = LIB.ParsingError

        assert result == expected, \
               "Parsing error: typeof={}.  name={}.  actual = {}.  expected {}.".format(typeof, name, result, expected)


    for typeof, name, synonym in [
        (LIB.NAME_TYPE_AUTHORITY, _AUTHORITY, None),
        (LIB.NAME_TYPE_SCOPE, _SCOPE, None),
        (LIB.NAME_TYPE_COLLECTION, _COLLECTION, None),
        (LIB.NAME_TYPE_TERM, _TERM, _TERM_SYNONYM),
        ]:
        for cfg in _get_config(typeof, name, synonym):
            desc = "parse {}: {} [reformat={}, parse_synonyms={}]".format(cfg[0], cfg[1], cfg[3], cfg[4])
            tu.init(_test, desc)
            yield _test, cfg
