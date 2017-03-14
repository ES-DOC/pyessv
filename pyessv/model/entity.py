# -*- coding: utf-8 -*-

"""
.. module:: pyessv.model.entity.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: An entity within the pyessv domain model.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

from pyessv.constants import ENCODING_DICT
from pyessv.constants import ENCODING_JSON



class Entity(object):
    """An entity within the pyessv domain model.

    """
    def validate(self):
        """Validates instance.

        :returns: Set of validation errrors.
        :rtype: set

        """
        # N.B. just-in-time import to avaoid circular references.
        from pyessv import validation as v

        return v.validate(self)


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


    @property
    def as_dict(self):
        """Returns dictionary representation of term.

        """
        return pyessv.encode(self, ENCODING_DICT)


    @property
    def as_json(self):
        """Returns json representation of term.

        """
        return pyessv.encode(self, ENCODING_JSON)


    @classmethod
    def from_json(cls, encoded):
        """Returns json representation of term.

        """
        return pyessv.decode(encoded, ENCODING_JSON)


    @staticmethod
    def getiter(items):
        """Returns an iterator over a managed collection.

        """
        return iter(sorted(items, key=lambda i: i if isinstance(i, (str, unicode)) else i.name))


    @staticmethod
    def getitem(items, key):
        """Returns an item from a managed collections.

        """
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

        # Return first matching item.
        for item in items:
            if comparator(item) == key:
                return item

