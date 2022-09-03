import re

from pyessv.constants import PARSING_STRICTNESS_2
from pyessv.constants import PARSING_STRICTNESS_4
from pyessv.constants import IDENTIFIER_TYPE_SET
from pyessv.constants import IDENTIFIER_TYPE_FILENAME
from pyessv.loader import load as load_collection
from pyessv.parsing.identifiers.config import get_config
from pyessv.utils import  compat


def parse_identifer(scope, identifier_type, identifier, strictness=PARSING_STRICTNESS_2):
    """Parses an identifier.

    :param scope: Scope associated with the identifier to be parsed.
    :param identifier_type: Type of parser to be used.
    :param identifier: An identifier to be parsed.
    :param strictness: Strictness level to apply when applying name matching rules.

    """
    assert identifier_type in IDENTIFIER_TYPE_SET, f"Unsupported parser type: {identifier_type}"

    # Set parsing configuration.
    cfg = get_config(scope, identifier_type)

    # Split identifier into a set of elements.
    elements = _get_elements(identifier_type, identifier, cfg.seperator)
    if len(elements) != len(cfg.specs):
        raise ValueError('Invalid identifier. Element count is invalid. Expected={}. Actual={}. Identifier = {}'.format(len(cfg.specs), len(elements), identifier))

    # Strip suffix ... TODO circle back on this.
    if '#' in elements[-1]:
        elements[-1] = elements[-1].split("#")[0]

    # For each identifier element, execute relevant parse. 
    for idx, (element, spec) in enumerate(zip(elements, cfg.specs)):
        # ... constants.
        if spec.startswith("const"):
            expected = spec.split(":")[1]
            if element != expected:
                raise ValueError('Invalid identifier - failed constant check. Element #{} ({}) is invalid. Expected={}. Scope = {}. Identifier={}'.format(idx + 1, element, expected, scope, identifier))

        # ... regular expressions.
        elif spec.startswith("regex"):
            if strictness >= PARSING_STRICTNESS_4:
                element = str(element).strip().lower()
            if re.compile(spec.split(":")[1]).match(element) is None:
                raise ValueError('Invalid identifier - failed regex check. Element #{} ({}) is invalid. Scope = {}. Identifier={}'.format(idx + 1, element, scope, identifier))

        # ... vocabulary collection members.
        else:
            if not load_collection(spec).is_matched(element, strictness):
                raise ValueError('Invalid identifier - failed vocab check. Element #{} ({}) is invalid. Scope = {}. Identifier={}'.format(idx + 1, element, scope, identifier))

def parse_identifer_set(scope, identifier_type, identifier_set, strictness=PARSING_STRICTNESS_2):
    """Parses a collection of identifiers.

    :param scope: Scope associated with the identifier to be parsed.
    :param identifier_type: Type of parser to be used.
    :param identifier_set: A set of identifier to be parsed.
    :param strictness: Strictness level to apply when applying name matching rules.

    """
    assert isinstance(identifier_set, compat.Iterable), 'Invalid identifiers'

    result = set()
    for identifier in identifier_set:
        result = result.union(parse_identifer(scope, identifier_type, identifier, strictness))

    return result

def _get_elements(identifier_type, identifier, seperator):
    """Returns set of elements to be parsed.
    
    """
    elements = identifier.split(seperator)

    # Filenames have a filetype suffix. 
    if identifier_type == IDENTIFIER_TYPE_FILENAME:
        return elements[:-1] + elements[-1].split(".")

    return elements
