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


    def __repr__(self):
        """Instance representation.

        """
        return self.namespace


    def __len__(self):
        """Returns number of terms in managed collection.

        """
        return len(self.terms)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return Entity.getiter(self)


    def __getitem__(self, key):
        """Returns a child section item.

        """
        return Entity.getitem(self, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def authority(self):
        """Gets associated governing authority.

        """
        return self.scope.authority


    @property
    def namespace(self):
        """Gets namespace.

        """
        return ":".join([
            self.scope.namespace,
            self.name,
            ])


    @property
    def full_idx(self):
        """Gets full computed idx.

        """
        return u"{}.{}".format(
            self.scope.idx,
            self.idx
            )


    @property
    def partition(self):
        """Returns associated partition.

        """
        return pyessv.get_partition(self.namespace)


    def parse(self, term, strict=True):
        """Parses an associated term name.

        """
        return pyessv.parse(self.authority, self.scope, self, term, strict=strict)
