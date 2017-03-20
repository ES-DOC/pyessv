# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.entity.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: An entity within the pyessv domain model.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

from pyessv._constants import ENTITY_TYPE_AUTHORITY
from pyessv._constants import ENTITY_TYPE_COLLECTION
from pyessv._constants import ENTITY_TYPE_SCOPE
from pyessv._constants import ENTITY_TYPE_TERM


class Entity(object):
    """An entity within the pyessv domain model.

    """
    def __init__(self, typeof):
        """Instance constructor.

        """
        self.create_date = None
        self.data = None
        self.description = None
        self.idx = None
        self.io_path = None
        self.label = None
        self.name = None
        self.status = None
        self.typeof = typeof
        self.url = None
        self.uid = None


    def __repr__(self):
        """Instance representation.

        """
        return self.namespace


    @property
    def namespace(self):
        """Gets namespace.

        """
        return Entity.get_namespace(self)


    def validate(self):
        """Validates instance.

        :returns: Set of validation errrors.
        :rtype: set

        """
        # N.B. just-in-time import to avoid circular references.
        from pyessv._validation import validate_entity

        return validate_entity(self)


    @property
    def errors(self):
        """Returns set of validation errors.

        """
        return sorted(list(self.validate()))


    @property
    def is_valid(self):
        """Gets flag indicating validity status.

        """
        return len(self.validate()) == 0


    @staticmethod
    def get_namespace(entity):
        """Returns namespace used in I/O scenarios.

        """
        return u":".join([i.name for i in Entity.get_hierarchy(entity)])


    @staticmethod
    def get_hierarchy(entity):
        """Returns an entity's hierachy within the archive.

        """
        if entity.typeof == ENTITY_TYPE_AUTHORITY:
            hierachy = []
        elif entity.typeof == ENTITY_TYPE_SCOPE:
            hierachy = Entity.get_hierarchy(entity.authority)
        elif entity.typeof == ENTITY_TYPE_COLLECTION:
            hierachy = Entity.get_hierarchy(entity.scope)
        elif entity.typeof == ENTITY_TYPE_TERM:
            hierachy = Entity.get_hierarchy(entity.collection)
        hierachy.append(entity)

        return hierachy


    @staticmethod
    def get_ancestors(entity):
        """Returns an entity's ancestors within the archive.

        """
        return Entity.get_hierarchy(entity)[0:-1]


    @staticmethod
    def get_ancestor(entity):
        """Returns an entity's ancestor within the archive.

        """
        try:
            return Entity.get_ancestors(entity)[-1]
        except IndexError:
            pass


    @staticmethod
    def get_collection(entity):
        """Returns associated managed collection.

        """
        if entity.typeof == ENTITY_TYPE_AUTHORITY:
            return entity.scopes
        elif entity.typeof == ENTITY_TYPE_COLLECTION:
            return entity.terms
        elif entity.typeof == ENTITY_TYPE_SCOPE:
            return entity.collections
        elif entity.typeof == ENTITY_TYPE_TERM:
            raise NotImplementedError()


    @staticmethod
    def get_count(entity):
        """Returns associated managed collection count.

        """
        return len(Entity.get_collection(entity))


    @staticmethod
    def get_iter(entity):
        """Returns an iterator over managed collection.

        """
        items = Entity.get_collection(entity)

        return iter(sorted(items, key=lambda i: i if isinstance(i, (str, unicode)) else i.name))


    @staticmethod
    def get_item(entity, key):
        """Returns an item from managed collection.

        """
        items = Entity.get_collection(entity)

        # Set comparator to be used.
        if isinstance(key, int):
            comparator = lambda i: i.idx
        elif isinstance(key, uuid.UUID):
            comparator = lambda i: i.uid
        else:
            key = unicode(key).strip().lower()
            try:
                uuid.UUID(key)
            except ValueError:
                comparator = lambda i: i.name
            else:
                comparator = lambda i: unicode(i.uid)

        # Match against a attribute.
        for item in items:
            if comparator(item) == key:
                return item

        # Match against a synonym.
        try:
            items = [i for i in items if i.synonyms]
        except AttributeError:
            pass
        else:
            for item in items:
                if key in item.synonyms:
                    return item
