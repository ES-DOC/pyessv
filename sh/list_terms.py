    # -*- coding: utf-8 -*-

"""
.. module:: write_cv.py.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps raw WCRP CMIP6 vocab files to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os

import pyessv


# Define command line options.
_ARGS = argparse.ArgumentParser("Writes to stdout an authority's vocabularies.")
_ARGS.add_argument(
    "--source",
    help="Archive path.",
    dest="source",
    type=str
    )
_ARGS.add_argument(
    "--authority",
    help="Authority to be displayed.",
    dest="authority",
    type=str
    )
_ARGS.add_argument(
    "--scope",
    help="scope to be displayed.",
    dest="scope",
    type=str,
    default=None
    )
_ARGS.add_argument(
    "--collection",
    help="Collection to be displayed.",
    dest="collection",
    type=str,
    default=None
    )


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.source):
        raise ValueError("Archive directory does not exist")

    pyessv.archive.set_directory(args.source)

    authority = pyessv.archive.load_authority(args.authority)
    for scope in authority:
        if args.scope and args.scope != scope.name:
            continue
        for collection in scope:
            if args.collection and args.collection != collection.name:
                continue
            for term in collection:
                print authority.name, "->", scope.name, "->", collection.name, "->", term.name


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
