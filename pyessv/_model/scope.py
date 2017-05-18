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
        return Node.get_item(self, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority]


    @property
    def hierarchy(self):
        """Gets hierachy within archive.

        """
        return [self.authority, self]


    @property
    def namespace(self):
        """Returns namespace used in I/O scenarios.

        """
        return '{}:{}'.format(self.authority.namespace, self.name)


    @property
    def owner(self):
        """Gets owner within vocabulary model.

        """
        return self.authority


    def parse(self, collection_name, strict=True):
        """Parses an associated collection name.

        """
        return pyessv.parse(collection_name, self, strict=strict)


    def accept(self):
        """Marks node as accepted.

        """
        for collection in self:
            collection.accept()


    def deprecate(self):
        """Marks node as deprecated.

        """
        for collection in self:
            collection.deprecate()


    def destroy(self):
        """Marks node for removal from all persistant state stores.

        """
        for collection in self:
            collection.destroy()


    def reject(self):
        """Marks node as rejected.

        """
        for collection in self:
            collection.reject()


    def reset(self):
        """Resets node status.

        """
        for collection in self:
            collection.reset()
