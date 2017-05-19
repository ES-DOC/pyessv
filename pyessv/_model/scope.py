# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.scope.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary scope, e.g. CMIP6.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

import pyessv
from pyessv._model.node import IterableNode



class Scope(IterableNode):
    """A scope managed by an authority.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.authority = None
        self.collections = []
        super(Scope, self).__init__(self.collections, pyessv.NODE_TYPEKEY_SCOPE)


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority]
