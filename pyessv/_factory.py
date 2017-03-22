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
from pyessv._validation import validate_canonical_name
from pyessv._validation import validate_data
from pyessv._validation import validate_date
from pyessv._validation import validate_entity
from pyessv._validation import validate_unicode
from pyessv._validation import validate_url



def create_authority(name, description, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term authority.

    :param str name: Canonical authority name.
    :param str description: Authority description.
    :param str url: Authority further information URL.
    :param datetime create_date: Date upon which authority was created.
    :param dict data: Arbirtrary data associated with authority.

    :returns: A vocabulary authority, e.g. wcrp.
    :rtype: pyessv.Authority

    """
    instance = _create_entity(Authority, name, description, url, create_date, data)
    if not instance.is_valid:
        raise ValidationError(instance.errors)

    return instance



def create_scope(authority, name, description, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term scope.

    :param pyessv.Authority authority: CV authority to which scope is bound.
    :param str name: Canonical scope name.
    :param str description: Scope description.
    :param str url: Scope URL for further information.
    :param datetime create_date: Date upon which scope was created.
    :param dict data: Arbirtrary data associated with scope.

    :returns: A vocabulary scope, e.g. cmip6.
    :rtype: pyessv.Scope

    """
    instance = _create_entity(Scope, name, description, url, create_date, data, authority)
    instance.authority = authority
    if not instance.is_valid:
        raise ValidationError(instance.errors)

    return instance



def create_collection(scope, name, description, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term collection.

    :param pyessv.Scope scope: CV scope to which collection is bound.
    :param str name: Canonical collection name.
    :param str description: Collection description.
    :param str url: Collection URL for further information.
    :param datetime create_date: Date upon which collection was created.
    :param dict data: Arbirtrary data associated with collection.

    :returns: A vocabulary collection, e.g. insitution-id.
    :rtype: pyessv.Collection

    """
    instance = _create_entity(Collection, name, description, url, create_date, data, scope)
    instance.scope = scope
    if not instance.is_valid:
        raise ValidationError(instance.errors)

    return instance


def create_term(collection, name, description, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term.

    :param pyessv.Collection collection: The collection to which the term belongs.
    :param str name: Canonical term name.
    :param str description: Term description.
    :param str url: Term URL for further information.
    :param datetime create_date: Date upon which term was created.
    :param dict data: Arbitrary data associated with term.

    :returns: A vocabulary term, e.g. ipsl.
    :rtype: pyessv.Term

    """
    instance = _create_entity(Term, name, description, url, create_date, data, collection)
    instance.collection = collection
    instance.idx = Entity.get_count(collection)
    if not instance.is_valid:
        raise ValidationError(instance.errors)

    return instance


def _create_entity(typeof, name, description, url=None, create_date=None, data=None, owner=None):
    """Instantiates, initialises & returns an entity.

    """
    # Validate inputs.
    validate_canonical_name(name, "name")
    validate_unicode(description, "description")
    if url is not None:
        validate_url(url, "url")
    if create_date is not None:
        validate_date(create_date, "create-date")
    if data is not None:
        validate_data(data, "data")
    if owner is not None:
        validate_entity(owner)

    # Format inputs.
    name = unicode(name).strip()
    description = unicode(description).strip()
    if url is not None:
        url = unicode(url).strip()

    # Set core attributes.
    instance = typeof()
    instance.description = description
    instance.label = name
    instance.name = name.lower()
    if create_date:
        instance.create_date = create_date
    if data is not None:
        instance.data = data
    if url is not None:
        instance.url = url

    # Set associative attributes.
    if owner is not None:
        Entity.get_collection(owner).append(instance)

    return instance
