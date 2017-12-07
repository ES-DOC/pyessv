# -*- coding: utf-8 -*-

"""
.. module:: pyessv._validation.py
   :copyright: Copyright "December 01, 2016', IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates domain model class instance validation.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime
import inspect
import re
import uuid

from pyessv._constants import NODE_TYPEKEY_SET
from pyessv._constants import GOVERNANCE_STATUS_SET
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._model import Node
from pyessv._utils.compat import basestring
from pyessv._utils.compat import urlparse



def is_valid(instance):
    """Gets flag indicating validity status of a domain model class.

    :returns: Validity status of a domain model class.
    :rtype: bool

    """
    return len(validate(instance)) == 0


def get_errors(instance):
    """Returns sorted list of domain model class instance validation errors.

    :returns: Sorted list of domain model class instance validation errors.
    :rtype: list

    """
    return sorted(list(validate(instance)))


def validate(instance):
    """Validates an instance of a domain node.

    :param instance: Sub-class of pyessv.Node

    :returns: Set of instance validation errrors.
    :rtype: set

    """
    assert isinstance(instance, Node), 'Invalid vocabulary type'

    errs = set()
    for validator in instance.get_validators():
        try:
            validator()
        except AssertionError as err:
            typekey = instance.__class__.__name__
            field = validator.__name__[1:]
            val = getattr(instance, field)
            errs.add('{}: invalid {}: [{}]'.format(typekey, field, val))

    return errs
