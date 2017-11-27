# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parsers.cmip6_dataset_id.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of a CMIP5 dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv._factory import create_template_parser
from pyessv._constants import PARSING_STRICTNESS_1



# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = 'cmip5.%(product)s.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s.%(realm)s.%(cmor_table)s.%(ensemble)s'

# Test identifier (for reference purpose only).
_TEST_IDENTIFIER = 'cmip5.output2.IPSL.IPSL-CM5A-LR.historicalMisc.mon.ocean.Omon.r2i1p1.v20150504'

# Template that identifiers must conform to.
_TEMPLATE = 'cmip5.{}.{}.{}.{}.{}.{}.{}.{}'

# Collections injected into template.
_COLLECTIONS = (
    'wcrp:cmip5:product',
    'wcrp:cmip5:institute',
    'wcrp:cmip5:model',
    'wcrp:cmip5:experiment',
    'wcrp:cmip5:time-frequency',
    'wcrp:cmip5:realm',
    'wcrp:cmip5:cmor-table',
    'wcrp:cmip5:ensemble'
    )


def parse(identifier):
    """Parses a CMIP6 dataset identifier.

    """
    parser = create_template_parser(_TEMPLATE, _COLLECTIONS, PARSING_STRICTNESS_1)

    # Strip version suffix.
    if '#' in identifier:
      identifier = identifier.split('#')[0]

    return parser.parse(identifier.split('#')[0])
