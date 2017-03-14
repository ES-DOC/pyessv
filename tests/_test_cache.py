# -*- coding: utf-8 -*-

"""
.. module:: test_cache.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv cache tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pyessv

import nose

import tests.utils as tu


def _setup():
	"""Test runner setup.

	"""
	tu.setup()
	term = tu.create_term()
	pyessv.save(term)


@nose.with_setup(_setup, tu.teardown)
def test_get_term_01():
	"""pyessv-tests: cache: get term

	"""
	term = pyessv.get_term(tu.TERM_DOMAIN, tu.TERM_SUBDOMAIN, tu.TERM_KIND, tu.TERM_NAME)
	tu.assert_object(term, pyessv.Term)
