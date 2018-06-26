# -*- coding: utf-8 -*-

"""
.. module:: test_interface.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv interface tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pyessv as LIB
import tests.utils as tu



# Set of classes exposed by library.
_CLASSES = {
    'Authority',
    'Collection',
    'Scope',
    'Term'
    }

# Set of constants exposed by library.
_CONSTANTS = {
    'DIR_ARCHIVE',
    'ENCODING_DICT',
    'ENCODING_JSON',
    'NODE_TYPEKEY_AUTHORITY',
    'NODE_TYPEKEY_COLLECTION',
    'NODE_TYPEKEY_SCOPE',
    'NODE_TYPEKEY_TERM',
    'GOVERNANCE_STATUS_ACCEPTED',
    'GOVERNANCE_STATUS_DEPRECATED',
    'GOVERNANCE_STATUS_PENDING',
    'GOVERNANCE_STATUS_REJECTED',
    'PARSING_STRICTNESS_0',
    'PARSING_STRICTNESS_1',
    'PARSING_STRICTNESS_2',
    'PARSING_STRICTNESS_3',
    'PARSING_STRICTNESS_4',
    'REGEX_CANONICAL_NAME'
    }

# Set of exceptions exposed by library.
_EXCEPTIONS = {
    'InvalidAssociationError',
    'ParsingError',
    'TemplateParsingError',
    'ValidationError'
    }

# Set of functions exposed by library.
_FUNCS = {
    # ... archive
    'archive',
    # ... codecs
    'decode',
    'encode',
    # ... factory
    'create_authority',
    'create_collection',
    'create_template_parser',
    'create_scope',
    'create_term',
    # ... factory for testing
    'get_test_datasets',
    # ... governance
    'accept',
    'deprecate',
    'destroy',
    'reject',
    'reset',
    # ... initialisation
    'init',
    # ... loader
    'load_random',
    'load',
    # ... logging
    'log',
    'log_error',
    'log_warning',
    # ... parsing
    'parse',
    'parse_dataset_identifer',
    'parse_dataset_identifers',
    # ... validation
    'get_errors',
    'is_valid',
    'validate'
}


def test_library_exports():
    """Test set of exports exposed by library.

    """
    def _test_member(member, member_type):
        """Test that library exposes the named member.

        """
        assertor = getattr(tu, 'assert_has_{}'.format(member_type))
        assertor(LIB, member)


    for members, member_type, in (
        (_CLASSES, 'class'),
        (_CONSTANTS, 'constant'),
        (_EXCEPTIONS, 'exception'),
        (_FUNCS, 'function'),
        ):
        for member in sorted(members):
            desc = 'library exposes {} --> {}'.format(member_type, member)
            tu.init(_test_member, desc)
            yield _test_member, member, member_type
