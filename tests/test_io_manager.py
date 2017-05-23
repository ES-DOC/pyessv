# -*- coding: utf-8 -*-

"""
.. module:: test_io_manager.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv I/O tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import io
import json
import nose
import os

import pyessv as LIB
from pyessv._io_manager import delete
from pyessv._io_manager import read
from pyessv._io_manager import write
import tests.utils as tu



def test_interface():
    """pyessv-tests: io: interface.

    """
    assert inspect.isfunction(delete)
    assert inspect.isfunction(read)
    assert inspect.isfunction(write)


def test_directory():
    """pyessv-tests: io: directory.

    """
    assert os.path.isdir(LIB.DIR_ARCHIVE)


def test_read():
    """pyessv-tests: io: read.

    """
    authorities = read()
    assert isinstance(authorities, list)
    for authority in authorities:
        assert isinstance(authority, LIB.Authority)

    dirs = os.listdir(LIB.DIR_ARCHIVE)
    assert len(authorities) == len(dirs)
    assert dirs == [i.canonical_name for i in authorities]


@nose.with_setup(tu.setup, tu.teardown)
def test_write():
    """pyessv-tests: io: write.

    """
    authority_dirs = os.listdir(LIB.DIR_ARCHIVE)
    authority_dir = os.path.join(LIB.DIR_ARCHIVE, tu.TEST_AUTHORITY_NAME)
    authority_manifest = os.path.join(authority_dir, 'MANIFEST')
    scope_dir = os.path.join(authority_dir, tu.TEST_SCOPE_NAME)
    collection_dir = os.path.join(scope_dir, tu.TEST_COLLECTION_NAME)
    term_file = os.path.join(collection_dir, tu.TEST_TERM_NAME)

    assert not os.path.isdir(authority_dir)
    assert not os.path.isfile(authority_manifest)
    assert not os.path.isdir(scope_dir)
    assert not os.path.isdir(collection_dir)
    assert not os.path.isfile(term_file)

    write(LIB.load(tu.TEST_AUTHORITY_NAME))
    assert len(os.listdir(LIB.DIR_ARCHIVE)) == len(authority_dirs) + 1

    assert os.path.isdir(authority_dir)
    assert os.path.isfile(authority_manifest)
    assert os.path.isdir(scope_dir)
    assert os.path.isdir(collection_dir)
    assert os.path.isfile(term_file)
    with io.open(authority_manifest, 'r') as fstream:
        assert isinstance(json.loads(fstream.read()), dict)
    with io.open(term_file, 'r') as fstream:
        assert isinstance(json.loads(fstream.read()), dict)


@nose.with_setup(tu.setup, tu.teardown)
def test_delete():
    """pyessv-tests: io: delete.

    """
    authority_dir = os.path.join(LIB.DIR_ARCHIVE, tu.TEST_AUTHORITY_NAME)
    scope_dir = os.path.join(authority_dir, tu.TEST_SCOPE_NAME)
    collection_dir = os.path.join(scope_dir, tu.TEST_COLLECTION_NAME)
    term_file = os.path.join(collection_dir, tu.TEST_TERM_NAME)

    write(LIB.load(tu.TEST_AUTHORITY_NAMESPACE))

    authority, scope, collection, term = \
        LIB.load(tu.TEST_AUTHORITY_NAMESPACE), \
        LIB.load(tu.TEST_SCOPE_NAMESPACE), \
        LIB.load(tu.TEST_COLLECTION_NAMESPACE), \
        LIB.load(tu.TEST_TERM_NAMESPACE) \

    delete(term)
    assert not os.path.isfile(term_file)
    delete(collection)
    assert not os.path.isfile(collection_dir)
    delete(scope)
    assert not os.path.isfile(scope_dir)
    delete(authority)
    assert not os.path.isdir(collection_dir)
    assert not os.path.isdir(scope_dir)
    assert not os.path.isdir(authority_dir)
