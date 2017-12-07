# -*- coding: utf-8 -*-

"""
.. module:: pyessv._initializer.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes library.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os
import collections

import pyessv
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
	logger.log('Loading vocabularies from {}:'.format(DIR_ARCHIVE))
	loaded = []
	for authority in read():
		loaded.append(authority)
		logger.log('... loaded: {}'.format(authority))
		cache(authority)

	# Cache.
	for authority in loaded:
		cache(authority)

	# Expose as psuedo-constants.
	Vocabs = collections.namedtuple('Vocabs', [i.canonical_name.replace('-', '_') for i in loaded])
	pyessv.vocabs = Vocabs._make(loaded)
