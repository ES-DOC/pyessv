# -*- coding: utf-8 -*-

"""
.. module:: pyessv.archive.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

from pyessv._io import read_authority
from pyessv._constants import DIR_ARCHIVE



# Cached loaded CV objects.
_CACHE = {}


def load(authority, scope=None, collection=None, term=None):
	"""Loads a CV authority from archive.

	"""
	if scope is not None:
		if collection is not None:
			if term is not None:
				return _load_term(authority, scope, collection, term)
			return _load_collection(authority, scope, collection)
		return _load_scope(authority, scope)
	return _load_authority(authority)


def _load_authority(authority):
	"""Loads a CV authority from archive.

	"""
	authority = _format_name(authority)
	_cache_authority(authority)
	try:
		return _CACHE[authority]
	except KeyError:
		pass


def _load_scope(authority, scope):
	"""Loads a CV scope from archive.

	"""
	authority = _load_authority(authority)
	scope = _format_name(scope)
	try:
		return authority[scope]
	except KeyError:
		pass


def _load_collection(authority, scope, collection):
	"""Loads a CV collection from archive.

	"""
	scope = _load_scope(authority, scope)
	collection = _format_name(collection)
	try:
		return scope[collection]
	except KeyError:
		pass


def _load_term(authority, scope, collection, term):
	"""Loads a CV collection from archive.

	"""
	term = _format_name(term)
	collection = _load_collection(authority, scope, collection)
	try:
		item = collection[term]
	except KeyError:
		item = None

	if item is None:
		for item in collection:
			if item.synonyms:
				print "TODO: search synonyms", term, term in item.synonyms

	return item


def _cache_authority(name):
	"""Caches an authority if necessary.

	"""
	if name in _CACHE:
		return

	dpath = os.path.expanduser(DIR_ARCHIVE)
	dpath = os.path.join(dpath, name)
	if not os.path.isdir(dpath):
		raise ValueError("Authority ({}) archive not found".format(name))

	authority = read_authority(dpath)
	if authority is None:
		raise ValueError("Authority ({}) archive not loaded".format(authority))

	_CACHE[name] = authority


def _format_name(name):
	"""Formats a name prior to accessing archive.

	"""
	return unicode(name).strip().lower()
