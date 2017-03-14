# -*- coding: utf-8 -*-

"""
.. module:: pyessv.model.authority.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary authority, e.g. WGCM.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.model.entity import Entity



class Authority(Entity):
    """An authority assuming responsibity for governance of vocabularies.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.create_date = None
        self.description = None
        self.label = None
        self.name = None
        self.scopes = list()
        self.url = None


    def __repr__(self):
        """Instance representation.

        """
        return self.namespace


    def __len__(self):
        """Returns number of items in managed collection.

        """
        return len(self.scopes)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return Entity.getiter(self.scopes)


    def __getitem__(self, key):
        """Returns a child section item.

        """
        return Entity.getitem(self.scopes, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def namespace(self):
        """Returns namespace used in I/O scenarios.

        """
        return self.name
