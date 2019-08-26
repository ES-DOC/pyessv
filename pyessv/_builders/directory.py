# -*- coding: utf-8 -*-

"""
.. module:: pyessv._builders.dataset_id.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates building of an ESGF dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv._model.term import Term
from pyessv import all_scopes
from pyessv._constants import PARSING_STRICTNESS_1
from pyessv._factory import create_template_builder
from pyessv._utils.compat import basestring

# Instantiated template
_TEMPLATE = None

# Instantiated template collections
_COLLECTIONS = None

# Instantiated project.
_PROJECT = None

# Instantiated builder.
_BUILDER = None


def build_directory(project, terms):
    """Builds a directory.

    :param str project: Project code.
    :param set terms: Directory terms.

    :returns: Directory string.
    :rtype: str

    """
    assert isinstance(project, basestring), 'Invalid project'
    assert isinstance(terms, set), 'Invalid terms'

    global _PROJECT, _BUILDER, _TEMPLATE, _COLLECTIONS

    if _PROJECT != project:

        # Get scope corresponding to the project code.
        scopes = all_scopes()
        assert project in [scope.name for scope in scopes], 'Unsupported project'
        scope = [scope for scope in scopes if scope.name == project][0]

        assert 'directory_structure' in scope.data.keys(), 'Directory parser not found'
        assert 'template' in scope.data['directory_structure'].keys(), 'Directory parser template not found'
        assert 'collections' in scope.data['directory_structure'].keys(), 'Directory parser template collections not found'

        # Get template from data scope.
        _TEMPLATE = scope.data['directory_structure']['template']
        assert isinstance(_TEMPLATE, basestring), 'Invalid template'

        # Get template collections from data scope.
        _COLLECTIONS = list()
        for name in scope.data['directory_structure']['collections']:
            _COLLECTIONS.append([collection.namespace for collection in scope.collections if collection.name == name.replace('_','-')][0])
        assert _COLLECTIONS, 'Invalid collections'

        # Instantiate parser JIT.
        _BUILDER = create_template_builder(_TEMPLATE, tuple(_COLLECTIONS), PARSING_STRICTNESS_1, separator='/')

        # Cached project.
        _PROJECT = project

    for term in terms:
        assert isinstance(term, Term), 'Invalid term :: {}'.format(term)

    return _BUILDER.build(terms)
