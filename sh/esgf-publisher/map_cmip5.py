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
	('experiment', map_pipe_delimited_options),
	('model', map_comma_delimited_options),
	('time_frequency', map_comma_delimited_options),
	('product', map_comma_delimited_options),
	('realm', map_comma_delimited_options),
	('thredds_exclude_variables', map_comma_delimited_options),
	('variable', map_comma_delimited_options)
}

# Map of fields to regular expressions.
REG_EX_COLLECTIONS = {
	('ensemble', r'r[0-9]i[0-9]p[0-9]'),
	('version', r'v[0-9]')
}

# Set of fields to be appended as data.
DATA = {
	'filename_format',
	'directory_format',
	'dataset_id',
	'dataset_name_format'
}
