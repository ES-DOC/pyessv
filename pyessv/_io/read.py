# -*- coding: utf-8 -*-

"""
.. module:: pyessv.io.read.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Reads an authority's vocabularies from file sytem.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import glob
import os

from pyessv._codecs import decode
from pyessv._constants import ENCODING_JSON


# Manifest file name.
_MANIFEST = "MANIFEST"


def read_authority(dpath):
    """Reads authority CV data from file system.

    :param str dpath: Path to directory to which a CV hierarchy has been written.

    :returns: Authority CV data.
    :rtype: pyessv.Authority

    """
    if not os.path.isdir(dpath):
        raise OSError("Invalid directory.")
    if not os.path.isfile(os.path.join(dpath, _MANIFEST)):
        raise OSError("Invalid MANIFEST.")

    # Read authority from manifest.
    fpath = os.path.join(dpath, _MANIFEST)
    with open(fpath, "r") as fstream:
        authority = decode(fstream.read(), ENCODING_JSON)
        authority.io_path = fpath

    # Read terms.
    term_cache = {}
    for scope in authority:
        for collection in scope:
            collection.terms = _read_terms(dpath, scope, collection, term_cache)

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
    dpath = os.path.join(dpath, scope.name)
    dpath = os.path.join(dpath, collection.name)
    dpath = os.path.join(dpath, "*")

    return [_read_term(i, collection, term_cache) for i in glob.iglob(dpath)]


def _read_term(fpath, collection, term_cache):
    """Reads terms from file system.

    """
    # Decode term from JSON file.
    with open(fpath, "r") as fstream:
        term = decode(fstream.read(), ENCODING_JSON)
    term.collection = collection
    term.io_path = fpath

    term_cache[term.uid] = term

    return term
