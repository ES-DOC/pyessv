"""
.. module:: pyessv.accessors.copernicus_cordexp.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to COPERNICUS CORDEXP vocabs.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv



def get_scope():
    """Returns target scope.

    """
    return pyessv.COPERNICUS.CORDEXP


def get_institutes():
    """Returns set of participating institutes.

    """
    scope = get_scope()

    return scope.institution_id
