# -*- coding: utf-8 -*-

"""
.. module:: test_parser_template.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv template parsing tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pytest

import pyessv

import tests.utils as tu


# Templates.
_TEMPLATE_1 = 'ciclad/cmip6/{}/{}/{}/{}/afilename.nc1'
_TEMPLATE_2 = '{}/{}/{}/{}/afilename.nc2'
_TEMPLATE_3 = 'ciclad/cmip6/{}/{}/{}/{}'
_TEMPLATES = (
    _TEMPLATE_1,
    _TEMPLATE_2,
    _TEMPLATE_3
    )

# Valid expressions.
_VALID = (
    (_TEMPLATE_1, 'ciclad/cmip6/ipsl/fafmip/ipsl-cm6a-lr/amip/afilename.nc1'),
    (_TEMPLATE_2, 'ipsl/fafmip/ipsl-cm6a-lr/amip/afilename.nc2'),
    (_TEMPLATE_3, 'ciclad/cmip6/ipsl/fafmip/ipsl-cm6a-lr/amip')
)

# Invalid expressions.
_INVALID = (
    (_TEMPLATE_1, 'ciclad/cmip6/WWW/XXX/YYY/ZZZ/afilename.nc1'),
    (_TEMPLATE_2, 'WWW/XXX/YYY/ZZZ/afilename.nc2'),
    (_TEMPLATE_3, 'ciclad/cmip6/WWW/XXX/YYY/ZZZ'),
)

# Map of templates to parsers.
_PARSERS = {
    _TEMPLATE_1: None,
    _TEMPLATE_2: None,
    _TEMPLATE_3: None
}


def setup_module():
    """Unit test setup.

    """
    # Set collections.
    collections = (
        'wcrp:cmip6:institution-id',
        'wcrp:cmip6:activity-id',
        'wcrp:cmip6:source-id',
        'wcrp:cmip6:experiment-id'
        )

    # Set parsers.
    for template in _TEMPLATES:
        _PARSERS[template] = pyessv.create_template_parser(template, collections, seperator='/')


@pytest.mark.parametrize("template, expression", _VALID)
def test_expressions_01(template, expression):
    """pyessv-tests: expression: valid.

    """
    parser = _PARSERS[template]
    parser.parse(expression)


@pytest.mark.parametrize("template, expression", _INVALID)
def test_expressions_02(template, expression):
    """pyessv-tests: expression: invalid.

    """
    with pytest.raises(ValueError):
        parser = _PARSERS[template]
        parser.parse(expression)

