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
    for scope in authority:
        for collection in scope:
            collection.terms = []
            collection.terms += _read_terms(dpath, scope, collection)

    # Set inter-concept hierachy.
    terms = {}
    for scope in authority:
        scope.authority = authority
        for collection in scope:
            collection.scope = scope
            for term in collection:
                term.collection = collection
                terms[term.uid] = term

    # Set inter-term hierarchies.
    for term in terms.values():
        if term.parent in terms:
            term.parent = terms[term.parent]

    # Set intra-term hierarchies.
    for term in [i for i in terms.values() if i.associations]:
        term.associations = [terms[i] if i in terms else i for i in term.associations]

    return authority


def _read_terms(dpath, scope, collection):
    """Reads terms from file system.

    """
    dpath = os.path.join(dpath, scope.name)
    dpath = os.path.join(dpath, collection.name)
    dpath = os.path.join(dpath, "*")

    return [_read_term(i) for i in glob.iglob(dpath)]


def _read_term(fpath):
    """Reads terms from file system.

    """
    # Decode term from JSON file.
    with open(fpath, "r") as fstream:
        term = decode(fstream.read(), ENCODING_JSON)
    term.io_path = fpath

    return term
