import pytest

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
    'INITIALISATION_MODE',
    'IDENTIFIER_TYPE_DATASET',
    'IDENTIFIER_TYPE_DIRECTORY',
    'IDENTIFIER_TYPE_FILENAME',
    'IDENTIFIER_TYPE_SET',
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
    'NamespaceParsingError',
    'ValidationError'
    }

# Set of functions exposed by library.
_FUNCS = {
    # ... archive
    'archive',
    # ... cache
    'get_cached',
    # ... codecs
    'decode',
    'encode',
    # ... factory
    'create_authority',
    'create_collection',
    'create_scope',
    'create_term',
    # ... factory for testing
    'get_datasets_for_testing',
    # ... governance
    'accept',
    'deprecate',
    'reject',
    'reset',
    # ... initialisation
    'init',
    # ... loader
    'load_random',
    'load',
    # ... matcher
    'match_term',
    # ... logging
    'log',
    'log_error',
    'log_warning',
    # ... parsing
    'parse',
    'parse_namespace',
    'parse_identifer',
    'parse_identifer_set',
    # ... validation
    'get_errors',
    'is_valid',
    'validate'
}


def yield_parameterizations():
    """Yields test parameterizations.

    """
    for members, member_type in (
        (_CLASSES, 'class'),
        (_CONSTANTS, 'constant'),
        (_EXCEPTIONS, 'exception'),
        (_FUNCS, 'function'),
            ):
        for member in sorted(members):
            yield member_type, member


@pytest.mark.parametrize("member_type, member", yield_parameterizations())
def test_library_exports(member_type, member):
    """Test set of exports exposed by library.

    """
    assertor = getattr(tu, 'assert_has_{}'.format(member_type))
    assertor(LIB, member)
