# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parsers.dataset_id.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of an ESGF dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import collections

from pyessv import all_scopes
from pyessv._constants import PARSING_STRICTNESS_1
from pyessv._factory import create_template_parser
from pyessv._utils.compat import basestring

# Test identifier (for reference purpose only).
_TEST_CMIP5_IDENTIFIER = 'cmip5.output2.IPSL.IPSL-CM5A-LR.historicalMisc.mon.ocean.Omon.r2i1p1.v20150504'
_TEST_CORDEX_IDENTIFIER = 'cordex.output.AFR-44.MOHC.MOHC-HadGEM2-ES.rcp60.r12i1p1.hadgem3-ra.v1.mon.areacella'

# Instantiated template
_TEMPLATE = None

# Instantiated template collections
_COLLECTIONS = None

# Instantiated project.
_PROJECT = None

# Instantiated parser.
_PARSER = None


def parse_dataset_identifiers(project, identifiers):
    """Parses a collection of dataset identifiers.

    :param str project: Project code.
    :param iterable identifiers: Dataset identifiers.

    :returns: Facets extracted from the identifiers.
    :rtype: list

    """
    assert isinstance(identifiers, collections.Iterable), 'Invalid identifiers'

    result = set()
    for identifier in identifiers:
        result = result.union(parse_dataset_identifier(project, identifier))

    return result


def parse_dataset_identifier(project, identifier):
    """Parses a dataset identifier.

    :param str project: Project code.
    :param str identifier: Dataset identifier.

    :returns: Set of terms extracted from the identifier.
    :rtype: set

    """
    assert isinstance(project, basestring), 'Invalid project'
    assert isinstance(identifier, basestring), 'Invalid identifier'

    global _PROJECT, _PARSER, _TEMPLATE, _COLLECTIONS

    if _PROJECT != project:

        # Get scope corresponding to the project code.
        scopes = all_scopes()
        assert project in [scope.name for scope in scopes], 'Unsupported project'
        scope = [scope for scope in scopes if scope.name == project][0]

        # Get template from data scope.
        assert 'dataset_id_template' in scope.data.keys(), 'Dataset ID template not found'
        _TEMPLATE = scope.data['dataset_id_template']
        assert isinstance(_TEMPLATE, basestring), 'Invalid template'

        # Get template collections from data scope.
        assert 'dataset_id_collections' in scope.data.keys(), 'Template collections not found'
        _COLLECTIONS = list()
        for name in scope.data['dataset_id_collections']:
            _COLLECTIONS.append([collection.namespace for collection in scope.collections if collection.name == name.replace('_','-')][0])
        assert _COLLECTIONS, 'Invalid collections'

        # Instantiate parser JIT.
        global _PARSER
        _PARSER = create_template_parser(_TEMPLATE, tuple(_COLLECTIONS), PARSING_STRICTNESS_1)

        # Cached project.
        _PROJECT = project

    # Convert version suffix to an identifier element.
    identifier = identifier.replace('#', '.v')

    return _PARSER.parse(identifier)
