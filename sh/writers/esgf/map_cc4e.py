# -*- coding: utf-8 -*-

"""
.. module:: map_cc4e.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps CC4E ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('work_package', yield_comma_delimited_options),
	('product', yield_comma_delimited_options),
	('source_type', yield_comma_delimited_options),
	('source_data_id', yield_comma_delimited_options),
	('realization', r'r[0-9]+'),
	('domain', yield_comma_delimited_options),
	('time_frequency', yield_comma_delimited_options),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('variable', yield_comma_delimited_options),
	('version', r'^v[0-9]*$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_format',
	'directory_format',
	'dataset_id'
}
