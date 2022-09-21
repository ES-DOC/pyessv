import json
import os
import pathlib
import typing

import pytest
import pyessv


# Path to test assets folder.
_ASSETS: pathlib.Path = pathlib.Path(os.path.dirname(__file__)).parent / "assets" / "identifiers"


@pytest.fixture(scope="session")
def dataset_identifiers() -> typing.Tuple[pyessv.Scope, str]:
    return list(_yield_identifiers(pyessv.IDENTIFIER_TYPE_DATASET))


@pytest.fixture(scope="session")
def dataset_identifiers_invalid() -> typing.Tuple[pyessv.Scope, str]:
    return list(_yield_identifiers_invalid(pyessv.IDENTIFIER_TYPE_DATASET))


@pytest.fixture(scope="session")
def directory_identifiers() -> typing.Tuple[pyessv.Scope, str]:
    return list(_yield_identifiers(pyessv.IDENTIFIER_TYPE_DIRECTORY))


@pytest.fixture(scope="session")
def directory_identifiers_invalid() -> typing.Tuple[pyessv.Scope, str]:
    return list(_yield_identifiers_invalid(pyessv.IDENTIFIER_TYPE_DIRECTORY))


@pytest.fixture(scope="session")
def filename_identifiers() -> typing.Tuple[pyessv.Scope, str]:
    return list(_yield_identifiers(pyessv.IDENTIFIER_TYPE_FILENAME))


@pytest.fixture(scope="session")
def filename_identifiers_invalid() -> typing.Tuple[pyessv.Scope, str]:
    return list(_yield_identifiers_invalid(pyessv.IDENTIFIER_TYPE_FILENAME))


def _yield_identifiers(identifier_type: str) -> typing.Iterator[typing.Tuple[pyessv.Scope, str]]:
    fpath: pathlib.Path = _ASSETS
    if not fpath.exists():
        return []

    for fpath in _ASSETS.glob(f"{identifier_type}_*.json"):
        with open(fpath, "r") as fstream:
            fixture: dict = json.loads(fstream.read())

        scope = pyessv.load(fixture["scope"])
        for identifier in [i for i in fixture["identifiers"] if i]:
            yield scope, identifier


def _yield_identifiers_invalid(identifier_type: str):
    for scope, identifier in _yield_identifiers(identifier_type):
        elements = identifier.split(".")

        # Invalid: too few elements.
        yield scope, ".".join(elements[1:])

        # Invalid: invalid element.
        for idx in range(len(elements)):
            new_parts = list(elements)
            new_parts[idx] = 'X!X!X!X!'
            yield scope, ".".join(new_parts)
