# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parsers.directory.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of an ESGF directory.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections

from pyessv import all_scopes
from pyessv._constants import PARSING_STRICTNESS_1
from pyessv._factory import create_template_parser
from pyessv._utils.compat import basestring

# Template extracted from esgf ini file (for reference purpose only).
_INI_PATTERN = '%(root)s/%(project)s/%(product)s/%(institute)s/%(model)s/%(experiment)s/%(time_frequency)s/%(realm)s/%(cmor_table)s/%(ensemble)s/%(version)s/%(variable)s'

# Test directory (for reference purpose only).
_TEST_DIRECTORY = 'CMIP5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/mon/atmos/Amon/r1i1p1/v20110427/tas'
_TEST_DIRECTORY = 'CMIP5/output1/IPSL/IPSL-CM5A-LR/1pctCO2/mon/atmos/Amon/r1i1p1/latest/tas'

# Instantiated template
_TEMPLATE = None

# Instantiated template collections
_COLLECTIONS = None

# Instantiated project.
_PROJECT = None

# Instantiated parser.
_PARSER = None


def parse_directories(project, directories):
    """Parses a collection of directories.

    :param str project: Project code.
    :param iterable directories: Data directories.

    :returns: Facets extracted from the directories.
    :rtype: list

    """
    assert isinstance(directories, collections.Iterable), 'Invalid directories'

    result = set()
    for directory in directories:
        result = result.union(parse_directory(project, directory))

    return result


def parse_directory(project, directory):
    """Parses a directory.

    :param str project: Project code.
    :param str directory: Data directory.

    :returns: Set of terms extracted from the directory.
    :rtype: set

    """
    assert isinstance(project, basestring), 'Invalid project'
    assert isinstance(directory, basestring), 'Invalid directory'

    global _PROJECT, _PARSER, _TEMPLATE, _COLLECTIONS

    if _PROJECT != project:

        # Instantiated template
        _TEMPLATE = None

        # Instantiated template collections
        _COLLECTIONS = None

        # Get scope corresponding to the project code.
        scopes = all_scopes()
        assert project in [scope.name for scope in scopes], 'Unsupported project'
        scope = [scope for scope in scopes if scope.name == project][0]

        # Get template from data scope.
        assert 'directory_template' in scope.data.keys(), 'Directory template not found'
        _TEMPLATE = scope.data['directory_template']
        assert isinstance(_TEMPLATE, basestring), 'Invalid template'

        # Get template collections from data scope.
        assert 'directory_collections' in scope.data.keys(), 'Template collections not found'
        _COLLECTIONS = list()
        for name in scope.data['directory_collections']:
            _COLLECTIONS.append([collection.namespace for collection in scope.collections if collection.name == name.replace('_','-')][0])
        assert _COLLECTIONS, 'Invalid collections'

        # Instantiate parser JIT.
        _PARSER = create_template_parser(_TEMPLATE, tuple(_COLLECTIONS), PARSING_STRICTNESS_1, separator='/')

        # Cached project.
        _PROJECT = project

    return _PARSER.parse(directory)
