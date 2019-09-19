# -*- coding: utf-8 -*-

"""
.. module:: test_parser_name.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv name parsing tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pytest

import pyessv as LIB
import tests.utils as tu


# Module level fixture setup.
setup_module = tu.setup

# Module level fixture teardown.
teardown_module = tu.teardown


# Test inputs.
_INPUTS = (
    (LIB.NODE_TYPEKEY_AUTHORITY, tu.AUTHORITY_NAME, tu.AUTHORITY_ALTERNATIVE_NAMES, None),
    (LIB.NODE_TYPEKEY_SCOPE, tu.SCOPE_NAME, tu.SCOPE_ALTERNATIVE_NAMES, None),
    (LIB.NODE_TYPEKEY_COLLECTION, tu.COLLECTION_01_NAME, tu.COLLECTION_01_ALTERNATIVE_NAMES, None),
    (LIB.NODE_TYPEKEY_COLLECTION, tu.COLLECTION_02_NAME, tu.COLLECTION_02_ALTERNATIVE_NAMES, None),
    (LIB.NODE_TYPEKEY_COLLECTION, tu.COLLECTION_03_NAME, tu.COLLECTION_03_ALTERNATIVE_NAMES, None),
    (LIB.NODE_TYPEKEY_TERM, tu.TERM_01_NAME, tu.TERM_01_ALTERNATIVE_NAMES, tu.COLLECTION_01_NAME),
    (LIB.NODE_TYPEKEY_TERM, tu.TERM_02_NAME, tu.TERM_02_ALTERNATIVE_NAMES, tu.COLLECTION_02_NAME),
    (LIB.NODE_TYPEKEY_TERM, tu.TERM_03_NAME, tu.TERM_03_ALTERNATIVE_NAMES, tu.COLLECTION_03_NAME)
    )


def _yield_parameterizations():
    """Test parameterizations.

    """    
    for typekey, canonical_name, alternative_names, parent in _INPUTS:
        for alternative_name in alternative_names:
            for name, expected, strictness in [
                (canonical_name, canonical_name, 0),
                (canonical_name.upper(), LIB.ParsingError, 1),
                (canonical_name.upper(), LIB.ParsingError, 2),
                # (canonical_name.upper(), canonical_name, 3),
                (alternative_name, LIB.ParsingError, 0),
                (alternative_name, LIB.ParsingError, 1),
                (alternative_name.upper(), LIB.ParsingError, 2),
                # (alternative_name, canonical_name, 2)
            ]:
                yield typekey, name, expected, strictness, parent


@pytest.mark.parametrize("typekey, name, expected, strictness, parent", _yield_parameterizations())
def test_parse_name(typekey, name, expected, strictness, parent):
    """Test parsing of names at various levels.

    """
    if typekey == LIB.NODE_TYPEKEY_AUTHORITY:
        namespace = name
    elif typekey == LIB.NODE_TYPEKEY_SCOPE:
        namespace = '{}:{}'.format(tu.AUTHORITY_NAME, name)
    elif typekey == LIB.NODE_TYPEKEY_COLLECTION:
        namespace = '{}:{}:{}'.format(tu.AUTHORITY_NAME, tu.SCOPE_NAME, name)
    elif typekey == LIB.NODE_TYPEKEY_TERM:
        namespace = '{}:{}:{}:{}'.format(tu.AUTHORITY_NAME, tu.SCOPE_NAME, parent, name)

    try:
        result = LIB.parse(namespace, strictness=strictness)
    except LIB.ParsingError:
        result = LIB.ParsingError

    assert result == expected, \
           'Name parsing error: node-type={}.  name={}.  actual = {}.  expected {}.'.format(typekey, name, result, expected)
