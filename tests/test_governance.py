import pytest

import pyessv
import tests.utils as tu


def yield_parameterizations():
    """Test parameterizations.

    """
    for func, status in (
        (pyessv.accept, pyessv.GOVERNANCE_STATUS_ACCEPTED),
        (pyessv.reject, pyessv.GOVERNANCE_STATUS_REJECTED),
        (pyessv.reset, pyessv.GOVERNANCE_STATUS_PENDING),
        (pyessv.deprecate, pyessv.GOVERNANCE_STATUS_DEPRECATED)
    ):
        yield func, status


@pytest.mark.parametrize("action, expected_status", yield_parameterizations())
def test_governance(action, expected_status):
    """Performs governance tests.

    """
    tu.create_test_entities()

    term = tu.create_term_01()
    tu.assert_str(term.status, pyessv.GOVERNANCE_STATUS_PENDING)
    action(term)
    tu.assert_str(term.status, expected_status)

    tu.teardown()
