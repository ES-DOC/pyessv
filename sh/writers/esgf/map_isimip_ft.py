# -*- coding: utf-8 -*-

"""
.. module:: map_isimip_ft.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps ISIMIP-FT ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
    ('product', yield_comma_delimited_options),
    ('model', yield_comma_delimited_options),
    ('impact_model', yield_comma_delimited_options),
    ('experiment', yield_pipe_delimited_options),
    ('sector_short', lambda: yield_sector),
    ('social_forcing', yield_comma_delimited_options),
    ('institute', lambda: yield_institute),
    ('co2_forcing', yield_comma_delimited_options),
    ('irrigation_forcing', yield_comma_delimited_options),
    ('land_use_short', lambda: yield_land_use),
    ('time_frequency', yield_comma_delimited_options),
    ('variable', yield_comma_delimited_options),
    ('dataset_version', r'latest|^v[0-9]*$'),
    ('thredds_exclude_variables', yield_comma_delimited_options),
    ('file_period', r'fixed|^\d+-\d+(-clim)?$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
    'filename': {
        'template': '{}_{}_{}_{}_{}_{}_{}_{}_{}_{}',
        'collections': (
            'impact_model',
            'model',
            'experiment',
            'social_forcing',
            'co2_forcing',
            'irrigation_forcing',
            'land_use_short',
            'variable'
            'time_frequency',
            'file_period'
        )
    },
    'directory_structure': {
        'template': 'ISIMIP-FT/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}',
        'collections': (
            'product',
            'model',
            'experiment',
            'impact_model',
            'sector_short',
            'social_forcing',
            'co2_forcing',
            'irrigation_forcing',
            'land_use_short',
            'variable'
            'time_frequency',
            'dataset_version'
        )
    },
    'dataset_id': {
        'template': 'isimip-ft.{}.{}.{}.{}.{}.{}.{}.{}.{}.{}.{}.{}',
        'collections': (
            'product',
            'impact_model',
            'sector_short',
            'model',
            'experiment',
            'social_forcing',
            'co2_forcing',
            'irrigation_forcing',
            'time_frequency',
            'land_use_short',
            'variable'
            'dataset_version'
        )
    }
}


def yield_institute(ctx):
    """Yields institute information to be converted to pyessv terms.

    """
    for model, institute in ctx.ini_section.get_option('institute_map', '\n', '|'):
        src_namespace = 'wcrp:isimip-ft:impact-model:{}'.format(model.lower().replace('_', '-'))
        yield src_namespace, institute


def yield_land_use(ctx):
    """Yields land use information to be converted to pyessv terms.

    """
    for land_use_acronym, land_use in ctx.ini_section.get_option('land_use_map', '\n', '|'):
        yield land_use_acronym, land_use_acronym, land_use


def yield_sector(ctx):
    """Yields sector information to be converted to pyessv terms.

    """
    for sector_acronym, sector in ctx.ini_section.get_option('sector_map', '\n', '|'):
        yield sector_acronym, sector_acronym, sector
