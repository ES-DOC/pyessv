# -*- coding: utf-8 -*-

"""
.. module:: map_cmip6.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP6 ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options

# Vocabulary collections extracted from ini file.
COLLECTIONS = [
    ('las_time_delta', lambda: yield_las_time_delta),
    ('model_cohort', lambda: yield_model_cohort),
    ('thredds_exclude_variables', yield_comma_delimited_options),
]

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
    'filename': {
        'template': '{}_{}_{}_{}_{}_{}_{}',
        'collections': (
            'variable_id',
            'table_id',
            'source_id',
            'experiment_id',
            'member_id',
            'grid_label'
            'file_period'
        )
    },
    'directory_structure': {
        'template': 'CMIP6/{}/{}/{}/{}/{}/{}/{}/{}/{}',
        'collections': (
            'activity_id',
            'institution_id',
            'source_id',
            'experiment_id',
            'member_id',
            'table_id',
            'variable_id',
            'grid_label',
            'dataset_version'
        )
    },
    'dataset_id': {
        'template': 'CMIP6.{}.{}.{}.{}.{}.{}.{}.{}.{}',
        'collections': (
            'activity_id',
            'institution_id',
            'source_id',
            'experiment_id',
            'member_id',
            'table_id',
            'variable_id',
            'grid_label',
            'dataset_version'
        )
    }
}


def yield_model_cohort(ctx):
    """Yields model cohort information to be converted to pyessv terms.

    """
    for source_id, model_cohort in ctx.ini_section.get_option('model_cohort_map', '\n', '|'):
        src_namespace = 'wcrp:cmip6:source-id:{}'.format(source_id.lower().replace('_', '-'))
        yield src_namespace, model_cohort


def yield_las_time_delta(ctx):
    """Yields las time delta information to be converted to pyessv terms.

    """
    for frequency, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
        src_namespace = 'wcrp:cmip6:frequency:{}'.format(frequency.lower().replace('_', '-'))
        yield src_namespace, las_time_delta
