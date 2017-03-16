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



class Entity(object):
    """An entity within the pyessv domain model.

    """
    def validate(self):
        """Validates instance.

        :returns: Set of validation errrors.
        :rtype: set

        """
        # N.B. just-in-time import to avoid circular references.
        from pyessv._validation import validate

        return validate(self)


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
    def getcollection(entity):
        """Returns associated managed collection.

        """
        if entity.typeof == ENTITY_TYPE_AUTHORITY:
            return entity.scopes
        elif entity.typeof == ENTITY_TYPE_COLLECTION:
            return entity.terms
        elif entity.typeof == ENTITY_TYPE_SCOPE:
            return entity.collections


    @staticmethod
    def getiter(entity):
        """Returns an iterator over managed collection.

        """
        items = Entity.getcollection(entity)

        return iter(sorted(items, key=lambda i: i if isinstance(i, (str, unicode)) else i.name))


    @staticmethod
    def getitem(entity, key):
        """Returns an item from managed collection.

        """
        items = Entity.getcollection(entity)

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
        if entity.typeof == ENTITY_TYPE_COLLECTION:
            for item in [i for i in items if i.synonyms]:
                if key in item.synonyms:
                    return item
