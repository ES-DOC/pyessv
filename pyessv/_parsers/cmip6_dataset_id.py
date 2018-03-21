# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parsers.cmip6_dataset_id.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of a CMIP6 dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv._factory import create_template_parser
from pyessv._constants import PARSING_STRICTNESS_1



# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = 'CMIP6.%(activity_id)s.%(institution_id)s.%(source_id)s.%(experiment_id)s.%(member_id)s.%(table_id)s.%(variable_id)s.%(grid_label)s'

# Template that identifiers must conform to.
_TEMPLATE = 'CMIP6.{}.{}.{}.{}.{}.{}.{}.{}'

# Collections injected into template.
_COLLECTIONS = (
    'wcrp:cmip6:activity-id',
    'wcrp:cmip6:institution-id',
    'wcrp:cmip6:source-id',
    'wcrp:cmip6:experiment-id',
    'wcrp:cmip6:member-id',
    'wcrp:cmip6:table-id',
    'wcrp:cmip6:variable-id',
    'wcrp:cmip6:grid-label'
    )


def parse(identifier):
    """Parses a CMIP6 dataset identifier.

    """
    parser = create_template_parser(_TEMPLATE, _COLLECTIONS, PARSING_STRICTNESS_1)

    # Strip version suffix.
    if '#' in identifier:
      identifier = identifier.split('#')[0]

    return parser.parse(identifier)
