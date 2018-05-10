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
from pyessv._cache import uncache
from tests.utils_assert import assert_objects


# Test authority.
AUTHORITY = None
AUTHORITY_DESCRIPTION = 'authority-description'
AUTHORITY_NAME = 'authority'
AUTHORITY_NAMESPACE = AUTHORITY_NAME
AUTHORITY_ALTERNATIVE_NAMES = ['authority-alternative-name-1', 'authority-alternative-name-2']
AUTHORITY_URL = 'https://github.com/ES-DOC/pyesssv-archive/{}'.format(AUTHORITY_NAME)


def create_authority():
    """Creates & returns a test authority.

    """
    global AUTHORITY

    if AUTHORITY is not None:
        return AUTHORITY

    AUTHORITY = LIB.create_authority(
        name=AUTHORITY_NAME,
        description=AUTHORITY_DESCRIPTION,
        alternative_names=AUTHORITY_ALTERNATIVE_NAMES,
        url=AUTHORITY_URL
        )
    create_scope()

    return AUTHORITY


# Test scope.
SCOPE = None
SCOPE_DESCRIPTION = 'scope-description'
SCOPE_NAME = 'scope'
SCOPE_NAMESPACE = ":".join([AUTHORITY_NAME, SCOPE_NAME])
SCOPE_ALTERNATIVE_NAMES = ['scope-alternative-name-1', 'scope-alternative-name-2']
SCOPE_URL = '{}/{}'.format(AUTHORITY_URL, SCOPE_NAME)


def create_scope():
    """Creates & returns a test scope.

    """
    global SCOPE

    if SCOPE is not None:
        return SCOPE

    SCOPE = LIB.create_scope(
        authority=AUTHORITY or create_authority(),
        name=SCOPE_NAME,
        description=SCOPE_DESCRIPTION,
        alternative_names=SCOPE_ALTERNATIVE_NAMES,
        url=SCOPE_URL
        )
    create_collection_01()
    create_collection_02()
    create_collection_03()

    return SCOPE


# Test collection - 01.
COLLECTION_01 = None
COLLECTION_01_DESCRIPTION = 'collection-01-description'
COLLECTION_01_NAME = 'collection-01'
COLLECTION_01_NAMESPACE = ":".join([AUTHORITY_NAME, SCOPE_NAME, COLLECTION_01_NAME])
COLLECTION_01_ALTERNATIVE_NAMES = ['collection-01-alternative-name-1', 'collection-01-alternative-name-2']
COLLECTION_01_URL = '{}/{}'.format(SCOPE_URL, COLLECTION_01_NAME)


def create_collection_01():
    """Creates & returns a test collection.

    """
    global COLLECTION_01

    if COLLECTION_01 is not None:
        return COLLECTION_01

    COLLECTION_01 = LIB.create_collection(
        scope=SCOPE or create_scope(),
        name=COLLECTION_01_NAME,
        description=COLLECTION_01_DESCRIPTION,
        alternative_names=COLLECTION_01_ALTERNATIVE_NAMES,
        url=COLLECTION_01_URL
        )
    create_term_01()

    return COLLECTION_01


# Test collection - 02.
COLLECTION_02 = None
COLLECTION_02_DESCRIPTION = 'collection-02-description'
COLLECTION_02_NAME = 'collection-02'
COLLECTION_02_NAMESPACE = ":".join([AUTHORITY_NAME, SCOPE_NAME, COLLECTION_02_NAME])
COLLECTION_02_ALTERNATIVE_NAMES = ['collection-02-alternative-name-1', 'collection-02-alternative-name-2']
COLLECTION_02_TERM_REGEX = r'^[A-z0-9\-]*$'
COLLECTION_02_URL = '{}/{}'.format(SCOPE_URL, COLLECTION_02_NAME)


def create_collection_02():
    """Creates & returns a test collection.

    """
    global COLLECTION_02

    if COLLECTION_02 is not None:
        return COLLECTION_02

    COLLECTION_02 = LIB.create_collection(
        scope=SCOPE or create_scope(),
        name=COLLECTION_02_NAME,
        description=COLLECTION_02_DESCRIPTION,
        alternative_names=COLLECTION_02_ALTERNATIVE_NAMES,
        term_regex=COLLECTION_02_TERM_REGEX,
        url=COLLECTION_02_URL
        )
    create_term_02()

    return COLLECTION_02


# Test composite collection.
COLLECTION_03 = None
COLLECTION_03_DESCRIPTION = 'collection-03-description'
COLLECTION_03_NAME = 'collection-03'
COLLECTION_03_NAMESPACE = ":".join([AUTHORITY_NAME, SCOPE_NAME, COLLECTION_03_NAME])
COLLECTION_03_ALTERNATIVE_NAMES = ['collection-03-alternative-name-1', 'collection-03-alternative-name-2']
COLLECTION_03_TERM_REGEX = r'^[A-z0-9\-]*$'
COLLECTION_03_URL = '{}/{}'.format(SCOPE_URL, COLLECTION_03_NAME)


def create_collection_03():
    """Creates & returns a test collection.

    """
    global COLLECTION_03

    if COLLECTION_03 is not None:
        return COLLECTION_03

    COLLECTION_03 = LIB.create_collection(
        scope=SCOPE or create_scope(),
        name=COLLECTION_03_NAME,
        description=COLLECTION_03_DESCRIPTION,
        alternative_names=COLLECTION_03_ALTERNATIVE_NAMES,
        term_regex=COLLECTION_03_TERM_REGEX,
        url=COLLECTION_03_URL
        )
    create_term_03()

    return COLLECTION_03


# Test term - 01.
TERM_01 = None
TERM_01_DESCRIPTION = 'term-01-description'
TERM_01_NAME = 'term-01'
TERM_01_NAMESPACE = ":".join([AUTHORITY_NAME, SCOPE_NAME, COLLECTION_01_NAME, TERM_01_NAME])
TERM_01_ALTERNATIVE_NAMES = ['term-01-alternative-name-1', 'term-01-alternative-name-2']
TERM_01_URL = '{}/{}'.format(COLLECTION_01_URL, TERM_01_NAME)


def create_term_01(collection=None):
    """Creates & returns a test term.

    """
    global TERM_01

    if TERM_01 is not None:
        return TERM_01

    TERM_01 = LIB.create_term(
        collection=collection or COLLECTION_01 or create_collection_01(),
        name=TERM_01_NAME,
        description=TERM_01_DESCRIPTION,
        alternative_names=TERM_01_ALTERNATIVE_NAMES,
        url=TERM_01_URL
        )

    return TERM_01


# Test term - 02.
TERM_02 = None
TERM_02_DESCRIPTION = 'term-02-description'
TERM_02_NAME = 'term-02'
TERM_02_NAMESPACE = ":".join([AUTHORITY_NAME, SCOPE_NAME, COLLECTION_02_NAME, TERM_02_NAME])
TERM_02_ALTERNATIVE_NAMES = ['term-02-alternative-name-1', 'term-02-alternative-name-2']
TERM_02_URL = '{}/{}'.format(COLLECTION_02_URL, TERM_02_NAME)


def create_term_02(collection=None):
    """Creates & returns a test term.

    """
    global TERM_02

    if TERM_02 is not None:
        return TERM_02

    TERM_02 = LIB.create_term(
        collection=collection or COLLECTION_02 or create_collection_02(),
        name=TERM_02_NAME,
        description=TERM_02_DESCRIPTION,
        alternative_names=TERM_02_ALTERNATIVE_NAMES,
        url=TERM_02_URL
        )

    return TERM_02


# Test term - 03.
TERM_03 = None
TERM_03_DESCRIPTION = 'term-03-description'
TERM_03_NAME = '{}-TESTING-{}'.format(TERM_01_NAME, TERM_02_NAME)
TERM_03_NAMESPACE = ":".join([AUTHORITY_NAME, SCOPE_NAME, COLLECTION_03_NAME, TERM_03_NAME])
TERM_03_ALTERNATIVE_NAMES = ['term-03-alternative-name-1', 'term-03-alternative-name-2']
TERM_03_URL = '{}/{}'.format(COLLECTION_03_URL, TERM_03_NAME)


def create_term_03(collection=None):
    """Creates & returns a test term.

    """
    global TERM_03

    if TERM_03 is not None:
        return TERM_03

    TERM_03 = LIB.create_term(
        collection=collection or COLLECTION_03 or create_collection_03(),
        name=TERM_03_NAME,
        description=TERM_03_DESCRIPTION,
        alternative_names=TERM_03_ALTERNATIVE_NAMES,
        url=TERM_03_URL
        )

    return TERM_03


def create_test_entities():
    """Returns tuple of test entities.

    """
    return \
        create_term_01(), \
        create_term_02(), \
        create_term_03(), \
        create_collection_01(), \
        create_collection_02(), \
        create_collection_03(), \
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
    """Initialises test objects.

    """
    teardown()
    for func in (
        create_authority,
        create_scope,
        create_collection_01,
        create_collection_02,
        create_collection_03,
        create_term_01,
        create_term_02,
        create_term_03
        ):
        func()


def teardown():
    """Performs teardown functions after running a test.

    """
    global AUTHORITY
    global SCOPE
    global COLLECTION_01
    global COLLECTION_02
    global COLLECTION_03
    global TERM_01
    global TERM_02
    global TERM_03

    uncache(AUTHORITY)

    AUTHORITY = None
    SCOPE = None
    COLLECTION_01 = None
    COLLECTION_02 = None
    COLLECTION_03 = None
    TERM_01 = None
    TERM_02 = None
    TERM_03 = None

    try:
        shutil.rmtree(os.path.join(LIB.DIR_ARCHIVE, AUTHORITY_NAME))
    except OSError:
        pass
