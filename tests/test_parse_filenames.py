import pytest
import pyessv


def test_parse_filename_formats(filename_identifiers):
    """Asserts that test identifiers are valid."""
    for scope, identifier in filename_identifiers:
        pyessv.parse_identifer(scope, pyessv.IDENTIFIER_TYPE_FILENAME, identifier)


def test_parse_filename_formats_invalid(filename_identifiers_invalid):
    """Asserts that test identifiers are invalid."""
    for scope, identifier in filename_identifiers_invalid:
        with pytest.raises(ValueError):
            pyessv.parse_identifer(scope, pyessv.IDENTIFIER_TYPE_FILENAME, identifier)
