# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.authority.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary authority, e.g. WGCM.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

import pyessv
from pyessv._model.node import IterableNode



class Authority(IterableNode):
    """An authority assuming responsibity for governance of vocabularies.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.scopes = []
        super(Authority, self).__init__(self.scopes, pyessv.NODE_TYPEKEY_AUTHORITY)


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return []
