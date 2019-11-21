"""
.. module:: pyessv.model.authority.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary authority, e.g. WGCM.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.constants import NODE_TYPEKEY_AUTHORITY
from pyessv.constants import REGEX_CANONICAL_NAME
from pyessv.model.node import IterableNode
from pyessv.model.scope import Scope
from pyessv.utils.validation import assert_iterable
from pyessv.utils.validation import assert_regex
from pyessv.utils.validation import assert_string



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
