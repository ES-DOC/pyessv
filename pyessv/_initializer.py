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

	# Read set of authorities from file system & cache.
	logger.log('Loading vocabularies from {}:'.format(DIR_ARCHIVE))
	for authority in read():
		logger.log('... loaded: {}'.format(authority))
		cache(authority)
