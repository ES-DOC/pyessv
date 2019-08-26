# -*- coding: utf-8 -*-

"""
.. module:: map_primavera.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps PRIMAVERA ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options

# Vocabulary collections extracted from ini file.
COLLECTIONS = [
    ('activity', yield_comma_delimited_options),
    ('model', yield_comma_delimited_options),
    ('institute', lambda: yield_institute),
    ('experiment', yield_pipe_delimited_options),
    ('ensemble', r'r[0-9]+i[0-9]+p[0-9]+f[0-9]+'),
    ('cmor_table', yield_comma_delimited_options),
    ('variable', r'^[A-Za-z0-9]*$'),
    ('grid_label', yield_comma_delimited_options),
    ('thredds_exclude_variables', yield_comma_delimited_options),
    ('dataset_version', r'latest|^v[0-9]*$'),
    ('file_period', r'fixed|^\d+-\d+(-clim)?$')
]

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
    'filename': {
        'template': '{}_{}_{}_{}_{}_{}_{}',
        'collections': (
            'variable',
            'cmor_table',
            'model',
            'experiment',
            'ensemble',
            'grid_label',
            'file_period'
        )
    },
    'directory_structure': {
        'template': 'PRIMAVERA/{}/{}=/{}/{}/{}/{}/{}/{}/{}',
        'collections': (
            'activity',
            'institute',
            'model',
            'experiment',
            'ensemble',
            'cmor_table',
            'variable',
            'grid_version',
            'dataset_version'
        )
    },
    'dataset_id': {
        'template': 'PRIMAVERA.{}.{}.{}.{}.{}.{}.{}.{}.{}',
        'collections': (
            'activity',
            'institute',
            'model',
            'experiment',
            'ensemble',
            'cmor_table',
            'variable',
            'grid_version',
            'dataset_version'
        )
    }
}


def yield_institute(ctx):
    """Yields institute information to be converted to pyessv terms.

    """
    for model, institute in ctx.ini_section.get_option('institute_map', '\n', '|'):
        src_namespace = 'wcrp:primavera:model:{}'.format(model.lower().replace('_', '-'))
        yield src_namespace, institute
