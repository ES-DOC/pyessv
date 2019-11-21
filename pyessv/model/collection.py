"""
.. module:: pyessv.model.collection.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary collection, e.g. institute-id.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import re

from pyessv.constants import NODE_TYPEKEY_COLLECTION
from pyessv.constants import PARSING_STRICTNESS_0
from pyessv.constants import PARSING_STRICTNESS_1
from pyessv.constants import PARSING_STRICTNESS_2
from pyessv.constants import PARSING_STRICTNESS_3
from pyessv.constants import PARSING_STRICTNESS_4
from pyessv.constants import PARSING_STRICTNESS_SET
from pyessv.constants import REGEX_CANONICAL_NAME
from pyessv.model.node import IterableNode
from pyessv.model.term import Term
from pyessv.utils import compat
from pyessv.utils.validation import assert_iterable
from pyessv.utils.validation import assert_namespace
from pyessv.utils.validation import assert_regex
from pyessv.utils.validation import assert_string


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


    @property
    def is_virtual(self):
        """Gets flag indicating whether the collection is a virtual one (i.e. simply constrained by a reg-ex).

        """
        return len(self) == 0


    def get_validators(self):
        """Returns set of validators.

        """
        from pyessv.model.scope import Scope

        def _canonical_name():
            assert_string(self.canonical_name)
            assert_regex(self.canonical_name, REGEX_CANONICAL_NAME)

        def _scope():
            assert isinstance(self.scope, Scope)

        def _term_regex():
            assert isinstance(self.term_regex, (compat.basestring, tuple))
            if isinstance(self.term_regex, compat.basestring):
                assert_string(self.term_regex)
            else:
                assert_iterable(self.term_regex, compat.basestring, tuple)
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


    def is_matched(self, name, strictness=PARSING_STRICTNESS_2):
        """Gets flag indicating whether a matching term can be found.

        :param str name: A term name to be validated.
        :param int strictness: Strictness level to apply when applying name matching rules.

        """
        assert isinstance(name, compat.basestring), 'Invalid term name'
        assert strictness in PARSING_STRICTNESS_SET, 'Invalid parsing strictness: {}'.format(strictness)

        # Reg-ex match.
        if self.is_virtual:
            if strictness >= PARSING_STRICTNESS_4:
                name = str(name).strip().lower()
            return re.compile(self.term_regex).match(name) is not None

        # Match by term.
        for term in self:
            # match by: canonical_name
            if strictness == PARSING_STRICTNESS_0:
                if name == term.canonical_name:
                    return term

            # match by: raw_name
            elif strictness == PARSING_STRICTNESS_1:
                if name == term.raw_name:
                    return term

            # match by: canonical_name | raw_name
            elif strictness == PARSING_STRICTNESS_2:
                if name in {term.canonical_name, term.raw_name}:
                    return term

            # match by: alternative_name
            if strictness == PARSING_STRICTNESS_3:
                if name in {term.canonical_name, term.raw_name}.union(set(term.alternative_names)):
                    return term

            # match by: all (case-insensitive)
            if strictness == PARSING_STRICTNESS_4:
                name = str(name).strip().lower()
                if name in [i.lower() for i in term.all_names]:
                    return term

        return False
