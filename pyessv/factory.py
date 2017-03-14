# -*- coding: utf-8 -*-

"""
.. module:: pyessv.factory.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates creation of domain model class instances.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import uuid

import arrow

from pyessv import constants
from pyessv import validation as v
from pyessv.exceptions import ValidationError
from pyessv.model import Term
from pyessv.model import Authority
from pyessv.model import Collection
from pyessv.model import Scope



def create_authority(name, description, url, create_date=None):
	"""Instantiates, initialises & returns a term authority.

	"""
	# Validate inputs.
	v.validate_authority_name(name)
	v.validate_authority_description(description)
	v.validate_authority_url(url)

	# Format inputs.
	name = unicode(name).strip()
	description = unicode(description).strip()
	url = unicode(url).strip()

	# Instantiate.
	i = Authority()
	i.create_date = create_date or arrow.utcnow().datetime
	i.description = description
	i.label = name
	i.name = name.lower()
	i.url = url

	# Raise validation exception (if appropriate).
	if not i.is_valid:
		raise ValidationError(i.errors)

	return i


def create_scope(authority, name, description, url, create_date=None):
	"""Instantiates, initialises & returns a term scope.

	param: pyessv.Authority authority: CV authority to which scope is bound.
	param: str name: Scope name (must be unique within authority).
	param: str description: Scope description.
	param: str url: Scope URL for further information.
	param: datetime create_date: Date upon which scope was created.

	"""
	# Validate inputs.
	v.validate(authority)
	v.validate_scope_name(name)
	v.validate_scope_description(description)
	v.validate_scope_url(url)

	# Format inputs.
	name = unicode(name).strip()
	description = unicode(description).strip()
	url = unicode(url).strip()

	# Instantiate.
	i = Scope()
	i.authority = authority
	i.create_date = create_date or arrow.utcnow().datetime
	i.description = description
	i.label = name
	i.name = name.lower()
	i.uid = uuid.uuid4()
	i.url = url

	# Append to parent & set idx.
	authority.scopes.append(i)
	i.idx = len(authority.scopes)

	# Raise validation exception (if appropriate).
	if not i.is_valid:
		raise ValidationError(i.errors)

	return i


def create_collection(scope, name, description, create_date=None):
	"""Instantiates, initialises & returns a term collection.

	param: pyessv.Scope scope: CV scope to which collection is bound.
	param: str name: Collection name (must be unique within scope).
	param: str description: Collection description.
	param: datetime create_date: Date upon which collection was created.

	"""
	# Validate inputs.
	v.validate(scope)
	v.validate_collection_name(name)
	v.validate_collection_description(description)

	# Format inputs.
	name = unicode(name).strip()
	description = unicode(description).strip()

	# Instantiate.
	i = Collection()
	i.create_date = create_date or arrow.utcnow().datetime
	i.description = description
	i.label = name
	i.name = name.lower()
	i.scope = scope
	i.uid = uuid.uuid4()

	# Append to parent & set idx.
	scope.collections.append(i)
	i.idx = len(scope.collections)

	# Raise validation exception (if appropriate).
	if not i.is_valid:
		raise ValidationError(i.errors)

	return i


def create_term(collection, name, data=None, create_date=None):
	"""Instantiates, initialises & returns a term.

	param: pyessv.Collection collection: The collection to which the term belongs.
	param: str name: Name of term.
	param: dict data: Arbitrary data associated with term.
	param: datetime create_date: Date upon which term was created.

	"""
	# Validate inputs.
	v.validate(collection)
	v.validate_term_name(name)
	if data is not None:
		v.validate_term_data(data)

	# Format inputs.
	name = unicode(name).strip()

	# Instantiate.
	i = Term()
	i.collection = collection
	i.create_date = create_date or arrow.utcnow().datetime
	i.label = name
	i.name = name.lower()
	i.status = constants.GOVERNANCE_STATUS_PENDING
	i.uid = uuid.uuid4()
	i.data = data

	# Append to parent & set idx.
	collection.terms.append(i)
	i.idx = len(collection.terms)

	# Raise validation exception (if appropriate).
	if not i.is_valid:
		raise ValidationError(i.errors)

	return i
