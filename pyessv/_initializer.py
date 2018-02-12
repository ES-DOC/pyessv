# -*- coding: utf-8 -*-

"""
.. module:: pyessv._initializer.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes library.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import inspect
import os

import pyessv
from pyessv._accessors import ACCESSORS
from pyessv._cache import cache
from pyessv._constants import DIR_ARCHIVE
from pyessv._io_manager import read
from pyessv._utils import logger



def init():
	"""Library initializer.

	"""
	# Verify archive folder exists.
	if not os.path.isdir(DIR_ARCHIVE):
		raise EnvironmentError('{} directory does not exists'.format(DIR_ARCHIVE))

	# Load set of authorities from file system.
	authorities = _load_authorities()

	# Mixin pseudo-constants.
	_mixin_constants(authorities)

	# Set scope level accessor functions.
	_mixin_scope_accessors(authorities)


def _load_authorities():
	"""Loads vocabulary authorities from archive.

	"""
	logger.log('Loading vocabularies from {}:'.format(DIR_ARCHIVE))
	authorities = []
	for authority in read():
		authorities.append(authority)
		logger.log('... loaded: {}'.format(authority))
		cache(authority)

	return authorities


def _mixin_constants(authorities):
	"""Mixes in authorities as pseudo-constants to pyessv.

	"""
	for authority in authorities:
		attr_name = authority.canonical_name.replace('-', '_').upper()
		setattr(pyessv, attr_name, authority)


def _mixin_scope_accessors(authorities):
	"""Mixes in scope level vocab accessors functions.

	"""
	# In pyessv._accessors sub-package are modules that expose helper functions for accessing vocabularies,
	# here we are ensuring that those functions are easily accessed.
	targets = []
	for authority in authorities:
		for scope in authority:
			try:
				accessor = ACCESSORS[authority.canonical_name][scope.canonical_name]
			except KeyError:
				pass
			else:
				targets.append((scope, accessor))

	# Mixin accessor functions with scope.
	for scope, accessor in targets:
		funcs = [i for i in inspect.getmembers(accessor)
				 if inspect.isfunction(i[1]) and not i[0].startswith('_')]
		for name, func in funcs:
			setattr(scope, name, func)
