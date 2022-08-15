from pyessv.constants import PARSING_STRICTNESS_2
from pyessv.constants import PARSER_TYPE_SET
from pyessv.parsing.config import get_config
from pyessv.utils import  compat


def parse_identifer(scope, parser_type, identifier, strictness=PARSING_STRICTNESS_2):
    """Parses an identifier.

    :param scope: Scope associated with the identifier to be parsed.
    :param parser_type: Type of parser to be used.
    :param identifier: An identifier to be parsed.
    :param strictness: Strictness level to apply when applying name matching rules.

    """
    assert parser_type in PARSER_TYPE_SET, f"Unsupported parser type: {parser_type}"

    # Set parser config.
    cfg = get_config(scope, parser_type)

    # Split identifier into a set of elements.
    elements = identifier.split(cfg.template_seperator)

    # Strip identifier version suffix.
    if '#' in elements[-1]:
        elements[-1] = elements[-1].split("#")[0]

    # Execute validators.
    _validate_step_01(identifier, elements, cfg.template_slots)
    _validate_step_02(identifier, elements, cfg.template_slots, strictness)


def parse_identifer_set(scope, parser_type, identifier_set, strictness=PARSING_STRICTNESS_2):
    """Parses a collection of identifiers.

    :param scope: Scope associated with the identifier to be parsed.
    :param parser_type: Type of parser to be used.
    :param identifier_set: A set of identifier to be parsed.
    :param strictness: Strictness level to apply when applying name matching rules.

    """
    assert isinstance(identifier_set, compat.Iterable), 'Invalid identifiers'

    result = set()
    for identifier in identifier_set:
        result = result.union(parse_identifer(scope, parser_type, identifier, strictness))

    return result


def _validate_step_01(identifier, elements, slots):
    """Validates that length of identifier elements is equivalent to length of template slots.
    
    """
    if len(elements) != len(slots):
        raise ValueError('Invalid identifier: {}: Number of elements is {}, expected {}'.format(identifier, len(elements), len(slots)))


def _validate_step_02(identifier, elements, slots, strictness):
    """Validates the set of identifier elements against the set of template slots.
    
    """
    # Iterate each identifier element & validate accordingly.
    for idx, element in enumerate(elements):
        # Set validation slot associated with element being validated.
        slot = slots[idx]

        # Validate element against a constant.
        if isinstance(slot, compat.basestring):
            if element != slot:
                raise ValueError(f"Invalid identifier :: element = {element} :: identifier = {identifier}")

        # Validate element against a vocabulary collection.
        else:
            term = slot.is_matched(element, strictness=strictness)
            if term == False:
                raise ValueError(f"Invalid identifier :: element = {element} :: identifier = {identifier}")
