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
	('dataset_version', r'latest|^v[0-9]*$'),
	('file_period', r'fixed|^\d+-\d+(-clim)?$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_template': '{}_cc4e_{}_{}_{}_{}_{}_{}_{}_{}',
    'filename_collections': (
		'variable',
		'work_package',
		'product',
		'source_type',
		'source_data_id',
		'realization',
		'domain',
		'time_frequency',
		'file_period'
		),
	'directory_template': 'CC4E/{}/{}/{}/{}/{}/{}/{}/{}',
	'directory_collections': (
		'work_package',
		'product',
		'source_type',
		'source_data_id',
		'realization',
		'time_frequency',
		'variable',
		'dataset_version'
		),
	'dataset_id_template': 'CC4E.{}.{}.{}.{}.{}.{}.{}.{}',
	'dataset_id_collections': (
		'work_package',
		'product',
		'source_type',
		'source_data_id',
		'realization',
		'time_frequency',
		'variable',
		'dataset_version'
		)
}
