# -*- coding: utf-8 -*-

"""
.. module:: pyessv._accessors.esdoc_cmip6.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to ESDOC CMIP6 vocabs.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv



def _get_scope():
    """Returns target scope.

    """
    return pyessv.ESDOC.cmip6


def get_model_topics(source_id=None):
    """Returns topics to be documented by a source identifier.

    """
    def _requires_documentation(topic):
        if topic.canonical_name == 'toplevel':
            return True
        return source_id.data['model_component'][topic.raw_name]['description'] != 'none'

    scope = _get_scope()
    if source_id is None:
        return scope.model_topic
    else:
        return [i for i in scope.model_topic if _requires_documentation(i)]
