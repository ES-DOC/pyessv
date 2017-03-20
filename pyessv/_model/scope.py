# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.scope.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary scope, e.g. CMIP6.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
from pyessv._model.entity import Entity



class Scope(Entity):
    """A scope managed by an authority.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Scope, self).__init__(pyessv.ENTITY_TYPE_SCOPE)

        self.authority = None
        self.collections = list()


    def __len__(self):
        """Returns number of items in managed collection.

        """
        return Entity.get_count(self)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return Entity.get_iter(self)


    def __getitem__(self, key):
        """Returns a child section item.

        """
        return Entity.get_item(self, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def owner(self):
        """Gets owner within vocabulary model.

        """
        return self.authority


    @property
    def full_idx(self):
        """Gets full computed idx.

        """
        return unicode(self.idx)


    def parse(self, collection_name, strict=True):
        """Parses an associated collection name.

        """
        return pyessv.parse(collection_name, self, strict=strict)
