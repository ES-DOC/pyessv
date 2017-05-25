# -*- coding: utf-8 -*-

"""
.. module:: utils_cv.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Exposes other test utility functions.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import os
import shutil

import pyessv as LIB
from pyessv._cache import cache
from pyessv._cache import uncache
from tests.utils_assert import assert_objects



# Test authority.
TEST_AUTHORITY = None
TEST_AUTHORITY_NAME = 'test-authority'
TEST_AUTHORITY_NAMESPACE = TEST_AUTHORITY_NAME
TEST_AUTHORITY_DESCRIPTION = 'test-authority-description'
TEST_AUTHORITY_URL = 'https://github.com/ES-DOC/pyesssv-archive/{}'.format(TEST_AUTHORITY_NAME)
TEST_AUTHORITY_ALTERNATIVE_NAME = 'test-authority-alternative-name'
TEST_AUTHORITY_ALTERNATIVE_URL = 'https://github.com/ES-DOC/pyesssv-archive/{}'.format(TEST_AUTHORITY_NAME)
TEST_AUTHORITY_SYNONYMS = ['test-authority-synonym-1', 'test-authority-synonym-2']

# Test scope.
TEST_SCOPE = None
TEST_SCOPE_NAME = 'test-scope'
TEST_SCOPE_NAMESPACE = ":".join([TEST_AUTHORITY_NAME, TEST_SCOPE_NAME])
TEST_SCOPE_DESCRIPTION = 'test-scope-description'
TEST_SCOPE_URL = '{}/{}'.format(TEST_AUTHORITY_URL, TEST_SCOPE_NAME)
TEST_SCOPE_SYNONYMS = ['test-scope-synonym-1', 'test-scope-synonym-2']

# Test collection.
TEST_COLLECTION = None
TEST_COLLECTION_NAME = 'test-collection'
TEST_COLLECTION_NAMESPACE = ":".join([TEST_AUTHORITY_NAME, TEST_SCOPE_NAME, TEST_COLLECTION_NAME])
TEST_COLLECTION_DESCRIPTION = 'test-collection-description'
TEST_COLLECTION_URL = '{}/{}'.format(TEST_SCOPE_URL, TEST_COLLECTION_NAME)
TEST_COLLECTION_SYNONYMS = ['test-collection-synonym-1', 'test-collection-synonym-2']

# Test composite collection.
TEST_COMPOSITE_COLLECTION = None
TEST_COMPOSITE_COLLECTION_NAME = 'test-composite-collection'
TEST_COMPOSITE_COLLECTION_NAMESPACE = ":".join([TEST_AUTHORITY_NAME, TEST_SCOPE_NAME, TEST_COMPOSITE_COLLECTION_NAME])
TEST_COMPOSITE_COLLECTION_DESCRIPTION = 'test-composite-collection-description'
TEST_COMPOSITE_COLLECTION_URL = '{}/{}'.format(TEST_SCOPE_URL, TEST_COLLECTION_NAME)
TEST_COMPOSITE_COLLECTION_SYNONYMS = ['test-composite-collection-synonym-1', 'test-composite-collection-synonym-2']
TEST_COMPOSITE_COLLECTION_TEMPLATE = '{}-TEST'
TEST_COMPOSITE_COLLECTION_TEMPLATE_COLLECTIONS = [TEST_COLLECTION_NAMESPACE]


# Test term.
TEST_TERM = None
TEST_TERM_NAME = 'test-term'
TEST_TERM_NAMESPACE = ":".join([TEST_AUTHORITY_NAME, TEST_SCOPE_NAME, TEST_COLLECTION_NAME, TEST_TERM_NAME])
TEST_TERM_DESCRIPTION = 'test-term-description'
TEST_TERM_URL = '{}/{}'.format(TEST_COLLECTION_URL, TEST_TERM_NAME)
TEST_TERM_SYNONYMS = ['test-term-synonym-1', 'test-term-synonym-2']


def create_authority():
    """Creates & returns a test authority.

    """
    global TEST_AUTHORITY
    if TEST_AUTHORITY is None:
        TEST_AUTHORITY = LIB.create_authority(
            name=TEST_AUTHORITY_NAME,
            description=TEST_AUTHORITY_DESCRIPTION,
            synonyms=TEST_AUTHORITY_SYNONYMS,
            url=TEST_AUTHORITY_URL
            )

    return TEST_AUTHORITY


def create_scope():
    """Creates & returns a test scope.

    """
    global TEST_SCOPE
    if TEST_SCOPE is None:
        TEST_SCOPE = LIB.create_scope(
            authority=TEST_AUTHORITY or create_authority(),
            name=TEST_SCOPE_NAME,
            description=TEST_SCOPE_DESCRIPTION,
            synonyms=TEST_SCOPE_SYNONYMS,
            url=TEST_SCOPE_URL
            )

    return TEST_SCOPE


def create_collection():
    """Creates & returns a test collection.

    """
    global TEST_COLLECTION
    if TEST_COLLECTION is None:
        TEST_COLLECTION = LIB.create_collection(
            scope=TEST_SCOPE or create_scope(),
            name=TEST_COLLECTION_NAME,
            description=TEST_COLLECTION_DESCRIPTION,
            synonyms=TEST_COLLECTION_SYNONYMS,
            url=TEST_COLLECTION_URL
            )

    return TEST_COLLECTION


def create_term(collection=None):
    """Creates & returns a test term.

    """
    global TEST_TERM
    if TEST_TERM is None:
        TEST_TERM = LIB.create_term(
            collection=collection or TEST_COLLECTION or create_collection(),
            name=TEST_TERM_NAME,
            description=TEST_TERM_DESCRIPTION,
            synonyms=TEST_TERM_SYNONYMS,
            url=TEST_TERM_URL
            )

    return TEST_TERM


def create_test_entities():
    """Returns tuple of test entities.

    """
    return \
        create_term(), \
        create_collection(), \
        create_scope(), \
        create_authority()


def init(func, desc=None):
    """Initializes a test function prior to be executed.

    """
    if desc is None:
        desc = inspect.getdoc(func)
    desc = desc.strip()
    if desc[-1] == '.':
        desc = desc[:-1]
    desc = desc[0].lower() + desc[1:]
    func.description = 'pyessv-tests: {}'.format(desc)


def setup():
    """Performs setup functions and then creates a term prior to running a test.

    """
    teardown()
    create_authority()
    create_scope()
    create_collection()
    create_term()
    cache(TEST_AUTHORITY)


def teardown():
    """Performs teardown functions after running a test.

    """
    global TEST_AUTHORITY
    global TEST_SCOPE
    global TEST_COLLECTION
    global TEST_TERM

    uncache(TEST_AUTHORITY)

    TEST_AUTHORITY = None
    TEST_SCOPE = None
    TEST_COLLECTION = None
    TEST_TERM = None

    try:
        shutil.rmtree(os.path.join(LIB.DIR_ARCHIVE, TEST_AUTHORITY_NAME))
    except OSError:
        pass


def assert_terms(term1, term2):
    """Assers equality of 2 terms.

    :param Term term1: A term to be compared against another.
    :param Term term2: A term to be compared against another.

    """
    assert_objects(term1, term2, LIB.Term)
    assert _get_object_attribute_values(term1) == _get_object_attribute_values(term1)


def _get_object_attribute_values(obj):
    """Returns collection of object attribute values.

    """
    return [getattr(obj, k) for k in dir(obj) if k not in dir(obj.__class__)]
