# -*- coding: utf-8 -*-

"""
.. module:: pyessv.model.scope.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary scope, e.g. CMIP6.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.model.entity import Entity



class Scope(Entity):
    """A scope managed by an authority.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.authority = None
        self.collections = list()
        self.create_date = None
        self.description = None
        self.idx = None
        self.label = None
        self.name = None
        self.uid = None
        self.url = None


    def __repr__(self):
        """Instance representation.

        """
        return self.namespace


    def __len__(self):
        """Returns number of items in managed collection.

        """
        return len(self.collections)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return Entity.getiter(self.collections)


    def __getitem__(self, key):
        """Returns a child section item.

        """
        return Entity.getitem(self.collections, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def namespace(self):
        """Returns full namespace of the term set.

        """
        return u":".join([self.authority.name, self.name])


    @property
    def full_idx(self):
        """Gets full computed idx.

        """
        return unicode(self.idx)

