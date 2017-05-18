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
from pyessv._model.node import Node



class Scope(Node):
    """A scope managed by an authority.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Scope, self).__init__(pyessv.NODE_TYPE_SCOPE)

        self.authority = None
        self.collections = list()


    def __len__(self):
        """Returns number of items in managed collection.

        """
        return len(self.collections)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return iter(sorted(self.collections,
                           key=lambda i: i if isinstance(i, basestring) else i.name))


    def __getitem__(self, key):
        """Returns a child section item.

        """
        # Match against key.
        comparator = Node.get_comparator(key)
        for item in self.collections:
            if comparator(item) == key:
                return item


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority]
