# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.collection.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary collection, e.g. institute-id.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
from pyessv._model.entity import Entity



class Collection(Entity):
    """A vocabulary term collection.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Collection, self).__init__(pyessv.ENTITY_TYPE_COLLECTION)

        self.scope = None
        self.terms = list()


    def __len__(self):
        """Returns number of terms in managed collection.

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
        return self.scope


    @property
    def authority(self):
        """Gets associated governing authority.

        """
        return self.scope.authority


    def parse(self, term_name, strict=True):
        """Parses an associated term name.

        """
        return pyessv.parse(term_name, self, strict=strict)
