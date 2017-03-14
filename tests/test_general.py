# -*- coding: utf-8 -*-

"""
.. module:: test_general.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyesdoc.cv general tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import uuid

import nose.tools

import pyesdoc.cv as LIB
import tests.cv.utils as tu



# Set of classes exposed by library.
_CLASSES = {
    'Term'
}

# Set of constants exposed by library.
_CONSTANTS = {
    'GOVERNANCE_STATUS_ACCEPTED',
    'GOVERNANCE_STATUS_DEPRECATED',
    'GOVERNANCE_STATUS_PENDING',
    'GOVERNANCE_STATUS_REJECTED',
    'OPT_IO_DIR',
    'OPT_IS_VERBOSE'
}

# Set of exceptions exposed by library.
_EXCEPTIONS = {
    'InvalidAssociationError',
    'InvalidOptionError',
    'ValidationError'
}

# Set of functions exposed by library.
_FUNCS = {
    'accept',
    'create',
    'delete',
    'deprecate',
    'get_count',
    'get_option',
    'get_term',
    'get_termset',
    'get_termsets',
    'init',
    'is_valid',
    'reject',
    'reset',
    'save',
    'validate'
}


def test_library_exports():
    """Test set of exports exposed by library.

    """
    def _test_member(member, member_type):
        """Test that library exposes the named member."""
        assertor = getattr(tu, 'assert_has_{}'.format(member_type))
        assertor(LIB, member)

    for members, member_type, in (
        (_CLASSES, 'class'),
        (_CONSTANTS, 'constant'),
        (_EXCEPTIONS, 'exception'),
        (_FUNCS, 'function'),
        ):
        for member in members:
            desc = "exposes a {} called {}".format(member_type, member)
            tu.init(_test_member, 'library', desc)
            yield _test_member, member, member_type


def test_library_initialization():
    """Test library initialization.

    """
    def _test_init_01():
        """Normal initialization."""
        with tu.get_options() as opts:
            LIB.init(opts)

    @nose.tools.raises(IOError)
    def _test_init_02():
        """Initialization error caused by invalid io directory."""
        LIB.init({
            'io_dir': uuid.uuid4()
        })

    @nose.tools.raises(ValueError)
    def _test_init_03():
        """Initialization error caused by invalid verbose flag."""
        LIB.init({
            'verbose': float()
        })

    for func in (_test_init_01, _test_init_02, _test_init_03):
        tu.init(func, 'library')
        yield func
