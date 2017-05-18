# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.node.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A node within the pyessv domain model.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

import arrow

from pyessv._constants import NODE_TYPE_AUTHORITY
from pyessv._constants import NODE_TYPE_COLLECTION
from pyessv._constants import NODE_TYPE_SCOPE
from pyessv._constants import NODE_TYPE_TERM
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
from pyessv._utils.formatter import format_io_name



class Node(object):
    """A node within the pyessv domain model.

    """
    def __init__(self, typekey):
        """Instance constructor.

        """
        self.create_date = None
        self.data = None
        self.description = None
        self.label = None
        self.name = None
        self.typekey = typekey
        self.uid = None
        self.url = None


    def __repr__(self):
        """Instance representation.

        """
        return self.namespace


    def validate(self):
        """Validates instance.

        :returns: Set of validation errrors.
        :rtype: set

        """
        # N.B. just-in-time import to avoid circular references.
        from pyessv._validation import validate_node

        return validate_node(self)


    @property
    def errors(self):
        """Returns set of validation errors.

        """
        return sorted(list(self.validate()))


    @property
    def is_valid(self):
        """Gets flag indicating validity.

        """
        return len(self.validate()) == 0


    @property
    def io_name(self):
        """Returns name formatted for I/O operations.

        """
        return format_io_name(self.name)


    @staticmethod
    def get_comparator(key):
        """Returns an item from managed collection.

        """
        if isinstance(key, int):
            return lambda i: i.idx
        elif isinstance(key, uuid.UUID):
            return lambda i: i.uid
        else:
            key = str(key).strip().lower()
            try:
                uuid.UUID(key)
            except ValueError:
                return lambda i: i.name
            else:
                return lambda i: str(i.uid)
