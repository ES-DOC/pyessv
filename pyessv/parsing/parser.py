from pyessv.constants import PARSING_STRICTNESS_1
from pyessv.constants import PARSER_TYPE_SET
from pyessv.parsing.config import get_config


def parse_identifer(scope, parser_type, identifier, strictness=PARSING_STRICTNESS_1):
    """Parses an identifier.

    :param scope: Scope associated with the identifier to be parsed.
    :param parser_type: Type of parser to be used.
    :param str identifier: An identifier to be parsed.
    :param int strictness: Strictness level to apply when applying name matching rules.
    :returns: Set of terms deconstructed from the identifier.

    """
    assert parser_type in PARSER_TYPE_SET, f"Unsupported parser type: {parser_type}"

    # Set parser config.
    parser_cfg = get_config(scope, parser_type)
    print(parser_cfg)

    # Instantiate parser.
    parser = _get_parser(scope, parser_type, parser_cfg)

    # Return parsing result.
    return parser.parse(identifier)
