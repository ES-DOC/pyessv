from pyessv import io_manager
from pyessv import loader
from pyessv.model import Scope
from pyessv.utils import compat


# Map: scope:parser-type <-> configuration.
_CACHE = dict()


class ParsingSpecification():
    """Encapsulates parsing specification information declared within configuration.

    """
    def __init__(self, typeof, is_required):
        """Instance initializer.

        :param typeof: Key constraining specification type.
        :param is_required: Flag indicating whether the identifier element must exist.

        """
        self.typeof = typeof
        self.is_required = is_required


class ConstantParsingSpecification(ParsingSpecification):
    """Encapsulates specification information related to a constant element parser.

    """
    def __init__(self, value, is_required):
        """Instance initializer.

        :param value: A constant value that an identifier element must be equivalent to.
        :param is_required: Flag indicating whether the identifier element must exist.

        """
        super(ConstantParsingSpecification, self).__init__("constant", is_required)
        self.value = value

    def __repr__(self):
        """Instance representation.

        """
        return "parser-spec|const::{}::{}".format(self.value, self.is_required)


class CollectionParsingSpecification(ParsingSpecification):
    """Encapsulates specification information related to a term element parser.

    """
    def __init__(self, namespace, is_required):
        """Instance initializer.

        :param namespace: Namespace of a pyessv collection.
        :param is_required: Flag indicating whether the identifier element must exist.

        """
        super(CollectionParsingSpecification, self).__init__("collection", is_required)
        self.namespace = namespace

    def __repr__(self):
        """Instance representation.

        """
        return "parser-spec|collection::{}::{}".format(self.namespace, self.is_required)


class RegExParsingSpecification(ParsingSpecification):
    """Encapsulates specification information related to a regex element parser.

    """
    def __init__(self, expression, is_required):
        """Instance initializer.

        :param expression: A regular expression constraining set of valid elements.
        :param is_required: Flag indicating whether the identifier element must exist.

        """
        super(RegExParsingSpecification, self).__init__("regex", is_required)
        self.expression = expression

    def __repr__(self):
        """Instance representation.

        """
        return "parser-spec|regex::{}::{}".format(self.expression, self.is_required)


class ParsingConfiguration():
    """Encapsulates parsing configuration.

    """
    def __init__(
        self,
        identifier_type,
        scope_namespace,
        template,
        seperator,
        specs,
        suffix
    ):
        """Instance initializer.

        :param scope_namespace: Namespace of scope associated with parser.
        :param identifier_type: Type of parser being used.
        :param template: Template constraining parsing process.
        :param seperator: Seperator isolating slots from each other.
        :param specs: Set of processing instructions when parsing.
        :param suffix: A suffix to be stripped from the identifier when parsing.

        """
        self.identifier_type = identifier_type
        self.scope_namespace = scope_namespace
        self.seperator = seperator
        self.specs = specs
        self.suffix = suffix
        self.template = template

    def __repr__(self):
        """Instance representation.

        """
        return "parser-config|{}::{}::{}".format(self.scope_namespace, self.identifier_type, len(self.specs))


def get_config(scope, identifier_type):
    """Returns a parser configuration instance.

    :param scope: Scope associated with the identifier to be parsed.
    :param identifier_type: Type of parser to be used.
    :returns: Set of terms deconstructed from the identifier.

    """
    if isinstance(scope, compat.basestring):
        scope = loader.load(scope)
    cache_key = "{} :: {}".format(scope, identifier_type)
    if cache_key not in _CACHE:
        _CACHE[cache_key] = _get_config(scope, identifier_type)

    return _CACHE[cache_key]


def _get_config(scope, identifier_type):
    """Encaches a parsing configuration within a simple in-memory cache store.

    """
    cfg = io_manager.read_scope_parser_config(scope, identifier_type)

    return ParsingConfiguration(
        cfg["identifier_type"],
        cfg["scope"],
        cfg["template"],
        cfg["seperator"],
        [_get_spec(i) for i in cfg["specs"]],
        cfg.get("suffix")
    )


def _get_spec(obj):
    """Returns an identifier element validation specification.

    """
    if obj["type"] == "const":
        return ConstantParsingSpecification(
            obj["value"],
            obj["is_required"]
        )
    elif obj["type"] == "collection":
        return CollectionParsingSpecification(
            obj["namespace"],
            obj["is_required"]
        )
    elif obj["type"] == "regex":
        return RegExParsingSpecification(
            obj["expression"],
            obj["is_required"]
        )
    else:
        raise ValueError("Unsupported spec type")
