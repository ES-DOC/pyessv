# -*- coding: utf-8 -*-

"""
.. module:: map_cordex.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CORDEX ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import map_comma_delimited_options
from utils import map_pipe_delimited_options



# Map of fields to mapped vocab collections.
VOCAB_COLLECTIONS = {
	('domain', lambda: map_domain),
	('driving_model', map_comma_delimited_options),
	('experiment', map_pipe_delimited_options),
	('institute', map_comma_delimited_options),
	('las_time_delta', lambda: map_las_time_delta),
	('product', map_comma_delimited_options),
	('rcm_model', map_comma_delimited_options),
	('rcm_version', map_comma_delimited_options),
	('thredds_exclude_variables', map_comma_delimited_options),
	('time_frequency', map_comma_delimited_options),
	('variable', map_comma_delimited_options),
}

# Map of fields to regular expressions.
REG_EX_COLLECTIONS = dict()

# Set of fields to be appended as data.
DATA = {
	'filename_format',
	'dataset_id',
	'directory_format',
	'ensemble_pattern',
	'version_pattern'
}


def map_domain(ctx):
	"""Converts CORDEX domain to pyessv terms.

	"""
	for _, domain_name, domain_description in ctx.ini_section.get_option('domain_description_map', '\n', '|'):
		term_name = domain_name
		term_label = domain_name
		term_description = domain_description

		yield term_name, term_label, term_description


def map_las_time_delta(ctx):
	"""Converts CORDEX las time delta to pyessv terms.

	"""
	for time_frequency, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		term_name = las_time_delta
		term_label = las_time_delta
		term_description = las_time_delta

		# print time_frequency, las_time_delta

		yield term_name, term_label, term_description

