"""
.. module:: pyessv.parsers.cordex_dataset_id.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of a CORDEX dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv.factory import create_template_parser
from pyessv.constants import PARSING_STRICTNESS_1



# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = 'cordex.%(product)s.%(domain)s.%(institute)s.%(drivingmodel)s.%(experiment)s.%(ensemble)s.%(rcm_name)s.%(rcm_version)s.%(time_frequency)s.%(variable)s'

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

# Instantiated & cached parser instance.
_PARSER = None

def parse(identifier):
    """Parses a CMIP6 dataset identifier.

    """
    # Instantiate parser JIT.
    global _PARSER
    if _PARSER is None:
        _PARSER = create_template_parser(_TEMPLATE, _COLLECTIONS, PARSING_STRICTNESS_1)

    # Strip version suffix.
    if '#' in identifier:
      identifier = identifier.split('#')[0]

    return _PARSER.parse(identifier)
