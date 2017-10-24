# -*- coding: utf-8 -*-

"""
.. module:: map_cmip6.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CMIP6 ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import map_comma_delimited_options
from utils import map_pipe_delimited_options


# Map of fields to mapped vocab collections.
VOCAB_COLLECTIONS = {
	('activity', map_comma_delimited_options),
	('cmor_table', map_comma_delimited_options),
	('experiment', map_pipe_delimited_options),
	('grid_label', map_comma_delimited_options),
	('frequency', map_comma_delimited_options),
	('source_id', map_comma_delimited_options)
}

# Map of fields to regular expressions.
REG_EX_COLLECTIONS = {
	('ensemble', r'r[0-9]i[0-9]p[0-9]f[0-9]'),
	('variable', r'^[a-z0-9]*$'),
	('version', r'v[0-9]')
}

# Set of fields to be appended as data.
DATA = {
	'filename_format',
	'directory_format',
	'dataset_id',
	'dataset_name_format'
}
