# -*- coding: utf-8 -*-

"""
.. module:: map_primavera.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps PRIMAVERA ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options


# TODO process map: institute_map = map(model : institute)

# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('activity', yield_comma_delimited_options),
	('institute', lambda: yield_institute),
	('model', yield_comma_delimited_options),
	('experiment', yield_pipe_delimited_options),
	('ensemble', r'r[0-9]+i[0-9]+p[0-9]+f[0-9]+'),
	('cmor_table', yield_comma_delimited_options),
	('variable', r'^[A-Za-z0-9]*$'),
	('grid_label', yield_comma_delimited_options),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('version', r'^v[0-9]*$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_format',
	'directory_format',
	'dataset_id'
}


def yield_institute(ctx):
	"""Yields institute information to be converted to pyessv terms.

	"""
	for _, institute in ctx.ini_section.get_option('institute_map', '\n', '|'):
		yield institute
