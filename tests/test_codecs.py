# -*- coding: utf-8 -*-

"""
.. module:: test_codecs.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv encoding / decoding tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import nose

import pyessv as LIB
from pyessv._codecs import decode
from pyessv._codecs import encode
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
import tests.utils as tu



# Types of representation by encoding.
_ENCODING_REPRESENTATION_TYPE = {
    LIB.ENCODING_DICT: dict,
    LIB.ENCODING_JSON: basestring,
}


def test_interface():
    """pyessv-tests: codecs: interface.

    """
    assert inspect.isfunction(decode)
    assert inspect.isfunction(encode)


@nose.with_setup(None, tu.teardown)
def test_encode():
    """pyessv-tests: encode.

    """
    def _test(func, typeof, encoding):
        """Inner test.

        """
        instance = func()
        assert isinstance(instance, typeof)

        representation = encode(instance, encoding)
        assert isinstance(representation, _ENCODING_REPRESENTATION_TYPE[encoding])

        if encoding == LIB.ENCODING_DICT:
            for k, v in representation.iteritems():
                if not k.startswith('_'):
                    assert getattr(instance, k) == v, 'encode fail: {} :: {} :: {}'.format(k, getattr(instance, k), v)


    for func, typeof in (
        (tu.create_authority, LIB.Authority),
        (tu.create_scope, LIB.Scope),
        (tu.create_collection, LIB.Collection),
        (tu.create_term, LIB.Term)
        ):
        desc = 'encode --> {} --> dict'.format(str(typeof).split('.')[-1][0:-2].lower())
        tu.init(_test, desc)
        yield _test, func, typeof, LIB.ENCODING_DICT

        desc = 'encode --> {} --> json'.format(str(typeof).split('.')[-1][0:-2].lower())
        tu.init(_test, desc)
        yield _test, func, typeof, LIB.ENCODING_JSON



@nose.with_setup(None, tu.teardown)
def test_decode():
    """pyessv-tests: decode.

    """
    def _test(func, typeof, encoding):
        """Inner test.

        """
        instance = func()
        representation = encode(instance, encoding)
        decoded = decode(representation, encoding)
        assert isinstance(decoded, typeof)


    for func, typeof in (
        (tu.create_authority, LIB.Authority),
        (tu.create_scope, LIB.Scope),
        (tu.create_collection, LIB.Collection),
        (tu.create_term, LIB.Term)
        ):
        desc = 'decode --> {} --> dict'.format(str(typeof).split('.')[-1][0:-2].lower())
        tu.init(_test, desc)
        yield _test, func, typeof, LIB.ENCODING_DICT

        desc = 'decode --> {} --> json'.format(str(typeof).split('.')[-1][0:-2].lower())
        tu.init(_test, desc)
        yield _test, func, typeof, LIB.ENCODING_JSON
