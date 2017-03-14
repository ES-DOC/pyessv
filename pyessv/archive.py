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

from pyessv.io_mgr import read_authority


# Cached loaded CV objects.
_CACHE = {}

# Directory containing archived collections.
_DIRECTORY = os.getenv("PYESSV_ARCHIVE_HOME")


def set_directory(dpath):
	"""Sets directory to an archive.

	"""
	if not os.path.isdir(dpath):
		raise ValueError("Directory is not a path")

	global _DIRECTORY
	_DIRECTORY = dpath


def load_authority(authority):
	"""Loads a CV authority from archive.

	"""
	authority = unicode(authority).strip().lower()

	_cache_authority(authority)
	try:
		return _CACHE[authority]
	except KeyError:
		pass


def load_scope(authority, scope):
	"""Loads a CV scope from archive.

	"""
	authority = unicode(authority).strip().lower()
	scope = unicode(scope).strip().lower()

	_cache_authority(authority)
	try:
		return _CACHE[authority][scope]
	except KeyError:
		pass


def load_collection(authority, scope, collection):
	"""Loads a CV collection from archive.

	"""
	authority = unicode(authority).strip().lower()
	scope = unicode(scope).strip().lower()
	collection = unicode(collection).strip().lower()

	_cache_authority(authority)
	try:
		return _CACHE[authority][scope][collection]
	except KeyError:
		pass


def load_term(authority, scope, collection, term):
	"""Loads a CV collection from archive.

	"""
	authority = unicode(authority).strip().lower()
	scope = unicode(scope).strip().lower()
	collection = unicode(collection).strip().lower()
	term = unicode(term).strip().lower()

	_cache_authority(authority)
	try:
		return _CACHE[authority][scope][collection][term]
	except KeyError:
		pass


def _cache_authority(name):
	"""Caches an authority if necessary.

	"""
	if name not in _CACHE:
		dpath = os.path.join(_DIRECTORY, name)
		authority = read_authority(dpath)
		if authority is not None:
			_CACHE[name] = authority
