# -*- coding: utf-8 -*-

"""
.. module:: map_obs4mips.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps obs4MIPs ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options


# TODO process map: las_time_delta_map = map(time_frequency : las_time_delta)

# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('product', r'^[A-Za-z0-9]*$'),
	('institution_id', yield_comma_delimited_options),
	('realm', r'^[A-Za-z0-9]*$'),
	('variable', r'^[A-Za-z0-9]*$'),
	('frequency', yield_comma_delimited_options),
	('source_id', yield_comma_delimited_options),
	('version', r'^v[0-9]*$'),
	('thredds_exclude_variables', yield_comma_delimited_options)
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'directory_format',
	'dataset_id'
}

