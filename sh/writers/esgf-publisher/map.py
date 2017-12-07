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

import map_cmip5
import map_cmip6
import map_cordex



# Define command line options.
_ARGS = argparse.ArgumentParser('Maps ESGF publisher ini files to normalized pyessv vocabulary format.')
_ARGS.add_argument(
    '--source',
    help='Directory within which ESGF publisher ini files will be read.',
    dest='source',
    type=str
    )

# Relative path to ini file.
_INI_FPATH = 'publisher-configs/ini/esg.{}.ini'

# Set of mapping modules.
_MODULES = {
    map_cmip5,
    map_cmip6,
    map_cordex
    }


def _main(args):
    """Main entry point.

    """
    # Create authority.
    authority = pyessv.load('wcrp')

    # Process project modules:
    for module in _MODULES:
        # Set project.
        project = module.__name__[4:]

        # Set ini file handler.
        ini_section = _IniSection(project, args.source)

        # Create scope.
        scope = _get_scope(authority, project)
        scope.data = scope.data or dict()
        for field in module.SCOPE_DATA:
            scope.data[field] = ini_section.get_option(field, raw=True)

        # Create regex collections.
        collections = [i for i in module.COLLECTIONS if not inspect.isfunction(i[1])]
        for collection_id, term_regex in collections:
            _get_collection(module, scope, collection_id, term_regex=term_regex)

        # Create standard collections.
        collections = [i for i in module.COLLECTIONS if inspect.isfunction(i[1])]
        for collection_id, term_factory in collections:
            ctx = _MappingExecutionContext(project, collection_id, ini_section)
            collection = _get_collection(module, scope, collection_id)
            try:
                term_factory = term_factory()
            except TypeError:
                pass
            for term_data in term_factory(ctx):
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
        fpath = os.path.join(source_dir, _INI_FPATH.format(project))
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


def _get_scope(authority, project):
    """Factory method to return vocabulary scope.

    """
    return pyessv.load('wcrp:{}'.format(project)) or pyessv.create_scope(
        authority,
        project,
        description='ESGF publisher controlled Vocabularies (CVs) for use in {}'.format(project.upper()),
        label=project.upper(),
        url='https://esgf.llnl.gov'
    )


def _get_collection(module, scope, collection_id, term_regex=None):
    """Factory method to return vocabulary collection.

    """
    try:
        data = module.COLLECTION_DATA[collection_id]
    except (AttributeError, KeyError):
        data = None

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
    name = label = description = None
    if isinstance(term_info, basestring):
        name = term_info
    else:
        try:
            name, label, description = term_info
        except ValueError:
            try:
                name, label = term_info
            except ValueError:
                name = term_info

    return pyessv.create_term(collection, name,
        label=label,
        description=description
    )


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
