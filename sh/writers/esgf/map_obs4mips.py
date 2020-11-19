# -*- coding: utf-8 -*-

"""
.. module:: map_obs4mips.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps obs4MIPs ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('activity_id', yield_comma_delimited_options),
	('institution_id', yield_comma_delimited_options),
	('source_id', yield_comma_delimited_options),
	('frequency', yield_comma_delimited_options),
	('variable_id', r'^[A-Za-z0-9]*$'),
	('grid_label', yield_comma_delimited_options),
	('variant_label', r'^[A-Za-z0-9]*$'),
	('realm', r'^[A-Za-z0-9]*$'),
	('product', r'^[A-Za-z0-9]*$'),
	('thredds_exclude_variables', yield_comma_delimited_options),
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'directory_format',
	'dataset_id'
}
