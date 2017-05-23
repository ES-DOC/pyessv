# -*- coding: utf-8 -*-

"""
.. module:: test_parser_template.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv template parsing tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import nose

import pyessv as LIB

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

# Map of templates to parsers.
_PARSERS = {
    _TEMPLATE_1: None,
    _TEMPLATE_2: None,
    _TEMPLATE_3: None
}

# Map of expression templates to valid expressions.
_VALID = {
    _TEMPLATE_1: 'ciclad/cmip6/ipsl/dcpp/hadgem3-gc31-ll/dcppc-atl-spg/afilename.nc1',
    _TEMPLATE_2: 'ipsl/dcpp/hadgem3-gc31-ll/dcppc-atl-spg/afilename.nc2',
    _TEMPLATE_3: 'ciclad/cmip6/ipsl/dcpp/hadgem3-gc31-ll/dcppc-atl-spg'
}

# Map of expression templates to invalid expressions.
_INVALID = {
    _TEMPLATE_1: 'ciclad/cmip6/WWW/XXX/YYY/ZZZ/afilename.nc1',
    _TEMPLATE_2: 'WWW/XXX/YYY/ZZZ/afilename.nc2',
    _TEMPLATE_3: 'ciclad/cmip6/WWW/XXX/YYY/ZZZ'
}


def test_expressions():
    """pyessv-tests: expression: valid.

    """
    def _do_positive_test(template, parser):
        parser.parse(_VALID[template])

    @nose.tools.raises(ValueError)
    def _do_negative_test(template, parser):
        parser.parse(_INVALID[template])

    _setup()
    for template in _TEMPLATES:
        tu.init(_do_positive_test, 'parse expression :: {} --> positive'.format(template))
        yield _do_positive_test, template, _PARSERS[template]
        tu.init(_do_negative_test, 'parse expression :: {} --> negative'.format(template))
        yield _do_negative_test, template, _PARSERS[template]


def _setup():
    """Unit test setup.

    """
    # Load vocabs.
    LIB.init()

    # Set collections.
    collections = (
        LIB.load('wcrp:cmip6:institution-id'),
        LIB.load('wcrp:cmip6:activity-id'),
        LIB.load('wcrp:cmip6:source-id'),
        LIB.load('wcrp:cmip6:experiment-id')
        )

    # Set parsers.
    for template in _TEMPLATES:
        _PARSERS[template] = LIB.create_template_parser(template, collections)
