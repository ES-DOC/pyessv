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


# TODO process map: institute_map = map(model : institute)
# TODO process map: las_time_delta_map = map(time_frequency : las_time_delta)


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('product', yield_comma_delimited_options),
	('model', yield_comma_delimited_options),
	('impact_model', yield_comma_delimited_options),
	('experiment', yield_pipe_delimited_options),
	('sector_short', yield_comma_delimited_options),
	('social_forcing', yield_comma_delimited_options),
	('co2_forcing', yield_comma_delimited_options),
	('irrigation_forcing', yield_comma_delimited_options),
	('land_use_short', yield_comma_delimited_options),
	('time_frequency', yield_comma_delimited_options),
	('variable', yield_comma_delimited_options),
	('version', r'^v[0-9]*$'),
	('thredds_exclude_variables', yield_comma_delimited_options)
}


# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'directory_format',
	'dataset_id'
}


def yield_institute(ctx):
	"""Yields institute information to be converted to pyessv terms.

	"""
	for _, institute in ctx.ini_section.get_option('institute_map', '\n', '|'):
		yield institute


def yield_las_time_delta(ctx):
	"""Yields las time delta information to be converted to pyessv terms.

	"""
	for _, las_time_delta in ctx.ini_section.get_option('las_time_delta_map', '\n', '|'):
		yield las_time_delta