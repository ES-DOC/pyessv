# -*- coding: utf-8 -*-

"""
.. module:: map_c3s_cmip5.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps C3S-CMIP5 ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = [
    ('cmor_table', yield_comma_delimited_options),
    ('ensemble', r'r[0-9]+i[0-9]+p[0-9]+'),
    ('experiment', yield_pipe_delimited_options),
    ('model', yield_comma_delimited_options),
    ('institute', lambda: yield_institute),
    ('time_frequency', yield_comma_delimited_options),
    ('product', yield_comma_delimited_options),
    ('realm', yield_comma_delimited_options),
    ('thredds_exclude_variables', yield_comma_delimited_options),
    ('variable', yield_comma_delimited_options),
    ('dataset_version', r'latest|^v[0-9]*$'),
    ('file_period', r'fixed|^\d+-\d+(-clim)?$')
]

# Arbitrary data associated with a collection.
COLLECTION_DATA = {
    'experiment': {
        'cim_document_type': 'cim.1.activity.NumericalExperiment',
        'cim_document_type_alternative_name': 'experiment'
    },
    'model': {
        'cim_document_type': 'cim.1.software.ModelComponent',
        'cim_document_type_alternative_name': 'model'
    }
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
        'template': 'C3S-CMIP5/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}',
        'collections': (
            'product',
            'institute',
            'model',
            'experiment',
            'time_frequency',
            'realm',
            'cmor_table',
            'ensemble',
            'variable',
            'dataset_version'
        )
    },
    'dataset_id': {
        'template': 'c3s-cmip5.{}.{}.{}.{}.{}.{}.{}.{}.{}',
        'collections': (
            'product',
            'institute',
            'model',
            'experiment',
            'time_frequency',
            'realm',
            'cmor_table',
            'ensemble',
            'variable',
            'dataset_version'
        )
    }
}


def yield_institute(ctx):
    """Yields institute information to be converted to pyessv terms.

    """
    for model, institute in ctx.ini_section.get_option('institute_map', '\n', '|'):
        src_namespace = 'ecmwf:c3s-cmip5:model:{}'.format(model.lower().replace('_', '-'))
        yield src_namespace, institute
