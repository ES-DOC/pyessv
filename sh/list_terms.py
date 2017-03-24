    # -*- coding: utf-8 -*-

"""
.. module:: list_terms.py.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Lists an authority's vocabulary entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse

import pyessv



# Define command line options.
_ARGS = argparse.ArgumentParser("Writes an authority's vocabularies to stdout.")
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
    if args.authority is None or len(args.authority.strip()) == 0:
        raise ValueError("Authority is a required parameter")

    for scope in pyessv.load(args.authority):
        if args.scope and args.scope != scope.name:
            continue
        for collection in scope:
            if args.collection and args.collection != collection.name:
                continue
            for term in collection:
                print term.namespace.replace(":", " -> ")


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
