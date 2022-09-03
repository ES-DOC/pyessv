import pytest
import pyessv


def test_parse_dataset_identifiers(dataset_identifiers):
    """Asserts that test identifiers are valid."""
    for scope, identifier in dataset_identifiers:
        print(111, identifier)
        pyessv.parse_identifer(scope, pyessv.IDENTIFIER_TYPE_DATASET_ID, identifier)


def test_parse_dataset_identifiers_invalid(dataset_identifiers_invalid):
    """Asserts that test identifiers are invalid."""
    for scope, identifier in dataset_identifiers_invalid:
        with pytest.raises(ValueError):
            pyessv.parse_identifer(scope, pyessv.IDENTIFIER_TYPE_DATASET_ID, identifier)
