# -*- coding: utf-8 -*-

"""
.. module:: pyessv._factory.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates creation of domain model class instances.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import uuid

import arrow

import pyessv

from pyessv._constants import ENTITY_TYPE_AUTHORITY
from pyessv._constants import ENTITY_TYPE_COLLECTION
from pyessv._constants import ENTITY_TYPE_SCOPE
from pyessv._constants import ENTITY_TYPE_TERM
from pyessv._exceptions import ValidationError
from pyessv._model import ENTITY_TYPE_KEY_MAP
from pyessv._model import Authority
from pyessv._model import Entity
from pyessv._model import Scope
from pyessv._model import Collection
from pyessv._model import Term
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
from pyessv._validation import validate_entity
from pyessv._parser_template import TemplateParser



def create_authority(name, description=None, label=None, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term authority.

    :param str name: Canonical authority name.
    :param str description: Authority description.
    :param str label: Label for UI purposes.
    :param str url: Authority further information URL.
    :param datetime create_date: Date upon which authority was created.
    :param dict data: Arbirtrary data associated with authority.

    :returns: A vocabulary authority, e.g. wcrp.
    :rtype: pyessv.Authority

    """
    instance = _create_entity(Authority, name, description, label, url, create_date, data)
    errors = validate_entity(instance)
    if errors:
        raise ValidationError(errors)

    return instance


def create_scope(authority, name, description=None, label=None, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term scope.

    :param pyessv.Authority authority: CV authority to which scope is bound.
    :param str name: Canonical scope name.
    :param str label: Label for UI purposes.
    :param str description: Scope description.
    :param str url: Scope URL for further information.
    :param datetime create_date: Date upon which scope was created.
    :param dict data: Arbirtrary data associated with scope.

    :returns: A vocabulary scope, e.g. cmip6.
    :rtype: pyessv.Scope

    """
    instance = _create_entity(Scope, name, description, label, url, create_date, data, authority)
    instance.authority = authority
    errors = validate_entity(instance)
    if errors:
        raise ValidationError(errors)

    return instance


def create_collection(scope, name, description=None, label=None, url=None, create_date=None, data=None, term_name_regex=None):
    """Instantiates, initialises & returns a term collection.

    :param pyessv.Scope scope: CV scope to which collection is bound.
    :param str name: Canonical collection name.
    :param str description: Collection description.
    :param str label: Label for UI purposes.
    :param str url: Collection URL for further information.
    :param datetime create_date: Date upon which collection was created.
    :param dict data: Arbirtrary data associated with collection.

    :returns: A vocabulary collection, e.g. insitution-id.
    :rtype: pyessv.Collection

    """
    instance = _create_entity(Collection, name, description, label, url, create_date, data, scope)
    instance.scope = scope
    instance.term_name_regex = term_name_regex
    errors = validate_entity(instance)
    if errors:
        raise ValidationError(errors)

    return instance


def create_term(collection, name, description=None, label=None, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term.

    :param pyessv.Collection collection: The collection to which the term belongs.
    :param str name: Canonical term name.
    :param str description: Term description.
    :param str label: Label for UI purposes.
    :param str url: Term URL for further information.
    :param datetime create_date: Date upon which term was created.
    :param dict data: Arbitrary data associated with term.

    :returns: A vocabulary term, e.g. ipsl.
    :rtype: pyessv.Term

    """
    instance = _create_entity(Term, name, description, label, url, create_date, data, collection)
    instance.collection = collection
    instance.idx = len(collection)
    errors = validate_entity(instance)
    if errors:
        raise ValidationError(errors)

    return instance


def create_template_parser(template, collections):
    """Instantiates, initialises & returns a template parser.

    :param str template: An expression template.
    :param tuple collections: Collections that the template maps to.

    :returns: A vocabulary expression parser.
    :rtype: pyessv.TemplateParser

    """
    assert isinstance(template, basestring), 'Invalid template'
    assert isinstance(collections, tuple), 'Invalid collections'
    assert len(template) > 0, 'Invalid template'
    assert len(collections) > 0, 'Invalid collections'
    assert len([i for i in collections if not isinstance(i, Collection)]) ==0, 'Invalid collections'
    assert template.count('{}') == len(collections), 'Invalid template'

    return TemplateParser(template, collections)


def _create_entity(typeof, name, description, label=None, url=None, create_date=None, data=None, owner=None):
    """Instantiates, initialises & returns an entity.

    """
    # Set core attributes.
    instance = typeof()
    instance.description = description
    instance.label = name
    instance.name = str(name)
    instance.create_date = create_date or arrow.utcnow().datetime
    instance.data = data
    instance.uid = uuid.uuid4()
    instance.url = url

    # Set associative attributes.
    if owner is not None:
        # ... parent in vocab hierarchy
        if isinstance(instance, Scope):
            instance.authority = owner
        elif isinstance(instance, Collection):
            instance.scope = owner
        elif isinstance(instance, Term):
            instance.collection = owner
        # ... child in vocab hierarchy
        if isinstance(owner, Authority):
            owner.scopes.append(instance)
        elif isinstance(owner, Scope):
            owner.collections.append(instance)
        elif isinstance(owner, Collection):
            owner.terms.append(instance)

    return instance
