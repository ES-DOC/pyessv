# -*- coding: utf-8 -*-

"""
.. module:: map_input4mips.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps input4MIPs ESGF publisher ini file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from utils import get_ini_option
from utils import yield_comma_delimited_options


# Vocabulary collections extracted from ini file.
COLLECTIONS = {
	('variable_id', lambda: yield_variable_id_options),
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

def yield_variable_id_options(ctx):
    # Decode options from ini file.
    opts = get_ini_option(ctx)
    opts = [i.strip() for i in opts.split(',')]
    opts = [i for i in opts if len(i)]

    # Setup collections used to filter out unique options.
    opts_without_hyphen_and_uscore = [i for i in opts if '-' not in i and '_' not in i]
    opts_with_hyphen = [i for i in opts if '-' in i]
    opts_with_uscore = [i for i in opts if '_' in i]
    opts_with_uscore_not_in_hyphen = [i for i in opts_with_uscore if i.replace('_', '-') not in opts_with_hyphen]

    # Options without hyphen and underscore are unique.
    for opt in opts_without_hyphen_and_uscore:
        yield opt, opt, opt

    # Options without hyphen but with underscore are unique.
    for opt in opts_with_uscore_not_in_hyphen:
        yield opt, opt, opt

    # Options with hyphens but no underscore are unique.
    for opt in opts_with_hyphen:
        if opt.replace('-', '_') not in opts_with_uscore:
            yield opt, opt, opt
        else:
            yield opt, opt, opt, opt.replace('-', '_')
