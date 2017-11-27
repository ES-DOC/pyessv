# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parsers.cordex_dataset_id.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of a CORDEX dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv._factory import create_template_parser
from pyessv._constants import PARSING_STRICTNESS_1



# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = 'cordex.%(product)s.%(domain)s.%(institute)s.%(driving_model)s.%(experiment)s.%(ensemble)s.%(rcm_name)s.%(rcm_version)s.%(time_frequency)s.%(variable)s'

# Test identifier (for reference purpose only).
_TEST_IDENTIFIER = 'cordex.output.AFR-44.MOHC.MOHC-HadGEM2-ES.rcp60.r12i1p1.hadgem3-ra.v1.mon.areacella'

# Template that identifiers must conform to.
_TEMPLATE = 'cordex.{}.{}.{}.{}.{}.{}.{}.{}.{}.{}'

# Collections injected into template.
_COLLECTIONS = (
    'wcrp:cordex:product',
    'wcrp:cordex:domain',
    'wcrp:cordex:institute',
    'wcrp:cordex:driving-model',
    'wcrp:cordex:experiment',
    'wcrp:cordex:ensemble',
    'wcrp:cordex:rcm-name',
    'wcrp:cordex:rcm-version',
    'wcrp:cordex:time-frequency',
    'wcrp:cordex:variable',
    )


def parse(identifier):
    """Parses a CMIP6 dataset identifier.

    """
    parser = create_template_parser(_TEMPLATE, _COLLECTIONS, PARSING_STRICTNESS_1)

    # Strip version suffix.
    if '#' in identifier:
      identifier = identifier.split('#')[0]

    return parser.parse(identifier)
