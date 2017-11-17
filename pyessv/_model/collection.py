# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.collection.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary collection, e.g. institute-id.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import re
import uuid

import pyessv
from pyessv._constants import NODE_TYPEKEY_COLLECTION
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._model.node import IterableNode
from pyessv._model.term import Term
from pyessv._utils.compat import basestring
from pyessv._utils.validation import assert_iterable
from pyessv._utils.validation import assert_namespace
from pyessv._utils.validation import assert_regex
from pyessv._utils.validation import assert_string


class Collection(IterableNode):
    """A vocabulary term collection.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.scope = None
        self.terms = []
        self.term_regex = None
        super(Collection, self).__init__(self.terms, NODE_TYPEKEY_COLLECTION)


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority, self.scope]


    @property
    def authority(self):
        """Gets governing authority.

        """
        return self.scope.authority


    def get_validators(self):
        """Returns set of validators.

        """
        from pyessv._model.scope import Scope

        def _canonical_name():
            assert_string(self.canonical_name)
            assert_regex(self.canonical_name, REGEX_CANONICAL_NAME)

        def _scope():
            assert isinstance(self.scope, Scope)

        def _term_regex():
            assert isinstance(self.term_regex, (basestring, tuple))
            if isinstance(self.term_regex, basestring):
                assert_string(self.term_regex)
            else:
                assert_iterable(self.term_regex, basestring, tuple)
                assert len(self.term_regex) > 1
                assert self.term_regex[0].count('{}') == (len(self.term_regex) - 1)
                for identifier in self.term_regex[1:]:
                    assert_namespace(identifier, min_length=3, max_length=4)

        def _terms():
            assert_iterable(self.terms, Term)

        return super(Collection, self).get_validators() + (
            _canonical_name,
            _scope,
            _term_regex,
            _terms
            )


    def is_matched(self, name, field='canonical_name'):
        """Gets flag indicating whether a matching term can be found.

        :param str name: A term name to be validated.
        :param str field: Term attribute to be used for comparison.

        """
        assert isinstance(name, basestring), 'Invalid term name'
        assert field in ('canonical_name', 'raw_name', 'label'), 'Invalid term attribute'

        # Regular expression match.
        if len(self) == 0:
            return re.compile(self.term_regex).match(name) is not None

        # Attribute match.
        for term in self:
            if getattr(term, field) == name:
                return True

        return False


    @staticmethod
    def get_info(identifier, default_field='canonical_name'):
        """Returns collection reference information.

        """
        assert isinstance(identifier, basestring), 'Invalid collection identifier'
        identifier = identifier.split(':')
        assert len(identifier) in (3, 4), 'Invalid collection identifier'

        field = default_field if len(identifier) == 3 else identifier[-1]
        assert field in ('canonical_name', 'raw_name', 'label'), 'Invalid term field'

        identifier = ':'.join(identifier[0:3])
        collection = pyessv.load(identifier)
        assert isinstance(collection, Collection), 'Invalid collection identifier: {}'.format(identifier)

        return collection, field

