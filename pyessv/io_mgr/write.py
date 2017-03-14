# -*- coding: utf-8 -*-

"""
.. module:: pyessv.io.write.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Writes an authority's vocabularies to file sytem.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

from pyessv import validation
from pyessv.model import Authority
from pyessv.codecs import to_json


# Manifest file name.
_MANIFEST = "MANIFEST"


def write_authority(dpath, authority):
    """Writes authority CV data to file system.

    :param str dpath: Path to directory to which the CV will be written.
    :param pyessv.Authority authority: Authority class instance to be written to file-system.

    """
    # Validate inputs.
    if not os.path.isdir(dpath):
        raise OSError("Invalid directory.")
    if not isinstance(authority, Authority):
        raise ValueError("Invalid authority: unknown type")
    if not validation.is_valid(authority):
        raise ValueError("Invalid authority: has validation errors")

    # Set directory.
    dpath = os.path.join(dpath, authority.name)
    try:
        os.makedirs(dpath)
    except OSError:
        pass

    # Write manifest.
    with open(os.path.join(dpath, _MANIFEST), "w") as fstream:
        fstream.write(to_json(authority))

    # Write collections/terms.
    for scope in authority:
        for collection in scope:
            for term in collection:
                _write_term(dpath, term)


def _write_term(dpath, term):
    """Writes a term to the file system.

    """
    # Set directory.
    dpath = os.path.join(dpath, term.scope.name)
    dpath = os.path.join(dpath, term.collection.name)
    try:
        os.makedirs(dpath)
    except OSError:
        pass

    # Set file path.
    fpath = os.path.join(dpath, term.name)

    # Write term JSON file.
    with open(fpath, "w") as fstream:
        fstream.write(to_json(term))
