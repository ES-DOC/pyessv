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
_CREATE_DATE = arrow.get('2017-06-21 00:00:00.000000+0000').datetime

# CMIP6 institutional data.
with open(os.path.join(os.path.dirname(__file__), 'institution_id.json')) as fstream:
    _INSTITUTIONAL_DATA = json.loads(fstream.read())
    _INSTITUTIONAL_DATA = {i['code']: i for i in _INSTITUTIONAL_DATA}

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

# Map of scopes to collections.
_SCOPE_COLLECTIONS = {
    _SCOPE_CMIP6: {
        'activity_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': 'Activity',
            'ommitted': [],
            'term_regex': None
        },
        'experiment_id': {
            'cim_document_type': 'cim.2.designing.NumericalExperiment',
            'cim_document_type_alternative_name': 'experiment',
            'data_factory': lambda obj, name: obj[name],
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'frequency': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'grid_label': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'institution_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': lambda obj, name: _get_institution_data(obj, name),
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'member_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': True,
            'label': None,
            'ommitted': [],
            'term_regex': r'(s[0-9]{4}-)?r[0-9]+i[0-9]+p[0-9]+f[0-9]+',
        },
        'nominal_resolution': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': r'^[a-z0-9\-\.]*$'
        },
        'realm': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': lambda obj, name: {'description': obj[name]},
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'required_global_attributes': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'source_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': lambda obj, name: obj[name],
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'source_type': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'sub_experiment_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': lambda obj, name: {'description': obj[name]},
            'is_virtual': False,
            'label': None,
            'ommitted': ['none'],
            'term_regex': None
        },
        'table_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        },
        'variable_id': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': True,
            'label': None,
            'ommitted': [],
            'term_regex': r'^[A-Za-z0-9]*$',
        },
        'version': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': True,
            'label': None,
            'ommitted': [],
            'term_regex': r'^[0-9]{8}$',
        }
    },
    _SCOPE_GLOBAL: {
        'mip_era': {
            'cim_document_type': None,
            'cim_document_type_alternative_name': None,
            'data_factory': None,
            'is_virtual': False,
            'label': None,
            'ommitted': [],
            'term_regex': None
        }
    }
}


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.source):
        raise ValueError('WCRP vocab directory does not exist')

    # Create collections.
    for scope in _SCOPE_COLLECTIONS:
        for collection in _SCOPE_COLLECTIONS[scope]:
            cfg = _SCOPE_COLLECTIONS[scope][collection]
            _create_collection(args.source, scope, collection, cfg)

    # Add to archive & persist to file system.
    pyessv.archive(_AUTHORITY)


def _create_collection(source, scope, collection_id, cfg):
    """Creates collection from a WCRP JSON file.

    """
    # Create collection.
    if collection_id.lower().replace('_', '-') in [collection.name for collection in scope.collections]:
        collection = scope[collection_id]
        collection.description = "WCRP CMIP6 CV collection: ".format(collection_id),
        collection.label = cfg['label'] or collection_id.title().replace('_Id', '_ID').replace('_', ' '),
        collection.create_date = _CREATE_DATE,
        collection.term_regex = cfg['term_regex'] or pyessv.REGEX_CANONICAL_NAME,
        collection.data = None if cfg['cim_document_type'] is None else {
                'cim_document_type': cfg['cim_document_type'],
                'cim_document_type_alternative_name': cfg['cim_document_type_alternative_name']
            }
    else:
        collection = pyessv.create_collection(
            scope,
            collection_id,
            "WCRP CMIP6 CV collection: ".format(collection_id),
            label=cfg['label'] or collection_id.title().replace('_Id', '_ID').replace('_', ' '),
            create_date=_CREATE_DATE,
            term_regex=cfg['term_regex'] or pyessv.REGEX_CANONICAL_NAME,
            data = None if cfg['cim_document_type'] is None else {
                'cim_document_type': cfg['cim_document_type'],
                'cim_document_type_alternative_name': cfg['cim_document_type_alternative_name']
                }
            )

    # Load JSON data & create terms (if collection is not a virtual one).
    if cfg['is_virtual'] == False:
        cv_data = _get_wcrp_cv(source, scope, collection_id)
        data_factory = cfg['data_factory']
        for term_name in [i for i in cv_data if i not in cfg['ommitted']]:
            term_data = data_factory(cv_data, term_name) if data_factory else None
            _create_term(collection, term_name, term_data)


def _create_term(collection, raw_name, data):
    """Creates & returns a new term.

    """
    try:
        description = data['description']
    except (TypeError, KeyError):
        description = None
    else:
        del data['description']

    try:
        label = data['label']
    except (TypeError, KeyError):
        label = raw_name
    else:
        del data['label']

    term = pyessv.create_term(
        collection,
        raw_name,
        description=description,
        label=label,
        create_date=_CREATE_DATE,
        data=data
        )


def _get_wcrp_cv(source, scope, collection_id):
    """Returns raw WCRP CV data.

    """
    prefix = 'CMIP6_' if scope.canonical_name == 'cmip6' else ''
    fname = '{}{}.json'.format(prefix, collection_id)
    fpath = os.path.join(source, fname)
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())[collection_id]


def _get_institution_data(_, name):
    """Returns data related to an institution.

    """
    obj = _INSTITUTIONAL_DATA.get(name, {})
    del obj['code']

    return obj


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
