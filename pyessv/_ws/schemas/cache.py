# -*- coding: utf-8 -*-
"""

.. module:: schemas.cache.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC Errata - endpoint validation schema cache.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

from pyessv._ws.schemas import loader



# Cached store of loaded schemas.
_STORE = collections.defaultdict(dict)

# Set of endpoint substitutions.
_SUBSTITUTIONS = {
	'/1/retrieve',
}


def init(endpoints):
	"""Initializes cache from schemas upon file system.

	:param dict endpoints: Map of application endpoints.

	"""
    # Load retrieve json scehmas.
	for typeof in {'body', 'params', 'headers'}:
		_STORE[typeof]['/1/retrieve'] = loader.load(typeof, '/1/retrieve')

    # Load other json scehmas.
	for endpoint in [i for i in endpoints if not i.startswith('/1/retrieve')]:
		for typeof in {'body', 'params', 'headers'}:
            # payload = loader.load(typeof, endpoint)
			_STORE[typeof][endpoint] = loader.load(typeof, endpoint)


def get_schema(typeof, endpoint):
	"""Gets a schema from cache.

	"""
	for ep in _SUBSTITUTIONS:
		if endpoint.startswith(ep):
			endpoint = ep

	try:
		return _STORE[typeof][endpoint]
	except KeyError:
		pass
