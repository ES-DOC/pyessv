"""
.. module:: pyessv.parsers.cmip6_dataset_id.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of a CMIP6 dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv.factory import create_template_parser
from pyessv.constants import PARSING_STRICTNESS_3



# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = '%(activity_id)s.%(mip_era)s.%(target_mip)s.%(institution_id)s.%(source_id)s.%(realm)s.%(frequency)s.%(variable_id)s.%(grid_label)s'

# Template that identifiers must conform to.
_TEMPLATE = 'input4MIPs.CMIP6.{}.{}.{}.{}.{}.{}.{}'

# Collections injected into template.
_COLLECTIONS = (
    'wcrp:input4mips:target-mip',
    'wcrp:input4mips:institution-id',
    'wcrp:input4mips:source-id',
    'wcrp:input4mips:realm',
    'wcrp:input4mips:frequency',
    'wcrp:input4mips:variable-id',
    'wcrp:input4mips:grid-label',
    )

# Instantiated & cached parser instance.
_PARSER = None


def parse(identifier):
    """Parses a CMIP6 dataset identifier.

    """
    # Instantiate parser JIT.
    global _PARSER
    if _PARSER is None:
        _PARSER = create_template_parser(_TEMPLATE, _COLLECTIONS, PARSING_STRICTNESS_3)

    # Strip version suffix.
    if '#' in identifier:
      identifier = identifier.split('#')[0]

    return _PARSER.parse(identifier)
