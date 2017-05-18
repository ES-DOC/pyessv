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
from pyessv._model.node import Node



class Authority(Node):
    """An authority assuming responsibity for governance of vocabularies.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Authority, self).__init__(pyessv.NODE_TYPE_AUTHORITY)

        self.scopes = list()


    def __len__(self):
        """Returns number of items in managed collection.

        """
        return len(self.scopes)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return iter(sorted(self.scopes,
                           key=lambda i: i if isinstance(i, basestring) else i.name))


    def __getitem__(self, key):
        """Returns a child section item.

        """
        # Match against key.
        comparator = Node.get_comparator(key)
        for item in self.scopes:
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
        return []
