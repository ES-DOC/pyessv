import re

from pyessv.constants import PARSING_STRICTNESS_2
from pyessv.constants import PARSING_STRICTNESS_4
from pyessv.constants import IDENTIFIER_TYPE_SET
from pyessv.constants import IDENTIFIER_TYPE_FILENAME
from pyessv.loader import load as load_collection
from pyessv.matcher import match_term
from pyessv.parsing.identifiers.config import get_config
from pyessv.utils import compat


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

    # retrieve optional collection in spec
    all_optional_template_str = re.findall("\[(.+?)\]", cfg.template)
    optional_template_part = [it for sub in [re.findall("%\((\w+)\)s", opt_col) for opt_col in all_optional_template_str] for it in sub]

    # Split identifier into a set of elements.
    elements = _get_elements(identifier_type, identifier, cfg.seperator)
    if len(cfg.specs)-len(optional_template_part) > len(elements) or len(elements) > len(cfg.specs):
        raise ValueError('Invalid identifier. Element count is invalid. Expected={}. Actual={}. Identifier = {}'.format(len(cfg.specs), len(elements), identifier))

    # Strip suffix ...
    if '#' in elements[-1]:
        elements[-1] = elements[-1].split("#")[0]

    result = set()
    # For each identifier element, execute relevant parse.
    for idx, (element, spec) in enumerate(zip(elements, cfg.specs)):
        # ... constants.
        if spec.startswith("const"):
            expected = spec.split(":")[1]
            if element != expected:
                msg = 'Invalid identifier - failed const check. Element=#{}::({}). Identifier={}'
                raise ValueError(msg.format(idx + 1, element, expected, identifier))

        # ... regular expressions.
        elif spec.startswith("regex"):
            if strictness >= PARSING_STRICTNESS_4:
                element = str(element).strip().lower()
            if re.compile(spec.split(":")[1]).match(element) is None:
                msg = 'Invalid identifier - failed regex check. Element=#{}::({}). Identifier={}'
                raise ValueError(msg.format(idx + 1, element, identifier))

        # ... vocabulary collection members.
        else:
            match_result = match_term(load_collection(spec), element, strictness)
            if match_result is False:
                msg = 'Invalid identifier - failed vocab check. Element=#{}::({}). Identifier={}'
                raise ValueError(msg.format(idx + 1, element, identifier))
            result.add(match_result)

    return result


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
        return elements[:-1] + elements[-1].split(".")[:-1]

    return elements
