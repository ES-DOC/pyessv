# -*- coding: utf-8 -*-

"""
.. module:: map.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Maps raw ESGF CMIP6 ini config file to normalized pyessv format.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os
from ConfigParser import ConfigParser

import arrow
import pyessv

import map_cmip5
import map_cmip6
import map_cordex
import utils



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
    authority = create_authority()

    # Process project modules:
    for module in _MODULES:
        # Set project.
        project = module.__name__[4:]

        # Set ini file handler.
        ini_section = _IniSection(project, args.source)

        # Create scope.
        scope = create_scope(authority, project)
        try:
            module.set_scope_data(scope, ini_section)
        except AttributeError:
            pass

        # Process vocab collections.
        for collection_id, term_factory in module.VOCAB_COLLECTIONS:
            ctx = _MappingExecutionContext(project, collection_id, ini_section)
            collection = create_collection(scope, collection_id)
            try:
                term_factory = term_factory()
            except TypeError:
                pass
            for term_data in term_factory(ctx):
                create_term(collection, term_data)

        # Process regex collections.
        for collection_id, term_regex in module.REG_EX_COLLECTIONS:
            # print collection_id, term_regex
            create_collection(scope, collection_id, term_regex=term_regex)

        # Process data.
        scope.data = scope.data or dict()
        for field in module.DATA:
            scope.data[field] = ini_section.get_option(field, raw=True)


    # Add to the archive.
    pyessv.add(authority)

    # Save (to file system).
    pyessv.save()


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


def create_authority():
    return pyessv.create_authority(
        'esgf-publisher',
        description='Earth System Grid Federation',
        label='ESGF',
        url='https://esgf.llnl.gov',
        create_date=arrow.get('2017-10-11 00:00:00.000000+0000').datetime
    )


def create_scope(authority, project):
    return pyessv.create_scope(
        authority,
        project,
        description='ESGF publisher controlled Vocabularies (CVs) for use in {}'.format(project.upper()),
        label=project.upper(),
        url='https://esgf.llnl.gov'
    )


def create_collection(scope, collection_id, term_regex=None):
    return pyessv.create_collection(
        scope,
        collection_id,
        "ESGF publisher-config CV collection: ".format(collection_id),
        term_regex=term_regex
    )


def create_term(collection, term_info):
    term_name, term_label, term_description = term_info
    return pyessv.create_term(collection, term_name,
        label=term_label,
        description=term_description
    )


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
