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
from pyessv._constants import ENCODING_SET
from pyessv._constants import STANDARD_NODE_FIELDS
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
    def _test(node, encoding):
        """Inner test.

        """
        representation = encode(node, encoding)
        assert isinstance(representation, _ENCODING_REPRESENTATION_TYPE[encoding])
        decoded = decode(representation, encoding)
        assert isinstance(decoded, type(node))
        for field in STANDARD_NODE_FIELDS:
            assert getattr(decoded, field) == getattr(node, field)


    for node_factory in (
        tu.create_authority,
        tu.create_scope,
        tu.create_collection_01,
        tu.create_collection_02,
        tu.create_collection_03,
        tu.create_term_01,
        tu.create_term_02,
        tu.create_term_03
        ):
        node = node_factory()
        for encoding in ENCODING_SET:
            desc = 'codecs: {} --> {}'.format(node_factory.__name__[7:], encoding)
            tu.init(_test, desc)
            yield _test, node, encoding
