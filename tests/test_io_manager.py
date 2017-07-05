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
    authority_dir = os.path.join(LIB.DIR_ARCHIVE, tu.AUTHORITY_NAME)
    authority_manifest = os.path.join(authority_dir, 'MANIFEST')
    scope_dir = os.path.join(authority_dir, tu.SCOPE_NAME)
    collection_01_dir = os.path.join(scope_dir, tu.COLLECTION_01_NAME)
    collection_02_dir = os.path.join(scope_dir, tu.COLLECTION_02_NAME)
    collection_03_dir = os.path.join(scope_dir, tu.COLLECTION_03_NAME)
    term_01_file = os.path.join(collection_01_dir, tu.TERM_01_NAME)
    term_02_file = os.path.join(collection_02_dir, tu.TERM_02_NAME)
    term_03_file = os.path.join(collection_03_dir, tu.TERM_03_NAME)

    dpaths = (authority_dir, scope_dir, collection_01_dir, collection_02_dir, collection_03_dir)
    fpaths = (authority_manifest, term_01_file, term_02_file, term_03_file)

    for dpath in dpaths:
        assert not os.path.isdir(dpath)
    for fpath in fpaths:
        assert not os.path.isfile(fpath)

    write(LIB.load(tu.AUTHORITY_NAME))

    assert len(os.listdir(LIB.DIR_ARCHIVE)) == len(authority_dirs) + 1
    for dpath in dpaths:
        assert os.path.isdir(dpath)
    for fpath in fpaths:
        assert os.path.isfile(fpath)

    with io.open(authority_manifest, 'r') as fstream:
        assert isinstance(json.loads(fstream.read()), dict)
    for fpath in fpaths:
        with io.open(fpath, 'r') as fstream:
            assert isinstance(json.loads(fstream.read()), dict)


@nose.with_setup(tu.setup, tu.teardown)
def test_delete():
    """pyessv-tests: io: delete.

    """
    authority_dirs = os.listdir(LIB.DIR_ARCHIVE)
    authority_dir = os.path.join(LIB.DIR_ARCHIVE, tu.AUTHORITY_NAME)
    authority_manifest = os.path.join(authority_dir, 'MANIFEST')
    scope_dir = os.path.join(authority_dir, tu.SCOPE_NAME)
    collection_01_dir = os.path.join(scope_dir, tu.COLLECTION_01_NAME)
    collection_02_dir = os.path.join(scope_dir, tu.COLLECTION_02_NAME)
    collection_03_dir = os.path.join(scope_dir, tu.COLLECTION_03_NAME)
    term_01_file = os.path.join(collection_01_dir, tu.TERM_01_NAME)
    term_02_file = os.path.join(collection_02_dir, tu.TERM_02_NAME)
    term_03_file = os.path.join(collection_03_dir, tu.TERM_03_NAME)
    write(LIB.load(tu.AUTHORITY_NAMESPACE))

    for namespace, npath, predicate in (
        (tu.TERM_01_NAMESPACE, term_01_file, os.path.isfile),
        (tu.TERM_02_NAMESPACE, term_02_file, os.path.isfile),
        (tu.TERM_03_NAMESPACE, term_03_file, os.path.isfile),
        (tu.COLLECTION_01_NAMESPACE, collection_01_dir, os.path.isdir),
        (tu.COLLECTION_02_NAMESPACE, collection_02_dir, os.path.isdir),
        (tu.COLLECTION_03_NAMESPACE, collection_03_dir, os.path.isdir),
        (tu.SCOPE_NAMESPACE, scope_dir, os.path.isdir),
        (tu.AUTHORITY_NAMESPACE, authority_dir, os.path.isdir),
        ):
        node = LIB.load(namespace)
        delete(node)
        assert not predicate(npath)
