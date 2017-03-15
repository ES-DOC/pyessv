# -*- coding: utf-8 -*-

"""
.. module:: pyessv._validation.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encpasulates domain model class instance validation.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._model import TYPES
from pyessv._model import TYPE_INFO



def validate(instance):
    """Validates an instance of a domain model class.

    :param instance: Sub-class of pyessv.Entity

    :returns: Set of instance validation errrors.
    :rtype: set

    """
    if not isinstance(instance, TYPES):
        raise NotImplementedError("Invalid instance: unknown type")

    return _validate_instance(instance)


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


def _validate_instance(instance):
    """Validates an instance.

    """
    errs = set()

    for field_info in TYPE_INFO[type(instance)]:
        try:
            _validate_field(instance, field_info)
        except ValueError as err:
            errs.add("{}.{}".format(instance.__class__.__name__, err.message))

    return errs


def _validate_field(instance, type_info):
    """Validates a field.

    """
    # Unpack type info.
    try:
        field, typeof, cardinality, misc = type_info
    except ValueError:
        field, typeof, cardinality = type_info
        misc = None
    if isinstance(misc, unicode):
        pass
        # print "TODO: validate {}.{} by regex".format(instance.__class__.__name__, field)

    # Error: unknown field.
    if not hasattr(instance, field):
        raise ValueError("{}: unknown".format(field))

    # Set validation function.
    if cardinality in {"0.N", "1.N"}:
        func = _validate_iterable
    else:
        func = _validate_value

    # Execute validation function.
    val = getattr(instance, field)
    is_mandatory = (cardinality in {"1.1", "1.N"})
    try:
        func(val, is_mandatory, typeof, misc)
    except ValueError as err:
        raise ValueError("{}: {}".format(field, err))


def _validate_value(val, is_mandatory, typeof, misc):
    """Validates an iterable field value.

    """
    # Error: mandatory.
    if is_mandatory and val is None:
        raise ValueError("undefined")

    # Error: type mismatch.
    if val is not None and not isinstance(val, typeof):
        raise ValueError("type mismatch")

    # Error: unicode length.
    # TODO

    # Error: enum.
    if isinstance(misc, tuple) and val not in misc:
        raise ValueError("not in enum")

    # Error: regex.
    if isinstance(misc, unicode):
        # TODO: validate regex
        pass


def _validate_iterable(val, is_mandatory, typeof, misc):
    """Validates an iterable field value.

    """
    # Error: type mismatch.
    if not isinstance(val, list):
        raise ValueError("type")

    # Error: length.
    if is_mandatory and len(val) == 0:
        raise ValueError("undefined")

    # Error: item type mismatch.
    if [i for i in val if not isinstance(i, typeof)]:
        raise ValueError("item type mismatch")

    # Error: enum.
    if isinstance(misc, tuple) and [i for i in val if i not in misc]:
        raise ValueError("item not in enum")

    # Error: regex.
    if isinstance(misc, unicode):
        # TODO: validate regex
        pass


def validate_authority_description(description):
    """Validates a termset's description.

    """
    validate_unicode(description, "description")


def validate_authority_name(name):
    """Validates a term's name.

    """
    validate_unicode(name, "name")
    for char in REGEX_CANONICAL_NAME:
        if name.find(char) > -1:
            raise ValueError('invalid name')


def validate_authority_url(url):
    """Validates a term's url.

    """
    validate_url(url, "url")


def validate_collection_description(description):
    """Validates a termset's description.

    """
    validate_unicode(description, "description")


def validate_collection_name(name):
    """Validates a term's name.

    """
    validate_unicode(name, "name")
    for char in REGEX_CANONICAL_NAME:
        if name.find(char) > -1:
            raise ValueError('invalid name')


def validate_scope_description(description):
    """Validates a termset's description.

    """
    validate_unicode(description, "description")


def validate_scope_name(name):
    """Validates a term's name.

    """
    validate_unicode(name, "name")
    for char in REGEX_CANONICAL_NAME:
        if name.find(char) > -1:
            raise ValueError('invalid name')


def validate_scope_url(url):
    """Validates a term's url.

    """
    validate_url(url, "url")


def validate_term_data(data):
    """Validates a term's data.

    """
    if not isinstance(data, dict):
        raise ValueError("invalid term data")


def validate_term_name(name):
    """Validates a term's name.

    """
    validate_unicode(name, "name")
    for char in REGEX_CANONICAL_NAME:
        if name.find(char) > -1:
            raise ValueError('invalid name')


def validate_unicode(val, field):
    """Validates a unicode field value.

    """
    if val is None:
        raise ValueError("undefined {}".format(field))
    if not isinstance(val, unicode):
        raise ValueError("invalid {} (unicode test failed)".format(field))
    if not len(val.strip()):
        raise ValueError("invalid {} (>0 length test failed)".format(field))


def validate_url(val, field):
    """Validates a url field value.

    """
    validate_unicode(val, field)
    # TODO: apply regex
