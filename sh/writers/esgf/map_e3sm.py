# -*- coding: utf-8 -*-

"""
.. module:: map_e3sm.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps E3SM ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import yield_comma_delimited_options
from utils import yield_pipe_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('source', yield_comma_delimited_options),
	('model_version', yield_comma_delimited_options),
	('experiment', yield_pipe_delimited_options),
	('atmos_grid_resolution', yield_comma_delimited_options),
	('ocean_grid_resolution', yield_comma_delimited_options),
	('realm', yield_comma_delimited_options),
	('regridding', yield_comma_delimited_options),
	('data_type', yield_comma_delimited_options),
	('time_frequency', yield_comma_delimited_options),
	('ensemble_member', r'^[A-Za-z0-9]*$'),
	('thredds_exclude_variables', yield_comma_delimited_options),
	('version', r'^v[0-9]*$')
}

# Fields extracted from ini file & appended as data to the scope.
SCOPE_DATA = {
	'filename_format',
	'directory_format',
	'dataset_id'
}
