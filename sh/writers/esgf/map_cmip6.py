# -*- coding: utf-8 -*-

"""
.. module:: map_cmip6.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP6 ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options


# TODO process maps: institute_map, las_time_delta_map, model_cohort_map
# TODO process map: las_time_delta_map = las_time_delta_map = map(frequency : las_time_delta)

# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('las_time_delta', lambda: yield_las_time_delta),
	('thredds_exclude_variables', yield_comma_delimited_options),
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_template': '{}_{}_{}_{}_{}_{}_{}',
    'filename_collections': (
		'variable_id',
		'table_id',
		'source_id',
		'experiment_id',
		'member_id',
		'grid_label'
		'file_period'
		),
	'directory_template': 'CMIP6/{}/{}/{}/{}/{}/{}/{}/{}/{}',
	'directory_collections': (
		'activity_id',
		'institution_id',
		'source_id',
		'experiment_id',
		'member_id',
		'table_id',
		'variable_id',
		'grid_label',
		'dataset_version'
		),
	'dataset_id_template': 'CMIP6.{}.{}.{}.{}.{}.{}.{}.{}.{}',
	'dataset_id_collections': (
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


def yield_las_time_delta(ctx):
	"""Yields las time delta information to be converted to pyessv terms.

	"""
	for _, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		yield las_time_delta
