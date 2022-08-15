from pyessv import io_manager
from pyessv.constants import PARSER_TYPE_SET


# Map: project <-> parser configuration.
_PARSER_CONFIG_CACHE = dict()


def parse_identifer(scope, parser_type, identifier):
    """Parses an identifier.

    :param scope: Scope associated with the identifier to be parsed.
    :param parser_type: Type of parser to be used.
    :param str identifier: An identifier to be parsed.
    :returns: Set of terms deconstructed from the identifier.

    """
    assert parser_type in PARSER_TYPE_SET, f"Unsupported parser type: {parser_type}"

    # Set parser config.
    parser_cfg = _get_parser_config(scope, parser_type)

    print(parser_cfg)

    # Instantiate parser.
    parser = _get_parser(scope, parser_type, parser_cfg)

    # Return parsing result.
    return parser.parse(identifier)


class ParserConfiguration():
    """Encapsulates parsing configuration."""
    def __init__(self, scope_namespace, parser_type, template, collections):
        self.collections = collections
        self.parser_type = parser_type
        self.scope_namespace = scope_namespace
        self.template = template

    @staticmethod
    def create(cfg):
        return ParserConfiguration(
            cfg["scope"],
            cfg["parser_type"],
            cfg["template"],
            cfg["collections"]
        )


def _get_parser_config(scope, parser_type):
    """Returns a parser configuration instance.

    """
    cache_key = f"{scope} :: {parser_type}"
    if cache_key not in _PARSER_CONFIG_CACHE:
        _PARSER_CONFIG_CACHE[cache_key] = \
            ParserConfiguration.create(io_manager.read_scope_parser_config(scope, parser_type))
    
    return _PARSER_CONFIG_CACHE[cache_key]


def _get_parser(scope, parser_type, cfg):
    """Returns a parser instance.

    """
    pass

