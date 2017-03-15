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

from pyessv._constants import GOVERNANCE_STATUS_PENDING
from pyessv._exceptions import ValidationError
from pyessv._model import Term
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._validation import validate
from pyessv._validation import validate_authority_description
from pyessv._validation import validate_authority_name
from pyessv._validation import validate_authority_url
from pyessv._validation import validate_collection_description
from pyessv._validation import validate_collection_name
from pyessv._validation import validate_scope_description
from pyessv._validation import validate_scope_name
from pyessv._validation import validate_scope_url
from pyessv._validation import validate_term_data
from pyessv._validation import validate_term_name



def create_authority(name, description, url, create_date=None):
	"""Instantiates, initialises & returns a term authority.

	"""
	# Validate inputs.
	validate_authority_name(name)
	validate_authority_description(description)
	validate_authority_url(url)

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
	validate(authority)
	validate_scope_name(name)
	validate_scope_description(description)
	validate_scope_url(url)

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
	validate(scope)
	validate_collection_name(name)
	validate_collection_description(description)

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
	validate(collection)
	validate_term_name(name)
	if data is not None:
		validate_term_data(data)

	# Format inputs.
	name = unicode(name).strip()

	# Instantiate.
	i = Term()
	i.collection = collection
	i.create_date = create_date or arrow.utcnow().datetime
	i.label = name
	i.name = name.lower()
	i.status = GOVERNANCE_STATUS_PENDING
	i.uid = uuid.uuid4()
	i.data = data

	# Append to parent & set idx.
	collection.terms.append(i)
	i.idx = len(collection.terms)

	# Raise validation exception (if appropriate).
	if not i.is_valid:
		raise ValidationError(i.errors)

	return i
