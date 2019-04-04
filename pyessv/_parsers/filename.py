# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parsers.filename.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of an ESGF filename.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections
from os.path import splitext

from pyessv import all_scopes
from pyessv._constants import PARSING_STRICTNESS_1
from pyessv._exceptions import TemplateParsingError
from pyessv._factory import create_template_parser

# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = '%(variable)s_%(cmor_table)s_%(model)s_%(experiment)s_%(ensemble)s[_%(period_start)s-%(period_end)s].nc'

# Test filename (for reference purpose only).
_TEST_FILENAME = 'tas_Amon_IPSL-CM5A-LR_1pctCO2_r1i1p1_185001-198912.nc'
_TEST_FILENAME = 'orog_fx_IPSL-CM5A-LR_1pctCO2_r0i0p0.nc'
_TEST_FILENAME = 'tas_Amon_IPSL-CM5A-LR_1pctCO2_r1i1p1_185001-198912-clim.nc'

# Instantiated & cached parser instance.
_PARSER = None


def parse_filenames(project, filenames):
    """Parses a collection of filenames.

    :param str project: Project code.
    :param iterable filenames: Filenames.

    :returns: Facets extracted from the filenames.
    :rtype: list

    """
    assert isinstance(filenames, collections.Iterable), 'Invalid filenames'

    result = set()
    for filename in filenames:
        result = result.union(parse_filename(project, filename))

    return result


def parse_filename(project, filename):
    """Parses a filename.

    :param str project: Project code.
    :param str filename: Filename.

    :returns: Set of terms extracted from the filename.
    :rtype: set

    """
    assert isinstance(project, basestring), 'Invalid project'
    assert isinstance(filename, basestring), 'Invalid filename'

    # Instantiated template
    _TEMPLATE = None

    # Instantiated template collections
    _COLLECTIONS = None

    # Get scope corresponding to the project code.
    scopes = all_scopes()
    assert project in [scope.name for scope in scopes], 'Unsupported project'
    scope = [scope for scope in scopes if scope.name == project][0]

    # Get template from data scope.
    assert 'filename_template' in scope.data.keys(), 'Filename template not found'
    _TEMPLATE = scope.data['filename_template']
    assert isinstance(_TEMPLATE, basestring), 'Invalid template'

    # Get template collections from data scope.
    assert 'filename_collections' in scope.data.keys(), 'Filename collections not found'
    _COLLECTIONS = list()
    for name in scope.data['filename_collections']:
        _COLLECTIONS.append([collection.namespace for collection in scope.collections if collection.name == name.replace('_','-')][0])
    assert _COLLECTIONS, 'Invalid collections'

    # Instantiate parser JIT.
    global _PARSER
    if _PARSER is None:
        _PARSER = create_template_parser(_TEMPLATE, tuple(_COLLECTIONS), PARSING_STRICTNESS_1, separator='_')

    # Strip file extension.
    filename = splitext(filename)[0]

    try:
        return _PARSER.parse(filename)
    except TemplateParsingError:
        # Add suffix to filename without file period.
        return _PARSER.parse(filename + '_fixed')
