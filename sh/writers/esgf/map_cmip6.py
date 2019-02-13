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
	('variable_id', r'^[A-Za-z0-9]*$'),
	('las_time_delta', lambda: yield_las_time_delta),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('version', r'^v[0-9]{8}$'),
	('member_id', r'r[0-9]+i[0-9]+p[0-9]+'),
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_format',
	'directory_format',
	'dataset_id'
}


def yield_las_time_delta(ctx):
	"""Yields las time delta information to be converted to pyessv terms.

	"""
	for _, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		yield las_time_delta
