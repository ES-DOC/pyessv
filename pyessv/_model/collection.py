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
from pyessv._model.node import Node



class Collection(Node):
    """A vocabulary term collection.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Collection, self).__init__(pyessv.NODE_TYPE_COLLECTION)

        self.scope = None
        self.terms = list()
        self.term_name_regex = None


    def __len__(self):
        """Returns number of terms in managed collection.

        """
        return len(self.terms)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return iter(sorted(self.terms,
                           key=lambda i: i if isinstance(i, basestring) else i.name))


    def __getitem__(self, key):
        """Returns a child section item.

        """
        # Match against key.
        comparator = Node.get_comparator(key)
        for term in self.terms:
            if comparator(term) == key:
                return term

        # Match against a synonym.
        for term in self.terms:
            if key in term.synonyms:
                return term


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


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
