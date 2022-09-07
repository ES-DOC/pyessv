class NamespaceParsingError(ValueError):
    """A parsing error raised by the package parser.

    """
    def __init__(self, typeof, name):
        """Object constructor.

        """
        msg = 'Parsing error: typeof={}, name={}'.format(typeof, name)
        super(NamespaceParsingError, self).__init__(msg)


class ValidationError(ValueError):
    """A validation error raised by the package validator.

    """
    def __init__(self, msg):
        """Object constructor.

        """
        super(ValidationError, self).__init__(msg)


class InvalidAssociationError(ValueError):
    """An error raised an invalid association is declared.

    """
    def __init__(self, association):
        """Object constructor.

        """
        msg = 'Unsupported association: {}'.format(association)
        super(InvalidAssociationError, self).__init__(msg)
