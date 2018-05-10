# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.node.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A node within the pyessv domain model.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime
import uuid

import arrow

from pyessv._constants import NODE_TYPEKEY_SET
from pyessv._utils.compat import str
from pyessv._utils.formatter import format_io_name
from pyessv._utils.validation import assert_iterable
from pyessv._utils.validation import assert_string
from pyessv._utils.validation import assert_url


class Node(object):
    """A node within the pyessv domain model.

    """
    def __init__(self, typekey):
        """Instance constructor.

        """
        self.canonical_name = None
        self.create_date = None
        self.data = None
        self.description = None
        self.label = None
        self.raw_name = None
        self.alternative_names = list()
        self.typekey = typekey
        self.uid = None
        self.url = None


    def __repr__(self):
        """Instance representation.

        """
        return self.namespace


    def __getattr__(self, name):
        """Instance attribute getter.

        """
        try:
            return self.data[name]
        except KeyError:
            try:
                return self.data[name.replace('_', '-')]
            except KeyError:
                raise AttributeError('{} unknown attribute'.format(name))


    @property
    def name(self):
        """Helper attribute to return canonical_name.

        """
        return self.canonical_name


    @property
    def all_names(self):
        """Returns all term names.

        """
        result = [self.canonical_name, self.raw_name] + self.alternative_names
        result = [t for t in result if t is not None and len(t) > 0]

        return set(sorted(result))


    @property
    def hierarchy(self):
        """Gets hierachy within archive.

        """
        return self.ancestors + [self]


    @property
    def namespace(self):
        """Gets hierachy within archive.

        """
        return ":".join([i.canonical_name for i in self.hierarchy])


    @property
    def io_name(self):
        """Returns name formatted for I/O operations.

        """
        return format_io_name(self.canonical_name)


    def get_validators(self):
        """Returns set of validators.

        """
        def _alternative_names():
            assert_iterable(self.alternative_names, assert_string)

        def _create_date():
            assert isinstance(self.create_date, datetime.datetime)

        def _data():
            if self.data is not None:
                assert isinstance(self.data, dict)

        def _description():
            if isinstance(self, IterableNode):
                assert_string(self.description)
            elif self.description is not None:
                assert_string(self.description)

        def _label():
            if self.label is not None:
                assert_string(self.label)

        def _typekey():
            assert self.typekey in NODE_TYPEKEY_SET

        def _uid():
            assert isinstance(self.uid, uuid.UUID)

        def _url():
            if self.url is not None:
                assert_url(self.url)

        return (
            _alternative_names,
            _create_date,
            _data,
            _description,
            _label,
            _typekey,
            _uid,
            _url
            )


    @staticmethod
    def get_comparator(key):
        """Returns an item from managed collection.

        """
        if isinstance(key, uuid.UUID):
            return lambda i: i.uid
        else:
            key = str(key).strip().lower()
            try:
                uuid.UUID(key)
            except ValueError:
                return lambda i: i.canonical_name
            else:
                return lambda i: str(i.uid)


class IterableNode(Node):
    """An iterable node within the pyessv domain model.

    """
    def __init__(self, items, typekey):
        """Instance constructor.

        """
        self._items = items
        super(IterableNode, self).__init__(typekey)


    def __add__(self, other):
        """Add operator.

        """
        return self._items + other._items


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    def __getattr__(self, name):
        """Instance attribute getter.

        """
        try:
            return self[name.lower().replace('_', '-')]
        except KeyError:
            raise AttributeError('{} unknown attribute'.format(name))


    def __getitem__(self, key):
        """Returns a child section item.

        """
        # Match against a uid | canonical name.
        comparator = Node.get_comparator(key)
        for item in self:
            if comparator(item) == key:
                return item

        # Match against a raw name.
        for item in self:
            if key == item.raw_name:
                return item

        # Match against an alternative name.
        for item in self:
            if key in item.alternative_names:
                return item


    def __iter__(self):
        """Instance iterator initializer.

        """
        return iter(sorted(self._items,
                           key=lambda i: i if isinstance(i, basestring) else i.canonical_name))


    def __len__(self):
        """Returns number of items in managed collection.

        """
        return len(self._items)
