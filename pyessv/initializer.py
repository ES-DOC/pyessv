"""
.. module:: pyessv.initializer.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes library.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import inspect
import os

import pyessv
from pyessv.accessors import ACCESSORS
from pyessv.cache import encache
from pyessv.constants import DIR_ARCHIVE
from pyessv.io_manager import read
from pyessv.utils import logger
from pyessv import io_manager



def init(archive_dir=DIR_ARCHIVE, authority=None, scope=None):
	"""Library initializer.

    :param authority: Authority to be loaded (if unspecified then all will be loaded).
    :param scope: Scope to be loaded (if unspecified then all will be loaded).

	"""
	# Verify archive folder exists.
	if not os.path.isdir(archive_dir):
		raise EnvironmentError('{} directory does not exists'.format(archive_dir))

	# Load set of authorities from file system.
	authorities = _load_authorities(archive_dir, authority, scope)

	# Mixin pseudo-constants.
	_mixin_constants(authorities)

	# Set scope level accessor functions.
	_mixin_scopeaccessors(authorities)


def _load_authorities(archive_dir, authority, scope):
	"""Loads vocabulary authorities from archive.

	"""
	logger.log('Loading vocabularies from {} ... please wait'.format(DIR_ARCHIVE))
	authorities = []
	for authority in io_manager.read(archive_dir, authority, scope):
		authorities.append(authority)
		encache(authority)

	return authorities


def _mixin_constants(authorities):
	"""Mixes in authorities as pseudo-constants to pyessv.

	"""
	for authority in authorities:
		attr_name = authority.canonical_name.replace('-', '_').upper()
		setattr(pyessv, attr_name, authority)


def _mixin_scopeaccessors(authorities):
	"""Mixes in scope level vocab accessors functions.

	"""
	# In pyessv.accessors sub-package are modules that expose helper functions for accessing vocabularies,
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
