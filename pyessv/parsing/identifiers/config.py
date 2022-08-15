from pyessv import io_manager
from pyessv import loader


# Map: scope:parser-type <-> configuration.
_CACHE = dict()


class ParsingConfiguration():
    """Encapsulates parsing configuration.
    
    """
    def __init__(self, scope_namespace, identifier_type, template, template_seperator, collection_namespaces):
        """Instance initializer.

        :param scope_namespace: Namespace of scope associated with parser.
        :param identifier_type: Type of parser being used.
        :param template: Template constraining parsing process.
        :param template_seperator: Seperator isolating slots from each other.
        :param collection_namespaces: Set of pyessv collection namespaces to be injected into template.

        """
        # Assert that number of declared collection namespaces == number of slots within template.
        if len(collection_namespaces) != len([i for i in template.split(template_seperator) if i == "{}"]):
            raise ValueError("Parsing configuration error: collection to template mismatch")

        self.collection_namespaces = collection_namespaces
        self.identifier_type = identifier_type
        self.scope_namespace = scope_namespace
        self.template = template
        self.template_seperator = template_seperator
        self.template_slots = template.split(template_seperator)

        # Substitute template slots with appropriate pyessv collection.
        idx_namespace = 0
        for idx_slot, slot in enumerate(self.template_slots):
            if slot == '{}':
                self.template_slots[idx_slot] = _get_collection(collection_namespaces[idx_namespace])
                idx_namespace += 1


    def __repr__(self):
        """Instance representation.
        
        """
        return f"parser-config|{self.scope_namespace}::{self.identifier_type}::{len(self.template_slots)}"


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
            cfg["scope"],
            cfg["identifier_type"],
            cfg["template"],
            cfg["seperator"],
            cfg["collections"]
        )


def _get_collection(namespace):
    """Returns a vocabulary collection.
    
    """
    if namespace in (None, ""):
        raise ValueError(f"Parsing configuration error: invalid pyessv collection {namespace}")

    collection = loader.load(namespace)
    if collection is None:
        raise ValueError(f"Parsing configuration error: invalid pyessv collection {namespace}")

    return collection
