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
from pyessv._constants import GOVERNANCE_STATUS_PENDING
from pyessv._exceptions import ValidationError
from pyessv._model import ENTITY_TYPE_MAP
from pyessv._model import Entity
from pyessv._validation import validate_canonical_name
from pyessv._validation import validate_data
from pyessv._validation import validate_date
from pyessv._validation import validate_entity
from pyessv._validation import validate_unicode
from pyessv._validation import validate_url



def create_authority(canonical_name, description, url, data=None, create_date=None):
	"""Instantiates, initialises & returns a term authority.

	:param str canonical_name: Canonical authority name.
	:param str description: Authority description.
	:param str url: Authority further information URL.
	:param dict data: Arbirtrary data associated with authority.
	:param datetime create_date: Date upon which authority was created.

	:returns: A vocabulary authority, e.g. wcrp.
	:rtype: pyessv.Authority

	"""
	return _create(ENTITY_TYPE_AUTHORITY, canonical_name, description, url, data, create_date, None)


def create_scope(authority, canonical_name, description, url, data=None, create_date=None):
	"""Instantiates, initialises & returns a term scope.

	:param pyessv.Authority authority: CV authority to which scope is bound.
	:param str canonical_name: Canonical scope name.
	:param str description: Scope description.
	:param str url: Scope URL for further information.
	:param dict data: Arbirtrary data associated with scope.
	:param datetime create_date: Date upon which scope was created.

	:returns: A vocabulary scope, e.g. cmip6.
	:rtype: pyessv.Scope

	"""
	return _create(ENTITY_TYPE_SCOPE, canonical_name, description, url, data, create_date, authority)


def create_collection(scope, canonical_name, description, url, data=None, create_date=None):
	"""Instantiates, initialises & returns a term collection.

	:param pyessv.Scope scope: CV scope to which collection is bound.
	:param str canonical_name: Canonical collection name.
	:param str description: Collection description.
	:param str url: Collection URL for further information.
	:param dict data: Arbirtrary data associated with collection.
	:param datetime create_date: Date upon which collection was created.

	:returns: A vocabulary collection, e.g. insitution-id.
	:rtype: pyessv.Collection

	"""
	return _create(ENTITY_TYPE_COLLECTION, canonical_name, description, url, data, create_date, scope)


def create_term(collection, canonical_name, description, url, data=None, create_date=None):
	"""Instantiates, initialises & returns a term.

	:param pyessv.Collection collection: The collection to which the term belongs.
	:param str canonical_name: Canonical term name.
	:param str description: Term description.
	:param dict data: Arbitrary data associated with term.
	:param str url: Term URL for further information.
	:param datetime create_date: Date upon which term was created.

	:returns: A vocabulary term, e.g. ipsl.
	:rtype: pyessv.Term

	"""
	return _create(ENTITY_TYPE_TERM, canonical_name, description, url, data, create_date, collection)


def _create(typekey, canonical_name, description, url, data, create_date, owner):
	"""Instantiates, initialises & returns an entity.

	"""
	# Validate inputs.
	validate_canonical_name(canonical_name, "{}-canonical-name".format(typekey))
	validate_unicode(description, "{}-description".format(typekey))
	validate_url(url, "{}-url".format(typekey))
	if data is not None:
		validate_data(data, "{}-data".format(typekey))
	if create_date is not None:
		validate_date(create_date, "{}-date".format(typekey))
	if owner is not None:
		validate_entity(owner)

	# Format inputs.
	canonical_name = unicode(canonical_name).strip()
	description = unicode(description).strip()
	url = unicode(url).strip()

	# Set core attributes.
	instance = ENTITY_TYPE_MAP[typekey]()
	instance.create_date = create_date or arrow.utcnow().datetime
	instance.description = description
	instance.data = data or dict()
	instance.label = canonical_name
	instance.name = canonical_name.lower()
	instance.status = GOVERNANCE_STATUS_PENDING
	instance.uid = uuid.uuid4()
	instance.url = url

	# Set associative attributes.
	if owner is not None:
		if typekey == ENTITY_TYPE_SCOPE:
			instance.authority = owner
		elif typekey == ENTITY_TYPE_COLLECTION:
			instance.scope = owner
		elif typekey == ENTITY_TYPE_TERM:
			instance.collection = owner
		Entity.get_collection(owner).append(instance)
		instance.idx = Entity.get_count(owner)

	# If in error, raise validation exception.
	if not instance.is_valid:
		raise ValidationError(instance.errors)

	return instance
