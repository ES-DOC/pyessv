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

from pyessv._constants import ENTITY_TYPE_SET
from pyessv._constants import GOVERNANCE_STATUS_SET
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._constants import REGEX_LABEL
from pyessv._model import ENTITY_TYPES
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._model import Term
from pyessv._utils.compat import basestring
from pyessv._utils.compat import urlparse



def is_valid(instance):
    """Gets flag indicating validity status of a domain model class.

    :returns: Validity status of a domain model class.
    :rtype: bool

    """
    return len(validate_entity(instance)) == 0


def get_errors(instance):
    """Returns sorted list of domain model class instance validation errors.

    :returns: Sorted list of domain model class instance validation errors.
    :rtype: list

    """
    return sorted(list(validate_entity(instance)))


def validate_entity(instance):
    """Validates an instance of a domain entity.

    :param instance: Sub-class of pyessv.Entity

    :returns: Set of instance validation errrors.
    :rtype: set

    """
    if not isinstance(instance, ENTITY_TYPES):
        raise NotImplementedError('Invalid instance: unknown type')

    errs = set()
    for field_info in _ENTITY_TYPE_INFO[type(instance)]:
        try:
            _validate_field(instance, field_info)
        except ValueError as err:
            errs.add('{}.{}'.format(instance.__class__.__name__, err.message))

    return errs


def _validate_url(val, field):
    """Validates a url field value.

    """
    if not isinstance(val, basestring):
        raise ValueError('invalid {} (str test failed)'.format(field))
    elif not len(val.strip()):
        raise ValueError('invalid {} (>0 length test failed)'.format(field))
    else:
        url = urlparse(val)
        if not url.netloc or not url.scheme:
            raise ValueError('invalid url: {}'.format(field))


def _validate_field(instance, type_info):
    """Validates a field.

    """
    # Unpack type info.
    try:
        field, typeof, cardinality, misc = type_info
    except ValueError:
        field, typeof, cardinality = type_info
        misc = None

    # Error: unknown field.
    if not hasattr(instance, field):
        raise ValueError('{}: unknown'.format(field))

    # Set validation function.
    if cardinality in {'0.N', '1.N'}:
        func = _validate_iterable
    else:
        func = _validate_value

    # Execute validation function.
    val = getattr(instance, field)
    is_mandatory = (cardinality in {'1.1', '1.N'})
    try:
        func(field, val, is_mandatory, typeof, misc)
    except ValueError as err:
        raise ValueError('{}: {}'.format(field, err))


def _validate_iterable(field, val, is_mandatory, typeof, misc):
    """Validates an iterable field value.

    """
    # Error: type mismatch.
    if not isinstance(val, list):
        raise ValueError('type')

    # Error: length.
    if is_mandatory and len(val) == 0:
        raise ValueError('undefined')

    # Error: type mismatch.
    if [i for i in val if not isinstance(i, typeof)]:
        raise ValueError('item type mismatch')

    # Error: url.
    elif misc == 'url':
        for i in [i for i in val if i is not None]:
            _validate_url(i, field)

    # Error: regex.
    elif isinstance(misc, basestring):
        for i in [i for i in val if i is not None]:
            if re.compile(misc).match(i) is None:
                raise ValueError('failed reg-ex validation {}'.format(misc))

    # Error: enum.
    elif isinstance(misc, tuple):
        if [i for i in val if i not in misc]:
            raise ValueError('item not in enum')

    # Error: function.
    elif inspect.isfunction(misc):
        for val in [i for i in val if i is not None]:
            misc(val, field)


def _validate_value(field, val, is_mandatory, typeof, misc):
    """Validates an iterable field value.

    """
    # Error: mandatory.
    if val is None and is_mandatory:
        raise ValueError('undefined')

    if val is not None:
        # Error: type mismatch.
        if not isinstance(val, typeof):
            raise ValueError('type mismatch: {} :: {} :: {}'.format(type(val), typeof, val))

        # Error: url.
        elif misc == 'url':
            _validate_url(val, field)

        # Error: regex.
        elif isinstance(misc, basestring):
            if len(val.strip()) == 0:
                raise ValueError('invalid string length')
            elif re.compile(misc).match(val) is None:
                raise ValueError('failed reg-ex validation {}'.format(misc))

        # Error: enum.
        elif isinstance(misc, tuple):
            if val not in misc:
                raise ValueError('not in enum')

        # Error: function.
        elif inspect.isfunction(misc):
            misc(val, field)

        # Error: string length.
        elif isinstance(val, basestring):
            if len(val.strip()) == 0:
                raise ValueError('invalid string length')


# Type information applying to all entities.
_STANDARD_TYPE_INFO = {
    ('create_date', datetime.datetime, '1.1'),
    ('data', dict, '0.1'),
    ('description', basestring, '1.1'),
    ('label', basestring, '1.1'),
    ('name', basestring, '1.1', REGEX_CANONICAL_NAME),
    ('typekey', basestring, '1.1', tuple(ENTITY_TYPE_SET)),
    ('uid', uuid.UUID, '1.1'),
    ('url', basestring, '0.1', 'url')
}

# Map of types to tuples containing validation info.
_ENTITY_TYPE_INFO = {
    Authority: _STANDARD_TYPE_INFO.union({
        ('scopes', Scope, '0.N'),
    }),
    Collection: _STANDARD_TYPE_INFO.union({
        ('scope', Scope, '1.1'),
        ('terms', Term, '0.N'),
    }),
    Scope: _STANDARD_TYPE_INFO.union({
        ('authority', Authority, '1.1'),
        ('collections', Collection, '0.N'),
    }),
    Term: _STANDARD_TYPE_INFO.union({
        ('alternative_name', basestring, '0.1', REGEX_CANONICAL_NAME),
        ('alternative_url', basestring, '0.1', 'url'),
        ('collection', Collection, '1.1'),
        ('data', dict, '0.1'),
        ('idx', int, '1.1'),
        ('parent', Term, '0.1'),
        ('status', basestring, '1.1', tuple(GOVERNANCE_STATUS_SET)),
        ('synonyms', basestring, '0.N', REGEX_CANONICAL_NAME),
    })
}
