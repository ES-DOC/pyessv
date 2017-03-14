# -*- coding: utf-8 -*-

"""
.. module:: test_utils_other.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Exposes other test utility functions.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import contextlib
import inspect
import shutil
import tempfile

import pyesdoc.cv as LIB
from tests.cv.utils_assert import assert_objects



# Test term domain.
TERM_DOMAIN = "earth-system"

# Test term sub-domain.
TERM_SUBDOMAIN = "vegetation"

# Test term kind.
TERM_KIND = "tree"

# Test term kind.
TERM_NAME = "oak"

# Set of term attributes.
TERM_ATTRIBUTES = {
    'domain',
    'subdomain',
    'kind',
    'create_date',
    'status'
}


def assert_terms(term1, term2):
    """Assers equality of 2 terms.

    :param Term term1: A term to be compared against another.
    :param Term term2: A term to be compared against another.

    """
    assert_objects(term1, term2, LIB.Term)
    assert _get_object_attribute_values(term1) == _get_object_attribute_values(term1)


def create_term():
    """Creates & returns a test term.

    """
    return LIB.create(TERM_DOMAIN, TERM_SUBDOMAIN, TERM_KIND, TERM_NAME)


def get_term():
    """Returns a test term.

    """
    return LIB.get_term(TERM_DOMAIN, TERM_SUBDOMAIN, TERM_KIND, TERM_NAME)


@contextlib.contextmanager
def get_term_and_assert(assertion_callback):
    """Returns a term for testing and applies assertion callback.

    """
    term = get_term()
    try:
        yield term
    finally:
        assertion_callback(term)


def init(func, package, desc=None):
    """Initializes a test function prior to be executed.

    """
    if desc is None:
        desc = inspect.getdoc(func)
    desc = desc.strip()
    if desc[-1] == ".":
        desc = desc[:-1]
    desc = desc[0].lower() + desc[1:]
    func.description = "pyesdoc-cv-tests: {0}: {1}".format(package, desc)


def setup():
    """Performs setup functions before running a test.

    """
    LIB.init(_create_options())


def setup_and_create_termset():
    """Performs setup functions and then creates a termset prior to running a test.

    """
    setup()
    # TODO create a termset


def setup_and_create_term():
    """Performs setup functions and then creates a term prior to running a test.

    """
    setup()
    LIB.save(create_term())


def teardown():
    """Performs teardown functions after running a test.

    """
    shutil.rmtree(LIB.get_option(LIB.OPT_IO_DIR))
    LIB.cache.empty()


@contextlib.contextmanager
def get_options():
    """Returns set of options to use when running a test.

    """
    opts = _create_options()
    try:
        yield opts
    finally:
        shutil.rmtree(opts['io_dir'])


def _create_options():
    """Returns set of options to use when running a test.

    """
    return {
        'io_dir': tempfile.mkdtemp(),
        'verbose': False
    }


def _get_object_attribute_values(obj):
    """Returns collection of object attribute values.

    """
    return [getattr(obj, k) for k in dir(obj) if k not in dir(obj.__class__)]



