# -*- coding: utf-8 -*-

"""
.. module:: map.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps raw ESGF CMIP6 ini config file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import inspect
import os
from ConfigParser import ConfigParser

import arrow
import pyessv

import map_c3s_cmip5
import map_c3s_cordex
import map_cc4e
import map_cmip5
import map_cmip6
import map_cordex
import map_cordex_adjust
import map_euclipse
import map_geomip
import map_input4mips
import map_isimip_ft
import map_lucid
import map_obs4mips
import map_pmip3
import map_primavera
import map_tamip

# Define command line options.
_ARGS = argparse.ArgumentParser('Maps ESGF publisher ini files to normalized pyessv vocabulary format.')
_ARGS.add_argument(
    '--source',
    help='Directory within which ESGF publisher ini files will be read.',
    dest='source',
    default='/Users/glipsl/Documents/work/esgf-config/publisher-configs/ini',
    type=str
    )

# Ensure we use fixed creation date.
_CREATE_DATE = arrow.get('2019-04-02 00:00:00.000000+0000').datetime

# Set of mapping modules.
_MODULES = {
    map_c3s_cmip5,
    map_c3s_cordex,
    map_cc4e,
    map_cmip5,
    map_cmip6,
    map_cordex,
    map_cordex_adjust,
    map_euclipse,
    map_geomip,
    map_input4mips,
    map_isimip_ft,
    map_lucid,
    map_obs4mips,
    map_pmip3,
    map_primavera,
    map_tamip
    }


def _main(args):
    """Main entry point.

    """
    if not os.path.isdir(args.source):
        raise ValueError('ESGF vocab directory does not exist: {}'.format(args.source))

    # CV authority = ECMWF.
    #_AUTHORITY = pyessv.create_authority(
    #    'ECMWF',
    #    'European Center for Medium-Range Weather Forecasts',
    #    label='ECMWF',
    #    url='https://www.ecmwf.int/',
    #    create_date=_CREATE_DATE
    #)

    # Process project modules:
    for module in _MODULES:
        # Set project.
        project = module.__name__[4:].replace('_','-')

        # Set ini file handler.
        ini_section = _IniSection(project, args.source)

        # Load authority & create scope.
        if project in ['cc4e', 'c3s-cmip5', 'c3s-cordex']:
            authority = pyessv.load('ecmwf')
            scope = pyessv.load('ecmwf:{}'.format(project))
        else:
            authority = pyessv.load('wcrp')
            scope = pyessv.load('wcrp:{}'.format(project))
        if not scope:
            scope = _create_scope(authority, project)

        # Set scope data.
        scope.data = module.SCOPE_DATA or dict()
        #scope.data = scope.data or dict()
        #for field in module.SCOPE_DATA:
        #    scope.data[field] = ini_section.get_option(field, raw=True)

        # Create regex collections.
        collections = [i for i in module.COLLECTIONS if not inspect.isfunction(i[1])]
        for collection_id, term_regex in collections:
            _create_collection(module, scope, collection_id, term_regex=term_regex)

        # Create standard collections.
        collections = [i for i in module.COLLECTIONS if inspect.isfunction(i[1])]
        for collection_id, term_factory in collections:
            ctx = _MappingExecutionContext(project, collection_id, ini_section)
            collection = _create_collection(module, scope, collection_id)
            try:
                term_factory = term_factory()
            except TypeError:
                pass
            for term_data in term_factory(ctx):
                try:
                    term_src, term_dst = term_data
                    t = _get_term(collection, term_dst)
                    s = pyessv.load(term_src)
                    s.associations.append(t)
                except (ValueError, AttributeError):
                    _get_term(collection, term_data)

    # Add to archive & persist to file system.
    pyessv.archive(authority)


class _MappingExecutionContext(object):
    """Encpasulates information dispatched to mapping functions.

    """
    def __init__(self, project, collection_id, ini_section):
        """Instance constructor.

        """
        self.collection_id = collection_id
        self.project = project
        self.ini_section = ini_section


class _IniSection(object):
    """Wraps an ESG ini file section.

    """
    def __init__(self, project, source_dir):
        """Instance constructor.

        """
        fpath = os.path.join(source_dir, 'esg.{}.ini'.format(project))
        if not os.path.isfile(fpath):
            raise ValueError('ESGF ini file does not exist: {}'.format(fpath))
        self.parser = ConfigParser()
        self.parser.read(fpath)
        self.section = 'project:{}'.format(project)


    def get_option(self, option, seperator=None, splitter=None, raw=False):
        """Returns an ini file option.

        """
        data = self.parser.get(self.section, option, raw=raw)
        if seperator:
            data = data.split(seperator)
            if option.endswith('_map'):
                data = data[1:]
            if splitter:
                data = [[i.strip() for i in i.split(splitter)] for i in data]

        return data


def _create_scope(authority, project):
    """Factory method to return vocabulary scope.

    """
    return pyessv.create_scope(
        authority,
        project,
        description='ESGF publisher controlled Vocabularies (CVs) for use in {}'.format(project.upper()),
        label=project.upper(),
        url='https://esgf.llnl.gov'
    )


def _create_collection(module, scope, collection_id, term_regex=None):
    """Factory method to return vocabulary collection.

    """
    try:
        data = module.COLLECTION_DATA[collection_id]
    except (AttributeError, KeyError):
        data = None
    if collection_id.lower().replace('_', '-') in [collection.name for collection in scope.collections]:
        collection = scope[collection_id]
        collection.description = "ESGF publisher-config CV collection: ".format(collection_id),
        collection.label = collection_id.title().replace('_', ' ').replace('Rcm', 'RCM').replace('Cmor', 'CMOR')
        collection.term_regex = term_regex
        collection.data = data
        return collection
    else:
        return pyessv.create_collection(
            scope,
            collection_id,
            "ESGF publisher-config CV collection: ".format(collection_id),
            label=collection_id.title().replace('_', ' ').replace('Rcm', 'RCM').replace('Cmor', 'CMOR'),
            term_regex=term_regex,
            data=data
        )


def _get_term(collection, term_info):
    """Factory method to return vocabulary term.

    """
    # Unpack term information.
    name = label = description = synonym = None
    if isinstance(term_info, basestring):
        name = term_info
    else:
        try:
            name, label, description, synonym = term_info
        except ValueError:
            try:
                name, label, description = term_info
            except ValueError:
                try:
                    name, label = term_info
                except ValueError:
                    name = term_info

    alternative_names = [] if synonym is None else [synonym]

    return pyessv.create_term(collection, name,
        label=label,
        description=description,
        alternative_names=alternative_names
    )


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
