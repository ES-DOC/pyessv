# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.authority.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary authority, e.g. WGCM.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid

from pyessv._constants import NODE_TYPEKEY_AUTHORITY
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._model.node import IterableNode
from pyessv._model.scope import Scope
from pyessv._utils.validation import assert_iterable
from pyessv._utils.validation import assert_regex
from pyessv._utils.validation import assert_string



class Authority(IterableNode):
    """An authority assuming responsibity for governance of vocabularies.

    """
    def __init__(self):
        """Instance constructor.

        """
        self.scopes = []
        super(Authority, self).__init__(self.scopes, NODE_TYPEKEY_AUTHORITY)


    @property
    def ancestors(self):
        """Gets ancestors within archive hierarchy.

        """
        return []


    def get_validators(self):
        """Returns set of validators.

        """
        def _canonical_name():
            assert_string(self.canonical_name)
            assert_regex(self.canonical_name, REGEX_CANONICAL_NAME)

        def _scopes():
            assert_iterable(self.scopes, Scope)

        return super(Authority, self).get_validators() + (
            _canonical_name,
            _scopes
            )
