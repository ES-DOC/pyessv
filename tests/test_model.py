import pytest

import tests.utils as tu


# Module level fixture teardown.
teardown_module = tu.teardown


def _yield_parameterizations():
    """Test parameterizations.

    """
    for node_factory, keys in (
        (tu.create_authority, [tu.SCOPE_NAME]),
        (tu.create_scope, [tu.COLLECTION_01_NAME, tu.COLLECTION_02_NAME, tu.COLLECTION_03_NAME]),
        (tu.create_collection_01, [tu.TERM_01_NAME]),
        (tu.create_collection_02, [tu.TERM_02_NAME]),
        (tu.create_collection_03, [tu.TERM_03_NAME]),
    ):
        yield node_factory(), keys


@pytest.mark.parametrize("node, keys", _yield_parameterizations())
def test_iterability(node, keys):
    """Test iterability of domain model.

    """
    assert iter(node)
    assert len(node) == len(keys)
    for key in keys:
        assert key in node
        assert node[key] is not None
