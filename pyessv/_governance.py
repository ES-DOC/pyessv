# -*- coding: utf-8 -*-

"""
.. module:: pyessv._governance.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulate govenerance features.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._constants import GOVERNANCE_STATUS_ACCEPTED
from pyessv._constants import GOVERNANCE_STATUS_DEPRECATED
from pyessv._constants import GOVERNANCE_STATUS_PENDING
from pyessv._constants import GOVERNANCE_STATUS_REJECTED
from pyessv._model import IterableNode
from pyessv._model import Node



def accept(target):
    """Marks node as accepted.

    """
    _apply(target, pyessv.GOVERNANCE_STATUS_ACCEPTED)


def deprecate(target):
    """Marks node as deprecated.

    """
    _apply(target, pyessv.GOVERNANCE_STATUS_DEPRECATED)


def destroy(target):
    """Marks node for removal from all persistant state stores.

    """
    _apply(target, pyessv.GOVERNANCE_STATUS_DEPRECATED)


def reject(target):
    """Marks node as rejected.

    """
    _apply(target, pyessv.GOVERNANCE_STATUS_REJECTED)


def reset(target):
    """Resets node status.

    """
    _apply(target, pyessv.GOVERNANCE_STATUS_PENDING)


def _apply(target, status):
    """Applies governance status update.

    """
    assert isinstance(target, Node), \
           'Cannot apply governance status to a non domain node'

    # Update status.
    target.status = status

    # Cascade.
    if isinstance(target, IterableNode):
        for child in target:
            _apply(child, status)
