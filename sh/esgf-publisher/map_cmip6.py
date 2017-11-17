# -*- coding: utf-8 -*-

"""
.. module:: map_cmip6.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP6 ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options



# TODO process maps: institute_map, las_time_delta_map, model_cohort_map
# TODO process map: las_time_delta_map = las_time_delta_map = map(frequency : las_time_delta)

# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('activity', yield_comma_delimited_options),
	('cmor_table', yield_comma_delimited_options),
	('ensemble', r'r[0-9]i[0-9]p[0-9]f[0-9]'),
	('experiment', yield_pipe_delimited_options),
	('institute', lambda: yield_institute),
	('grid_label', yield_comma_delimited_options),
	('frequency', yield_comma_delimited_options),
	('las_time_delta', lambda: yield_las_time_delta),
	('source_id', yield_comma_delimited_options),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('variable', r'^[a-z0-9]*$'),
	('version', r'^[0-9]*$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_format',
	'directory_format',
	'dataset_id',
	'dataset_name_format'
}


def yield_institute(ctx):
	"""Yields insititute information to be converted to pyessv terms.

	"""
	for _, institute in ctx.ini_section.get_option('institute_map', '\n', '|'):
		yield institute, institute, institute


def yield_las_time_delta(ctx):
	"""Yields las time delta information to be converted to pyessv terms.

	"""
	for _, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		yield las_time_delta, las_time_delta, las_time_delta

