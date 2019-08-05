# -*- coding: utf-8 -*-

"""
.. module:: map_geomip.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps GeoMIP ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('cmor_table', yield_comma_delimited_options),
	('ensemble', r'r[0-9]+i[0-9]+p[0-9]+'),
	('experiment', yield_pipe_delimited_options),
	('institute', lambda: yield_institute),
	('las_time_delta', lambda: yield_las_time_delta),
	('model', yield_comma_delimited_options),
	('time_frequency', yield_comma_delimited_options),
	('product', yield_comma_delimited_options),
	('realm', yield_comma_delimited_options),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('variable', yield_comma_delimited_options),
	('dataset_version', r'latest|^v[0-9]*$'),
	('file_period', r'fixed|^\d+-\d+(-clim)?$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
    'filename': {
        'template': '{}_{}_{}_{}_{}_{}',
        'collections': (
            'variable',
            'cmor_table',
            'model',
            'experiment',
            'ensemble',
            'file_period'
        )
    },
    'directory_structure': {
        'template': 'GeoMIP/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}',
        'collections': (
            'product',
            'institute',
            'model',
            'experiment',
            'time_frequency',
            'realm',
            'cmor_table',
            'ensemble',
            'dataset_version',
            'variable'
        ),
    },
    'dataset_id': {
        'template': 'geomip.{}.{}.{}.{}.{}.{}.{}.{}.{}',
        'collections': (
            'product',
            'institute',
            'model',
            'experiment',
            'time_frequency',
            'realm',
            'cmor_table',
            'ensemble',
            'dataset_version'
        )
    }
}


def yield_las_time_delta(ctx):
    """Yields las time delta information to be converted to pyessv terms.

    """
    for time_frequency, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
        src_namespace = 'wcrp:geomip:time-frequency:{}'.format(time_frequency.lower().replace('_', '-'))
        yield src_namespace, las_time_delta


def yield_institute(ctx):
    """Yields institute information to be converted to pyessv terms.

    """
    for model, institute in ctx.ini_section.get_option('institute_map', '\n', '|'):
        src_namespace = 'wcrp:geomip:model:{}'.format(model.lower().replace('_', '-'))
        yield src_namespace, institute

