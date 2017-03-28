# -*- coding: utf-8 -*-

"""
.. module:: test_governance.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv governance tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pyessv

import nose

import tests.utils as tu



@nose.with_setup(tu.setup_and_create_term, tu.teardown)
def _test(governance_action, governance_status):
    """Performs governance tests.

    """
    term = tu.get_term()
    tu.assert_str(term.status, pyessv.GOVERNANCE_STATUS_PENDING)
    governance_action(term)
    tu.assert_str(term.status, governance_status)
    pyessv.save(term)

    tu.setup()
    term = tu.get_term()
    tu.assert_str(term.status, governance_status)


def test():
    """pyessv-tests: governance: accept term

    """


    for func, status, desc in (
        (pyessv.accept, pyessv.GOVERNANCE_STATUS_ACCEPTED, 'accept'),
        # (pyessv.reject, pyessv.GOVERNANCE_STATUS_REJECTED, 'reject'),
        # (pyessv.reset, pyessv.GOVERNANCE_STATUS_PENDING, 'reset'),
        # (pyessv.deprecate, pyessv.GOVERNANCE_STATUS_DEPRECATED, 'deprecate')
        ):
        tu.init(_test, 'governance', '{} term'.format(desc))
        yield _test, func, status
