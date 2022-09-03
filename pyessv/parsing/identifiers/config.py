from pyessv import io_manager
from pyessv import loader


# Map: scope:parser-type <-> configuration.
_CACHE = dict()


class ParsingConfiguration():
    """Encapsulates parsing configuration.
    
    """
    def __init__(
        self, 
        identifier_type,
        scope_namespace,
        template,
        seperator,
        specs
        ):
        """Instance initializer.

        :param scope_namespace: Namespace of scope associated with parser.
        :param identifier_type: Type of parser being used.
        :param template: Template constraining parsing process.
        :param seperator: Seperator isolating slots from each other.
        :param specs: Set of processing instructions when parsing.

        """
        self.identifier_type = identifier_type
        self.scope_namespace = scope_namespace
        self.seperator = seperator
        self.specs = specs
        self.template = template

    def __repr__(self):
        """Instance representation.
        
        """
        return f"parser-config|{self.scope_namespace}::{self.identifier_type}::{len(self.specs)}"


def get_config(scope, identifier_type):
    """Returns a parser configuration instance.

    :param scope: Scope associated with the identifier to be parsed.
    :param identifier_type: Type of parser to be used.
    :returns: Set of terms deconstructed from the identifier.

    """
    cache_key = f"{scope} :: {identifier_type}"
    if cache_key not in _CACHE:
        _encache(cache_key, scope, identifier_type)
    
    return _CACHE[cache_key]


def _encache(cache_key, scope, identifier_type):
    """Encaches a parsing configuration within a simple in-memory cache store.
    
    """
    cfg = io_manager.read_scope_parser_config(scope, identifier_type)

    _CACHE[cache_key] = \
        ParsingConfiguration(
            cfg["identifier_type"],
            cfg["scope"],
            cfg["template"],
            cfg["seperator"],
            cfg["specs"]
        )
