# -*- coding: utf-8 -*-

"""
.. module:: pyessv._accessors.wcrp_cmip6.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to WCRP CMIP6 vocabs.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv



def _get_scope():
    """Returns target scope.

    """
    return pyessv.WCRP.cmip6


def get_institutes():
    """Returns set of participating institutes.

    """
    scope = _get_scope()

    return scope.institution_id


def get_institute_sources(institution_id):
    """Returns collection of source identifiers related to an institute.

    :param str institution_id: ID of an institute.

    :returns: Collection of source identifiers related to an institute.
    :rtype: list

    """
    scope = _get_scope()

    try:
        institution_id = institution_id.canonical_name
    except AttributeError:
        pass

    def _is_related(source_id):
        return institution_id in [i.lower() for i in source_id.data['institution_id']]

    return [i for i in scope.source_id if _is_related(i)]


def get_source_realms(source_id=None):
    """Returns collection of realms related to a source identifier.

    :param str source_id: ID of a source.

    :returns: Collection of realms related to a source-id.
    :rtype: list

    """
    def _is_realized(realm):
        return source_id.data['model_component'][realm.raw_name]['description'] != 'none'

    scope = _get_scope()

    return scope.realm if source_id is None else [i for i in scope.realm if _is_realized(i)]
