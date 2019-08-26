# -*- coding: utf-8 -*-

"""
.. module:: map_c3s_cordex.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps C3S-CORDEX ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options

# Vocabulary collections extracted from ini file.
COLLECTIONS = [
    ('domain', lambda: yield_domain),
    ('driving_model', yield_comma_delimited_options),
    ('ensemble', r'r[0-9]+i[0-9]+p[0-9]+'),
    ('experiment', yield_pipe_delimited_options),
    ('institute', yield_comma_delimited_options),
    ('product', yield_comma_delimited_options),
    ('rcm_model', yield_comma_delimited_options),
    ('rcm_name', lambda: yield_rcm_name),
    ('rcm_version', yield_comma_delimited_options),
    ('thredds_exclude_variables', yield_comma_delimited_options),
    ('time_frequency', yield_comma_delimited_options),
    ('variable', yield_comma_delimited_options),
    ('dataset_version', r'latest|v^[0-9]*$'),
    ('file_period', r'fixed|^\d+-\d+(-clim)?$')
]

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
    'filename': {
            'template': '{}_{}_{}_{}_{}_{}_{}_{}_{}',
            'collections': (
                'variable',
                'domain',
                'driving_model',
                'experiment',
                'ensemble',
                'rcm_model',
                'rcm_version',
                'time_frequency',
                'file_period'
            )
        },
    'directory_structure': {
            'template': 'C3S-CORDEX/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}',
            'collections': (
                'product',
                'domain',
                'institute',
                'driving_model',
                'experiment',
                'ensemble',
                'rcm_model',
                'rcm_version',
                'time_frequency',
                'variable',
                'dataset_version'
            )
        },
    'dataset_id': {
        'template': 'c3s-cordex.{}.{}.{}.{}.{}.{}.{}.{}.{}.{}.{}',
        'collections': (
            'product',
            'domain',
            'institute',
            'driving_model',
            'experiment',
            'ensemble',
            'rcm_name',
            'rcm_version',
            'time_frequency',
            'variable',
            'dataset_version'
        )
    }
}


def yield_domain(ctx):
    """Yields domain information to be converted to pyessv terms.

    """
    for domain_name, domain_description in ctx.ini_section.get_option('domain_description_map', '\n', '|'):
        yield domain_name, domain_name, domain_description


def yield_rcm_name(ctx):
    """Yields rcm name information to be converted to pyessv terms.

    """
    for rcm_model, rcm_name in ctx.ini_section.get_option('rcm_name_map', '\n', '|'):
        src_namespace = 'ecmwf:c3s-cordex:rcm_model:{}'.format(rcm_model.lower().replace('_', '-'))
        yield src_namespace, rcm_name
