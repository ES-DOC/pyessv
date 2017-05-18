# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.authority.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary authority, e.g. WGCM.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
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
        return Node.get_item(self, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return []


    @property
    def hierarchy(self):
        """Gets hierachy within archive.

        """
        return [self]


    @property
    def namespace(self):
        """Returns namespace used in I/O scenarios.

        """
        return self.name


    def parse(self, scope_name, strict=True):
        """Parses an associated scope name.

        """
        return pyessv.parse(scope_name, self, strict=strict)


    def accept(self):
        """Marks node as accepted.

        """
        for scope in self:
            scope.accept()


    def deprecate(self):
        """Marks node as deprecated.

        """
        for scope in self:
            scope.deprecate()


    def destroy(self):
        """Marks node for removal from all persistant state stores.

        """
        for scope in self:
            scope.destroy()


    def reject(self):
        """Marks node as rejected.

        """
        for scope in self:
            scope.reject()


    def reset(self):
        """Resets node status.

        """
        for scope in self:
            scope.reset()
