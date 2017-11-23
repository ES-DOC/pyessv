# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parsers.__init__.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Expression parsers.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

from pyessv._constants import PARSING_STRICTNESS_1
from pyessv._constants import PARSING_STRICTNESS_SET
from pyessv._parsers.cmip5_dataset_id import parse as parse_cmip5_dataset_id
from pyessv._parsers.cmip6_dataset_id import parse as parse_cmip6_dataset_id
from pyessv._parsers.cordex_dataset_id import parse as parse_cordex_dataset_id
from pyessv._utils.compat import basestring



# Map of dataset id parsers to projects.
_DATASET_ID_PARSERS = {
    'cmip5': parse_cmip5_dataset_id,
    'cmip6': parse_cmip6_dataset_id,
    'cordex': parse_cordex_dataset_id
}


def parse_dataset_identifers(project, identifiers, strictness=PARSING_STRICTNESS_1):
    """Parses a collection of dataset identifiers.

    :param str project: Project code.
    :param iterable identifiers: Dataset identifiers.
    :param int strictness: Strictness level to apply when applying name matching rules.

    :returns: Facets extracted from the identifiers.
    :rtype: list

    """
    assert isinstance(identifiers, collections.Iterable), 'Invalid identifiers'

    result = set()
    for identifier in identifiers:
        result = result.union(parse_dataset_identifer(project, identifier, strictness))

    return result


def parse_dataset_identifer(project, identifier, strictness=PARSING_STRICTNESS_1):
    """Parses a dataset identifier.

    :param str project: Project code.
    :param str identifier: Dataset identifier.
    :param int strictness: Strictness level to apply when applying name matching rules.

    :returns: Set of terms extracted from the identifier.
    :rtype: set

    """
    assert isinstance(project, basestring), 'Invalid project'
    assert project in _DATASET_ID_PARSERS, 'Unsupported project'
    assert isinstance(identifier, basestring), 'Invalid identifier'
    assert strictness in PARSING_STRICTNESS_SET, 'Invalid strictness'

    parser = _DATASET_ID_PARSERS[project]

    return parser(identifier, strictness)
