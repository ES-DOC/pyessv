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
        try:
            validator(instance)
        except ValueError as err:
            errs.add('{}.{}'.format(instance.__class__.__name__, err.message))

    return errs


def _validate_core():
    """Returns common instance validators.

    """
    def _validate_create_date(i):
        if isinstance(i.create_date, datetime.datetime) == False:
            raise ValueError("Invalid create_date")

    def _validate_data(i):
        if i.data is None:
            return
        if isinstance(i.data, dict) == False:
            raise ValueError("Invalid data")

    def _validate_description(i):
        if isinstance(i.description, basestring) == False or \
           len(i.description.strip()) == 0:
            raise ValueError("Invalid description")

    def _validate_label(i):
        if isinstance(i.label, basestring) == False or \
           len(i.label.strip()) == 0:
            raise ValueError("Invalid label")

    def _validate_typekey(i):
        if i.typekey not in ENTITY_TYPE_SET:
            raise ValueError("Invalid typekey")

    def _validate_uid(i):
        if isinstance(i.uid, uuid.UUID) == False:
            raise ValueError("Invalid uid")

    def _validate_url(i):
        if i.url is None:
            return
        if isinstance(i.url, basestring) == False or \
           len(i.url.strip()) == 0:
            raise ValueError("Invalid url")
        url = urlparse(i.url)
        if not url.netloc or not url.scheme:
            raise ValueError('invalid url')


    return [
        _validate_create_date,
        _validate_data,
        _validate_description,
        _validate_label,
        _validate_typekey,
        _validate_uid,
        _validate_url
    ]


def _validate_authority():
    """Returns Authority instance validators.

    """
    def _validate_scopes(i):
        if isinstance(i.scopes, list) == False or \
           [j for j in i.scopes if isinstance(j, Scope) == False]:
            raise ValueError("Invalid scopes")

    def _validate_name(i):
        if isinstance(i.name, basestring) == False or \
           len(i.name.strip()) == 0 or \
           re.compile(REGEX_CANONICAL_NAME).match(i.name) is None:
            raise ValueError("Invalid name")

    return [
        _validate_scopes,
        _validate_name
        ]


def _validate_scope():
    """Returns Scope instance validators.

    """
    def _validate_authority(i):
        if isinstance(i.authority, Authority) == False:
            raise ValueError("Invalid authority")

    def _validate_collections(i):
        if isinstance(i.collections, list) == False or \
           [j for j in i.collections if isinstance(j, Collection) == False]:
            raise ValueError("Invalid collections")

    def _validate_name(i):
        if isinstance(i.name, basestring) == False or \
           len(i.name.strip()) == 0 or \
           re.compile(REGEX_CANONICAL_NAME).match(i.name) is None:
            raise ValueError("Invalid name")

    return [
        _validate_authority,
        _validate_collections,
        _validate_name
        ]


def _validate_collection():
    """Returns Collection instance validators.

    """
    def _validate_scope(i):
        if isinstance(i.scope, Scope) == False:
            raise ValueError("Invalid scope")

    def _validate_terms(i):
        if isinstance(i.terms, list) == False or \
           [j for j in i.terms if isinstance(j, Term) == False]:
            raise ValueError("Invalid terms")

    def _validate_name(i):
        if isinstance(i.name, basestring) == False or \
           len(i.name.strip()) == 0 or \
           re.compile(REGEX_CANONICAL_NAME).match(i.name) is None:
            raise ValueError("Invalid name")

    return [
        _validate_scope,
        _validate_terms,
        _validate_name
        ]


def _validate_term():
    """Returns Term instance validators.

    """
    def validate_alternative_name(i):
        if i.alternative_name is None:
            return
        if isinstance(i.alternative_name, basestring) == False or \
           len(i.alternative_name.strip()) == 0:
            raise ValueError("Invalid alternative_name")

    def validate_alternative_url(i):
        if i.alternative_url is None:
            return
        if isinstance(i.alternative_url, basestring) == False or \
           len(i.alternative_url.strip()) == 0:
            raise ValueError("Invalid alternative_url")
        url = urlparse(i.alternative_url)
        if not url.netloc or not url.scheme:
            raise ValueError('invalid alternative_url')

    def validate_collection(i):
        if isinstance(i.collection, Collection) == False:
            raise ValueError("Invalid collection")

    def validate_idx(i):
        if isinstance(i.idx, int) == False:
            raise ValueError("Invalid idx")

    def _validate_name(i):
        if i.collection.term_name_regex is None:
            reg_ex = REGEX_CANONICAL_NAME
        else:
            reg_ex = i.collection.term_name_regex
        if isinstance(i.name, basestring) == False or \
           len(i.name.strip()) == 0 or \
           re.compile(reg_ex).match(i.name) is None:
            raise ValueError("Invalid name")


    def validate_parent(i):
        if i.parent is None:
            return
        if isinstance(i.parent, Term) == False:
            raise ValueError("Invalid parent")

    def validate_status(i):
        if i.status not in GOVERNANCE_STATUS_SET:
            raise ValueError("Invalid status")

    def validate_synonyms(i):
        if isinstance(i.synonyms, list) == False or \
           [j for j in i.synonyms if isinstance(j, basestring) == False] or \
           [j for j in i.synonyms if len(j) == 0]:
            raise ValueError("Invalid synonyms")

    return [
        validate_alternative_name,
        validate_alternative_url,
        validate_collection,
        validate_idx,
        _validate_name,
        validate_parent,
        validate_status,
        validate_synonyms
        ]
