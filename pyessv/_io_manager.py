# -*- coding: utf-8 -*-

"""
.. module:: pyessv._io_manager.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: I/O manager.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import glob
import io
import os
import shutil
from os.path import join
from os.path import isdir
from os.path import isfile

from pyessv._codecs import decode
from pyessv._codecs import encode
from pyessv._constants import DIR_ARCHIVE
from pyessv._constants import ENCODING_JSON
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._model import Term
from pyessv._model import Node
from pyessv._validation import is_valid



# Manifest file name.
_MANIFEST = 'MANIFEST'


def delete(target):
    """Deletes vocabulary data from file system.

    """
    if not isinstance(target, Node):
        raise TypeError()

    elif isinstance(target, Authority):
        action = shutil.rmtree
        io_path = join(DIR_ARCHIVE, target.io_name)

    elif isinstance(target, Scope):
        action = shutil.rmtree
        io_path = join(DIR_ARCHIVE, target.authority.io_name)
        io_path = join(io_path, target.io_name)

    elif isinstance(target, Collection):
        action = shutil.rmtree
        io_path = join(DIR_ARCHIVE, target.authority.io_name)
        io_path = join(io_path, target.scope.io_name)
        io_path = join(io_path, target.io_name)

    elif isinstance(target, Term):
        action = os.remove
        io_path = join(DIR_ARCHIVE, target.authority.io_name)
        io_path = join(io_path, target.scope.io_name)
        io_path = join(io_path, target.collection.io_name)
        io_path = join(io_path, target.io_name)

    try:
        action(io_path)
    except OSError:
        pass


def read(archive_dir=DIR_ARCHIVE):
    """Reads vocabularies from archive folder (~/.esdoc/pyessv-archive) upon file system.

    :returns: List of vocabulary authorities loaded from archive folder.
    :rtype: list

    """
    return [_read_authority(i) for i in glob.glob('{}/*'.format(archive_dir)) if isdir(i)]


def _read_authority(dpath):
    """Reads authority CV data from file system.

    :param str dpath: Path to a directory to which an authority's vocabularies have been written.

    :returns: Authority vocabulary data.
    :rtype: pyessv.Authority

    """
    assert isfile(join(dpath, _MANIFEST)), 'Invalid authority MANIFEST: {}/MANIFEST'.format(dpath)

    # Read authority from manifest.
    fpath = join(dpath, _MANIFEST)
    with open(fpath, 'r') as fstream:
        authority = decode(fstream.read(), ENCODING_JSON)

    # Read terms.
    term_cache = {}
    for scope in authority:
        for collection in scope:
            for term in _read_terms(dpath, scope, collection, term_cache):
                term.collection = collection
                collection.terms.append(term)

    # Set inter-term hierarchies.
    for term in term_cache.values():
        if term.parent in term_cache:
            term.parent = term_cache[term.parent]

    # Set intra-term hierarchies.
    for term in [i for i in term_cache.values() if i.associations]:
        term.associations = [term_cache[i] if i in term_cache else i for i in term.associations]

    return authority


def _read_terms(dpath, scope, collection, term_cache):
    """Reads terms from file system.

    """
    dpath = join(dpath, scope.io_name)
    dpath = join(dpath, collection.io_name)
    dpath = join(dpath, '*')

    return [_read_term(i, collection, term_cache) for i in glob.iglob(dpath)]


def _read_term(fpath, collection, term_cache):
    """Reads terms from file system.

    """
    with open(fpath, 'r') as fstream:
        term = decode(fstream.read(), ENCODING_JSON)
    term.collection = collection

    term_cache[term.uid] = term

    return term


def write(authority, archive_dir=DIR_ARCHIVE):
    """Writes authority CV data to file system.

    :param pyessv.Authority authority: Authority class instance to be written to file-system.

    """
    # Validate inputs.
    assert isinstance(authority, Authority), 'Invalid authority: unknown type'
    assert isdir(archive_dir), 'Invalid authority directory.'
    assert is_valid(authority), 'Invalid authority: has validation errors'

    # Set directory.
    dpath = join(archive_dir, authority.io_name)
    try:
        os.makedirs(dpath)
    except OSError:
        pass

    # Write manifest.
    with open(join(dpath, _MANIFEST), 'w') as fstream:
        fstream.write(encode(authority))

    # Write collections/terms.
    for scope in authority:
        for collection in scope:
            for term in collection:
                _write_term(dpath, term)


def _write_term(dpath, term):
    """Writes a term to the file system.

    """
    # Set directory.
    dpath = join(dpath, term.scope.io_name)
    dpath = join(dpath, term.collection.io_name)
    try:
        os.makedirs(dpath)
    except OSError:
        pass

    # Set file path.
    fpath = join(dpath, term.io_name)

    # Write term JSON file.
    with open(fpath, 'w') as fstream:
        fstream.write(encode(term))
