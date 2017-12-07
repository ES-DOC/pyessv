# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.term.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary term, e.g. IPSL.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._constants import GOVERNANCE_STATUS_PENDING
from pyessv._constants import GOVERNANCE_STATUS_SET
from pyessv._constants import NODE_TYPEKEY_TERM
from pyessv._model.node import Node
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
from pyessv._utils.validation import assert_regex
from pyessv._utils.validation import assert_string



class Term(Node):
    """A vocabulary term.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Term, self).__init__(NODE_TYPEKEY_TERM)

        self.associations = list()
        self.collection = None
        self.parent = None
        self.status = GOVERNANCE_STATUS_PENDING


    def __contains__(self, key):
        """Instance membership predicate.

        """
        key = str(key).strip().lower()

        return key in self.all_names


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority, self.scope, self.collection]


    @property
    def authority(self):
        """Gets governing authority.

        """
        return self.scope.authority


    @property
    def scope(self):
        """Gets governing scope.

        """
        return self.collection.scope


    def get_validators(self):
        """Returns set of validators.

        """
        from pyessv._model.scope import Collection

        def _canonical_name():
            assert_string(self.canonical_name)
            if isinstance(self.collection.term_regex, basestring):
                assert_regex(self.canonical_name, self.collection.term_regex)

        def _collection():
            assert isinstance(self.collection, Collection)

        def _parent():
            if self.parent is not None:
                assert isinstance(self.parent, Term)

        def _status():
            assert self.status in GOVERNANCE_STATUS_SET

        return super(Term, self).get_validators() + (
            _collection,
            _canonical_name,
            _parent,
            _status,
            )
