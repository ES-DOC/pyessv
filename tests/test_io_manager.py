# -*- coding: utf-8 -*-

"""
.. module:: testio_manager.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv I/O tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import io
import json
import os

import pytest

import pyessv as LIB
from pyessv import io_manager
from pyessv.io_manager import write
import tests.utils as tu


# Module level fixture teardown.
teardown_module = tu.teardown

# Module level fixture teardown.
setup_module = tu.setup


def test_interface():
    """pyessv-tests: io: interface.

    """
    assert inspect.isfunction(io_manager.delete)
    assert inspect.isfunction(io_manager.read)
    assert inspect.isfunction(io_manager.write)


def test_directory():
    """pyessv-tests: io: directory.

    """
    assert os.path.isdir(LIB.DIR_ARCHIVE)


def test_read_all():
    """pyessv-tests: io: read.

    """
    authorities = io_manager.read()
    assert isinstance(authorities, list)
    for authority in authorities:
        assert isinstance(authority, LIB.Authority)

    dirs = [i for i in os.listdir(LIB.DIR_ARCHIVE) if not (i.startswith('.') or i.startswith("README") or i.endswith("_parsers"))]
    assert len(authorities) == len(dirs)
    assert dirs == [i.canonical_name for i in authorities]


def test_read_one_authority():
    """pyessv-tests: io: read one authority.

    """
    assert isinstance(io_manager.read(authority="wcrp"), LIB.Authority)


def test_read_one_scope():
    """pyessv-tests: io: read one scope.

    """
    authority = io_manager.read(authority="wcrp", scope="cmip6")
    assert isinstance(authority, LIB.Authority)
    assert len(authority) == 1


def test_read_one_negative():
    """pyessv-tests: io: read one (negative).

    """
    with pytest.raises(IOError):
        io_manager.read(authority="xxx")


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

    io_manager.write(LIB.load(tu.AUTHORITY_NAME))

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
    io_manager.write(LIB.load(tu.AUTHORITY_NAMESPACE))

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
        io_manager.delete(node)
        assert not predicate(npath)
