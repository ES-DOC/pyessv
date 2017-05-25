# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.collection.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary collection, e.g. institute-id.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

import pyessv
from pyessv._model.node import IterableNode



class Collection(IterableNode):
    """A vocabulary term collection.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.scope = None
        self.terms = []
        self.term_regex = None
        self.template = None
        self.template_collections = None
        super(Collection, self).__init__(self.terms, pyessv.NODE_TYPEKEY_COLLECTION)


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority, self.scope]


    @property
    def authority(self):
        """Gets governing authority.

        """
        return self.scope.authority
