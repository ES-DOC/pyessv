    # -*- coding: utf-8 -*-

"""
.. module:: write_cv.py.py
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
_AUTHORITY = pyessv.create_authority('wcrp',
    description='World Climate Research Program',
    label='WCRP',
    url='https://www.wcrp-climate.org/wgcm-overview',
    create_date=_CREATE_DATE
    )

# CV scope = CMIP6.
_SCOPE_CMIP6 = pyessv.create_scope('cmip6', _AUTHORITY,
    description='Controlled Vocabularies (CVs) for use in CMIP6',
    label='CMIP6',
    url='https://github.com/WCRP-CMIP/CMIP6_CVs',
    create_date=_CREATE_DATE
    )

# CV scope = GLOBAL.
_SCOPE_GLOBAL = pyessv.create_scope('global', _AUTHORITY,
    description='Global controlled Vocabularies (CVs)',
    url='https://github.com/WCRP-CMIP/CMIP6_CVs',
    create_date=_CREATE_DATE
    )

# Map of CMIP6 collections to data factories / name pre-formatters.
_COLLECTIONS_CMIP6 = {
    'activity_id': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'experiment_id': {
        'data_factory': lambda obj, name: obj[name],
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'frequency': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'grid_label': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'institution_id': {
        'data_factory': lambda obj, name: {'postal_address': obj[name]},
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'nominal_resolution': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'realm': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'required_global_attributes': {
        'data_factory': None,
        'name_preformatter': None
    },
    'source_id': {
        'data_factory': lambda obj, name: obj[name] ,
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'source_type': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
    },
    'table_id': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
    }
}

# Map of CMIP6 collections to data factories / name pre-formatters.
_COLLECTIONS_GLOBAL = {
    'mip_era': {
        'data_factory': None,
        'name_preformatter': lambda n: _reformat_name(n)
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


def _create_collection_cmip6(source, collection_type, parsers):
    """Creates cmip6 collection from a WCRP JSON files.

    """
    # Create collection.
    collection_name = _reformat_name(collection_type)
    collection = pyessv.create_collection(collection_name, _SCOPE_CMIP6,
        description="WCRP CMIP6 CV collection: ".format(collection_name),
        create_date=_CREATE_DATE
        )

    # Unpack parsers.
    data_factory = parsers['data_factory']
    name_preformatter = parsers['name_preformatter']

    # Load WCRP json data.
    wcrp_cv_data = _get_wcrp_cv(source, collection_type, 'CMIP6_')

    # Create terms.
    for label in wcrp_cv_data:
        name = name_preformatter(label) if name_preformatter else label
        pyessv.create_term(name, collection,
            label=label,
            description=label,
            create_date=_CREATE_DATE,
            data=data_factory(wcrp_cv_data, label) if data_factory else None
            )


def _create_collection_global(source, collection_type, parsers):
    """Creates global collection from a WCRP JSON files.

    """
    # Create collection.
    name = _reformat_name(collection_type)
    collection = pyessv.create_collection(name, _SCOPE_GLOBAL,
        description='WCRP GLOBAL CV collection: '.format(collection_type),
        create_date=_CREATE_DATE
        )

    # Unpack parsers.
    data_factory = parsers['data_factory']
    name_preformatter = parsers['name_preformatter']

    # Load WCRP json data.
    wcrp_cv_data = _get_wcrp_cv(source, collection_type)

    # Create terms.
    for label in wcrp_cv_data:
        name = name_preformatter(label) if name_preformatter else label
        pyessv.create_term(name, collection,
            description=label,
            create_date=_CREATE_DATE,
            data=data_factory(wcrp_cv_data, label) if data_factory else None
            )


def _get_wcrp_cv(source, collection_type, prefix=''):
    """Returns raw WCRP CV data.

    """
    fname = '{}{}.json'.format(prefix, collection_type)
    fpath = os.path.join(source, fname)
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())[collection_type]


def _reformat_name(name):
    """Reformats a name.

    """
    return str(name).lower().replace("_", "-")


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
