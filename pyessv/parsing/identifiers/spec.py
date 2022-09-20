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
        return f"parser-spec|const::{self.value}::{self.is_required}"


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
        return f"parser-spec|collection::{self.namespace}::{self.is_required}"


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
        return f"parser-spec|regex::{self.expression}::{self.is_required}"
