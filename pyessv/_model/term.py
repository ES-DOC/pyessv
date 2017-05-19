# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.term.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary term, e.g. IPSL.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
from pyessv._model.node import Node
from pyessv._utils.compat import str



class Term(Node):
    """A vocabulary term.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Term, self).__init__(pyessv.NODE_TYPEKEY_TERM)

        self.alternative_name = None
        self.alternative_url = None
        self.associations = list()
        self.collection = None
        self.idx = None
        self.parent = None
        self.status = pyessv.GOVERNANCE_STATUS_PENDING


    def __contains__(self, key):
        """Instance membership predicate.

        """
        key = str(key).strip().lower()

        return key in self.all_names


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority, self.scope, self.collection]


    @property
    def authority(self):
        """Gets governing authority.

        """
        return self.scope.authority


    @property
    def scope(self):
        """Gets governing scope.

        """
        return self.collection.scope
