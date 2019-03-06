# -*- coding: utf-8 -*-

"""
.. module:: map_input4mips.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps input4MIPs ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('variable_id', yield_comma_delimited_options),
	('activity_id', yield_comma_delimited_options),
	('dataset_category', r'^[A-Za-z0-9]*$'),
	('target_mip', yield_comma_delimited_options),
	('source_id', yield_comma_delimited_options),
	('grid_label', yield_comma_delimited_options),
	('institution_id', yield_comma_delimited_options),
	('realm', yield_comma_delimited_options),
	('frequency', yield_comma_delimited_options),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('version', r'^v[0-9]{8}$'),
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_format',
	'directory_format',
	'dataset_id'
}
