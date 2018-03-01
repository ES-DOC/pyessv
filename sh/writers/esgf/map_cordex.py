# -*- coding: utf-8 -*-

"""
.. module:: map_cordex.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CORDEX ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options


# TODO process map: las_time_delta_map = map(time_frequency : las_time_delta)
# TODO process map: rcm_name_map = map(project, rcm_model : rcm_name)

# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('domain', lambda: yield_domain),
	('driving_model', yield_comma_delimited_options),
	('ensemble', r'r[0-9]*i[0-9]p[0-9]'),
	('experiment', yield_pipe_delimited_options),
	('institute', yield_comma_delimited_options),
	('las_time_delta', lambda: yield_las_time_delta),
	('product', yield_comma_delimited_options),
	('rcm_model', yield_comma_delimited_options),
	('rcm_name', lambda: yield_rcm_name),
	('rcm_version', yield_comma_delimited_options),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('time_frequency', yield_comma_delimited_options),
	('variable', yield_comma_delimited_options),
	('version', r'^[0-9]*$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_format',
	'dataset_id',
	'directory_format',
	'ensemble_pattern',
	'version_pattern'
}


def yield_domain(ctx):
	"""Yields domain information to be converted to pyessv terms.

	"""
	for domain_name, domain_description in ctx.ini_section.get_option('domain_description_map', '\n', '|'):
		yield domain_name, domain_name, domain_description


def yield_las_time_delta(ctx):
	"""Yields las time delta information to be converted to pyessv terms.

	"""
	for _, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		yield las_time_delta


def yield_rcm_name(ctx):
	"""Yields rcm name information to be converted to pyessv terms.

	"""
	for _, rcm_name in ctx.ini_section.get_option('rcm_name_map', '\n', '|'):
		yield rcm_name
