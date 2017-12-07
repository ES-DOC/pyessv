# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.scope.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary scope, e.g. CMIP6.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

from pyessv._constants import NODE_TYPEKEY_SCOPE
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._model.collection import Collection
from pyessv._model.node import IterableNode
from pyessv._utils.validation import assert_iterable
from pyessv._utils.validation import assert_regex
from pyessv._utils.validation import assert_string



class Scope(IterableNode):
    """A scope managed by an authority.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.authority = None
        self.collections = []
        super(Scope, self).__init__(self.collections, NODE_TYPEKEY_SCOPE)


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return [self.authority]


    def get_validators(self):
        """Returns set of validators.

        """
        from pyessv._model.authority import Authority

        def _authority():
            assert isinstance(self.authority, Authority)

        def _canonical_name():
            assert_string(self.canonical_name)
            assert_regex(self.canonical_name, REGEX_CANONICAL_NAME)

        def _collections():
            assert_iterable(self.collections, Collection)

        return super(Scope, self).get_validators() + (
            _authority,
            _canonical_name,
            _collections
            )
