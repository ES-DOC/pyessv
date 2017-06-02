    # -*- coding: utf-8 -*-

"""
.. module:: write_bash_vars.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps raw WCRP CMIP6 vocab files to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import json
import os

import arrow

import pyessv



# Map of CMIP6 collections to data factories / name pre-formatters.
_VOCABS = {
    'cmip6': {
        'activity_id',
        'institution_id',
        'source_id'
        },
    'global': {
        'mip_era'
    }
}

_TEMPLATE = __file__.replace('.py', '_template.txt')
_OUTPUT = __file__.replace('.py', '_output.sh')


def _main():
    """Main entry point.

    """
    with open(_TEMPLATE, 'r') as fstream:
        content = fstream.read()

    # Create CMIP6 collections.
    for scope in _VOCABS:
        for collection in [pyessv.load('wcrp', scope, i) for i in _VOCABS[scope]]:
            data = ''
            for term in collection:
                data += '\t\'{}\'\n'.format(term.canonical_name)

            collection = '[{}]'.format(collection.raw_name.upper())

            content = content.replace(collection, data)


    with open(_OUTPUT, 'w') as fstream:
        fstream.write(content)


# Entry point.
if __name__ == '__main__':
    _main()
