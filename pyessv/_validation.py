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
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._model import Term
from pyessv._model import IterableNode
from pyessv._model import Node
from pyessv._utils.compat import basestring
from pyessv._utils.compat import urlparse



def is_valid(instance):
    """Gets flag indicating validity status of a domain model class.

    :returns: Validity status of a domain model class.
    :rtype: bool

    """
    return len(validate_node(instance)) == 0


def get_errors(instance):
    """Returns sorted list of domain model class instance validation errors.

    :returns: Sorted list of domain model class instance validation errors.
    :rtype: list

    """
    return sorted(list(validate_node(instance)))


def validate_node(instance):
    """Validates an instance of a domain node.

    :param instance: Sub-class of pyessv.Node

    :returns: Set of instance validation errrors.
    :rtype: set

    """
    if not isinstance(instance, Node):
        raise NotImplementedError('Invalid instance: unknown type')

    validators = _validate_core()
    if isinstance(instance, Authority):
        validators += _validate_authority()
    elif isinstance(instance, Scope):
        validators += _validate_scope()
    elif isinstance(instance, Collection):
        validators += _validate_collection()
    elif isinstance(instance, Term):
        validators += _validate_term()

    errs = set()
    for validator in validators:
        field = validator.__name__.split("_validate_")[-1]
        try:
            validator(instance)
        except AssertionError as err:
            errs.add('{}. Invalid {}. {}'.format(instance.__class__.__name__, field, getattr(instance, field)))

    return errs


def _validate_core():
    """Returns common instance validators.

    """
    def _validate_create_date(i):
        assert isinstance(i.create_date, datetime.datetime)

    def _validate_data(i):
        if i.data is not None:
            assert isinstance(i.data, dict)

    def _validate_description(i):
        if isinstance(i, IterableNode):
            _assert_string(i.description)
        elif i.description is not None:
            _assert_string(i.description)

    def _validate_label(i):
        _assert_string(i.label)

    def _validate_synonyms(i):
        _assert_iterable(i.synonyms, _assert_string)

    def _validate_typekey(i):
        assert i.typekey in NODE_TYPEKEY_SET

    def _validate_uid(i):
        assert isinstance(i.uid, uuid.UUID)

    def _validate_url(i):
        if i.url is not None:
            _assert_url(i.url)

    return [
        _validate_create_date,
        _validate_data,
        _validate_description,
        _validate_label,
        _validate_synonyms,
        _validate_typekey,
        _validate_uid,
        _validate_url
    ]


def _validate_authority():
    """Returns Authority instance validators.

    """
    def _validate_scopes(i):
        _assert_iterable(i.scopes, Scope)

    def _validate_canonical_name(i):
        _assert_string(i.canonical_name, REGEX_CANONICAL_NAME)

    return [
        _validate_scopes,
        _validate_canonical_name
        ]


def _validate_scope():
    """Returns Scope instance validators.

    """
    def _validate_authority(i):
        assert isinstance(i.authority, Authority)

    def _validate_collections(i):
        _assert_iterable(i.collections, Collection)

    def _validate_canonical_name(i):
        _assert_string(i.canonical_name, REGEX_CANONICAL_NAME)

    return [
        _validate_authority,
        _validate_collections,
        _validate_canonical_name
        ]


def _validate_collection():
    """Returns Collection instance validators.

    """
    def _validate_canonical_name(i):
        _assert_string(i.canonical_name, REGEX_CANONICAL_NAME)

    def _validate_scope(i):
        assert isinstance(i.scope, Scope)

    def _validate_terms(i):
        _assert_iterable(i.terms, Term)

    def _validate_template(i):
        if i.template is not None:
            _assert_string(i.template)
            _assert_iterable(i.template_collections, Collection)
            assert i.template.count('{}') == len(i.template_collections)
        else:
            assert i.template_collections is None

    return [
        _validate_scope,
        _validate_terms,
        _validate_canonical_name,
        _validate_template
        ]


def _validate_term():
    """Returns Term instance validators.

    """
    def _validate_alternative_name(i):
        if i.alternative_name is not None:
            _assert_string(i.alternative_name)

    def _validate_alternative_url(i):
        if i.alternative_url is not None:
            _assert_url(i.alternative_url)

    def _validate_collection(i):
        assert isinstance(i.collection, Collection)

    def _validate_idx(i):
        assert isinstance(i.idx, int)

    def _validate_canonical_name(i):
        if i.collection.term_regex is None:
            reg_ex = REGEX_CANONICAL_NAME
        else:
            reg_ex = i.collection.term_regex
        _assert_string(i.canonical_name, reg_ex)

    def _validate_parent(i):
        if i.parent is not None:
            assert isinstance(i.parent, Term)

    def _validate_status(i):
        assert i.status in GOVERNANCE_STATUS_SET

    return [
        _validate_alternative_name,
        _validate_alternative_url,
        _validate_collection,
        _validate_idx,
        _validate_canonical_name,
        _validate_parent,
        _validate_status
        ]


def _assert_string(val, reg_ex=None):
    """Asserts a string value.

    """
    assert isinstance(val, basestring)
    assert len(val.strip()) > 0
    if reg_ex:
        assert re.compile(reg_ex).match(val) is not None


def _assert_url(val):
    """Asserts a url value.

    """
    _assert_string(val)
    url = urlparse(val)
    assert url.netloc and url.scheme


def _assert_iterable(val, modifier):
    """Asserts an iterable value.

    """
    assert isinstance(val, list)
    for i in val:
        if inspect.isfunction(modifier):
            modifier(i)
        else:
            assert isinstance(i, modifier)
