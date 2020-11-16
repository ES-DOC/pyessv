# -*- coding: utf-8 -*-

"""
.. module:: map_obs4mips.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps obs4MIPs ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options


# TODO process map: las_time_delta_map = map(time_frequency : las_time_delta)

# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('product', yield_comma_delimited_options),
	('institute', yield_comma_delimited_options),
	('realm', yield_comma_delimited_options),
	('variable', lambda: yield_variable),
	('time_frequency', yield_comma_delimited_options),
	('data_structure', yield_comma_delimited_options),
	('source_id', yield_comma_delimited_options),
	('version', r'^v[0-9]*$'),
	('las_time_delta', lambda: yield_las_time_delta),
	('thredds_exclude_variables', yield_comma_delimited_options)
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'directory_format',
	'dataset_id'
}


def yield_variable(ctx):
	"""Yields institute information to be converted to pyessv terms.

	"""
	for var, _ in ctx.ini_section.get_option('variable_map', '\n', '|'):
		yield var


def yield_las_time_delta(ctx):
	"""Yields las time delta information to be converted to pyessv terms.

	"""
	for _, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		yield las_time_delta
