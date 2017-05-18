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


    @property
    def hierarchy(self):
        """Gets hierachy within archive.

        """
        return self.ancestors + [self]


    @property
    def namespace(self):
        """Gets hierachy within archive.

        """
        return ":".join([i.name for i in self.hierarchy])


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
