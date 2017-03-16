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
	_set_cache(authority)
	if term is not None:
		return  _load_term(authority, scope, collection, term)
	if collection is not None:
		return  _load_collection(authority, scope, collection)
	if scope is not None:
		return  _load_scope(authority, scope)
	return  _load_authority(authority)


def _load_authority(authority):
	"""Loads a CV authority from archive.

	"""
	try:
		return _CACHE[_format_name(authority)]
	except KeyError:
		pass


def _load_scope(authority, scope):
	"""Loads a CV scope from archive.

	"""
	authority = _load_authority(authority)
	try:
		return authority[_format_name(scope)]
	except KeyError:
		pass


def _load_collection(authority, scope, collection):
	"""Loads a CV collection from archive.

	"""
	scope = _load_scope(authority, scope)
	try:
		return scope[_format_name(collection)]
	except KeyError:
		pass


def _load_term(authority, scope, collection, term):
	"""Loads a CV collection from archive.

	"""
	collection = _load_collection(authority, scope, collection)
	try:
		return collection[_format_name(term)]
	except KeyError:
		pass


def _set_cache(name):
	"""Caches set of  authority vocabs (if necessary).

	"""
	name = _format_name(name)
	if name in _CACHE:
		return

	# Set path to authority archive.
	dpath = os.path.expanduser(DIR_ARCHIVE)
	dpath = os.path.join(dpath, name)
	if not os.path.isdir(dpath):
		raise ValueError("Authority ({}) archive not found".format(name))

	# Read vocab files from file system.
	authority = read_authority(dpath)
	if authority is None:
		raise ValueError("Authority ({}) archive not loaded".format(authority))

	_CACHE[name] = authority


def _format_name(name):
	"""Formats a name prior to accessing archive.

	"""
	return unicode(name).strip().lower()
