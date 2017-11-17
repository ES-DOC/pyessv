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



# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = 'cordex.%(product)s.%(domain)s.%(institute)s.%(driving_model)s.%(experiment)s.%(ensemble)s.%(rcm_name)s.%(rcm_version)s.%(time_frequency)s.%(variable)s'

# Test identifier (for reference purpose only).
_TEST_IDENTIFIER = 'cordex.output.AFR-44.MOHC.MOHC-HadGEM2-ES.rcp60.r12i1p1.hadgem3-ra.v1.mon.areacella'

# Template that identifiers must conform to.
_TEMPLATE = 'cordex.{}.{}.{}.{}.{}.{}.{}.{}.{}.{}'

# Collections injected into template.
_COLLECTIONS = (
    'esgf-publisher:cordex:product',
    'esgf-publisher:cordex:domain',
    'esgf-publisher:cordex:institute',
    'esgf-publisher:cordex:driving-model',
    'esgf-publisher:cordex:experiment',
    'esgf-publisher:cordex:ensemble',
    'esgf-publisher:cordex:rcm-name',
    'esgf-publisher:cordex:rcm-version',
    'esgf-publisher:cordex:time-frequency',
    'esgf-publisher:cordex:variable',
    )


def parse(identifier, field='canonical_name'):
    """Parses a CMIP6 dataset identifier.

    """
    parser = create_template_parser(_TEMPLATE, _COLLECTIONS, field)
    parser.parse(identifier)
