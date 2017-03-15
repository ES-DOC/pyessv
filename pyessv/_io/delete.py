# -*- coding: utf-8 -*-

"""
.. module:: pyessv.io.delete.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates deleting terms from file sytem.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

from pyessv._model import Authority
from pyessv._model import Term



def delete_authority(authority):
    """Deletes authority CV data from file system.

    """
    if not isinstance(authority, Authority):
        raise ValueError("Invalid authority: unknown type")

    if authority.io_path:
        os.remove(authority.io_path)


def delete_term(term):
    """Deletes term CV data from file system.

    """
    if not isinstance(term, Term):
        raise ValueError("Invalid term: unknown type")

    if term.io_path:
        os.remove(term.io_path)

