import re

from pyessv import factory
from pyessv.constants import PARSING_STRICTNESS_0
from pyessv.constants import PARSING_STRICTNESS_1
from pyessv.constants import PARSING_STRICTNESS_2
from pyessv.constants import PARSING_STRICTNESS_3
from pyessv.constants import PARSING_STRICTNESS_4
from pyessv.constants import PARSING_STRICTNESS_SET
from pyessv.utils import compat


def match_term(collection, name, strictness=PARSING_STRICTNESS_2):
    """Gets flag indicating whether a matching term can be found.

    :param str name: A term name to be validated.
    :param int strictness: Strictness level to apply when applying name matching rules.

    """
    assert isinstance(name, compat.basestring), \
        'Invalid term name'
    assert strictness in PARSING_STRICTNESS_SET, \
        'Invalid parsing strictness: {}'.format(strictness)

    # Reg-ex match.
    if collection.is_virtual:
        if strictness >= PARSING_STRICTNESS_4:
            name = str(name).strip().lower()
        if re.compile(collection.term_regex).match(name) is not None:
            return factory.create_term(collection, name, append=False)

    # Match by term.
    for term in collection:
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
            names = {term.canonical_name, term.raw_name}.union(set(term.alternative_names))
            if name in names:
                return term

        # match by: all (case-insensitive)
        if strictness == PARSING_STRICTNESS_4:
            name = str(name).strip().lower()
            if name in [i.lower() for i in term.all_names]:
                return term

    return False
