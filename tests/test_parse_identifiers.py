import pytest
import pyessv


def test_parse_dataset_identifiers(dataset_identifiers):
    """Asserts that test identifiers are valid."""
    _assert_valid(pyessv.IDENTIFIER_TYPE_DATASET, dataset_identifiers)

def test_parse_dataset_identifiers_invalid(dataset_identifiers_invalid):
    """Asserts that test identifiers are invalid."""
    _assert_invalid(pyessv.IDENTIFIER_TYPE_DATASET, dataset_identifiers_invalid)

def test_parse_directory_identifiers(directory_identifiers):
    """Asserts that test identifiers are valid."""
    _assert_valid(pyessv.IDENTIFIER_TYPE_DIRECTORY, directory_identifiers)

def test_parse_directory_identifiers_invalid(directory_identifiers_invalid):
    """Asserts that test identifiers are invalid."""
    _assert_invalid(pyessv.IDENTIFIER_TYPE_DIRECTORY, directory_identifiers_invalid)

def test_parse_filename_identifiers(filename_identifiers):
    """Asserts that test identifiers are valid."""
    _assert_valid(pyessv.IDENTIFIER_TYPE_FILENAME, filename_identifiers)

def test_parse_filename_identifiers_invalid(filename_identifiers_invalid):
    """Asserts that test identifiers are invalid."""
    _assert_invalid(pyessv.IDENTIFIER_TYPE_FILENAME, filename_identifiers_invalid)

def _assert_valid(identifier_type, identifiers):
    for scope, identifier in identifiers:
        pyessv.parse_identifer(scope, identifier_type, identifier)

def _assert_invalid(identifier_type, identifiers):
    for scope, identifier in identifiers:
        with pytest.raises(ValueError):
            pyessv.parse_identifer(scope, pyessv.IDENTIFIER_TYPE_DATASET, identifier)
