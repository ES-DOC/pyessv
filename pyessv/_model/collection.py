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
        return Entity.get_item(self, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    @property
    def hierarchy(self):
        """Gets hierachy within archive.

        """
        return [self.authority, self.scope, self]


    @property
    def namespace(self):
        """Returns namespace used in I/O scenarios.

        """
        return '{}:{}'.format(self.scope.namespace, self.name)


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority, self.scope]


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


    def accept(self):
        """Marks entity as accepted.

        """
        for term in self:
            term.accept()


    def deprecate(self):
        """Marks entity as deprecated.

        """
        for term in self:
            term.deprecate()


    def destroy(self):
        """Marks entity for removal from all persistant state stores.

        """
        for term in self:
            term.destroy()


    def reject(self):
        """Marks entity as rejected.

        """
        for term in self:
            term.reject()


    def reset(self):
        """Resets entity status.

        """
        for term in self:
            term.reset()
