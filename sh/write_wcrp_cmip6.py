    # -*- coding: utf-8 -*-

"""
.. module:: write_wcrp_cmip6.py
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



# Define command line options.
_ARGS = argparse.ArgumentParser('Maps raw WCRP CMIP6 vocab files to normalized pyessv CV format.')
_ARGS.add_argument(
    '--source',
    help='Path from which raw WCRP CMIP6 vocab files will be read.',
    dest='source',
    type=str
    )

# Ensure we use fixed creation date.
_CREATE_DATE = arrow.get('2017-03-21 00:00:00.000000+0000').datetime

# CV authority = WCRP.
_AUTHORITY = pyessv.create_authority(
    'WCRP',
    'World Climate Research Program',
    label='WCRP',
    url='https://www.wcrp-climate.org/wgcm-overview',
    create_date=_CREATE_DATE
    )

# CV scope = CMIP6.
_SCOPE_CMIP6 = pyessv.create_scope(_AUTHORITY,
    'CMIP6',
    'Controlled Vocabularies (CVs) for use in CMIP6',
    label='CMIP6',
    url='https://github.com/WCRP-CMIP/CMIP6_CVs',
    create_date=_CREATE_DATE
    )

# CV scope = GLOBAL.
_SCOPE_GLOBAL = pyessv.create_scope(_AUTHORITY,
    'GLOBAL',
    'Global controlled Vocabularies (CVs)',
    url='https://github.com/WCRP-CMIP/CMIP6_CVs',
    create_date=_CREATE_DATE
    )

# Map of CMIP6 collections to data factories / name pre-formatters.
_COLLECTIONS_CMIP6 = {
    'activity_id': {
        'data_factory': None
    },
    'experiment_id': {
        'data_factory': lambda obj, name: obj[name]
    },
    'frequency': {
        'data_factory': None
    },
    'grid_label': {
        'data_factory': None
    },
    'institution_id': {
        'data_factory': lambda obj, name: {'postal_address': obj[name]}
    },
    'nominal_resolution': {
        'data_factory': None,
        'term_regex': r'^[a-z0-9\-\.]*$'
    },
    'realm': {
        'data_factory': None
    },
    'required_global_attributes': {
        'data_factory': None
    },
    'source_id': {
        'data_factory': lambda obj, name: obj[name]
    },
    'source_type': {
        'data_factory': None
    },
    'table_id': {
        'data_factory': None
    }
}

# Map of CMIP6 collections to data factories / name pre-formatters.
_COLLECTIONS_GLOBAL = {
    'mip_era': {
        'data_factory': None
    }
}

def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.source):
        raise ValueError('WCRP vocab directory does not exist')

    # Create CMIP6 collections.
    for typeof, parsers in _COLLECTIONS_CMIP6.items():
        _create_collection_cmip6(args.source, typeof, parsers)

    # Create GLOBAL collections.
    for typeof, handlers in _COLLECTIONS_GLOBAL.items():
        _create_collection_global(args.source, typeof, parsers)

    # Add to the archive.
    pyessv.add(_AUTHORITY)

    # Save (to file system).
    pyessv.save()


def _create_collection_cmip6(source, collection_type, collection_info):
    """Creates cmip6 collection from a WCRP JSON files.

    """
    # Create collection.
    collection = pyessv.create_collection(
        _SCOPE_CMIP6,
        collection_type,
        "WCRP CMIP6 CV collection: ".format(collection_type),
        create_date=_CREATE_DATE,
        term_regex=collection_info.get('term_regex')
        )

    # Load WCRP json data.
    wcrp_cv_data = _get_wcrp_cv(source, collection_type, 'CMIP6_')

    # Create terms.
    data_factory = collection_info['data_factory']
    for name in wcrp_cv_data:
        pyessv.create_term(
            collection,
            name,
            label=name,
            create_date=_CREATE_DATE,
            data=data_factory(wcrp_cv_data, name) if data_factory else None
            )


def _create_collection_global(source, collection_type, parsers):
    """Creates global collection from a WCRP JSON files.

    """
    # Create collection.
    collection = pyessv.create_collection(
        _SCOPE_GLOBAL,
        collection_type,
        'WCRP GLOBAL CV collection: '.format(collection_type),
        create_date=_CREATE_DATE
        )

    # Unpack parsers.
    data_factory = parsers['data_factory']

    # Load WCRP json data.
    wcrp_cv_data = _get_wcrp_cv(source, collection_type)

    # Create terms.
    for name in wcrp_cv_data:
        pyessv.create_term(
            collection,
            name,
            create_date=_CREATE_DATE,
            data=data_factory(wcrp_cv_data, name) if data_factory else None
            )


def _get_wcrp_cv(source, collection_type, prefix=''):
    """Returns raw WCRP CV data.

    """
    fname = '{}{}.json'.format(prefix, collection_type)
    fpath = os.path.join(source, fname)
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())[collection_type]


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
