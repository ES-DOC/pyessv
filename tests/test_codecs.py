# -*- coding: utf-8 -*-

"""
.. module:: testcodecs.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv encoding / decoding tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect

import pytest

from pyessv.codecs import decode
from pyessv.codecs import encode
from pyessv.constants import ENCODING_DICT
from pyessv.constants import ENCODING_JSON
from pyessv.constants import ENCODING_SET
from pyessv.constants import STANDARD_NODE_FIELDS
from pyessv.utils import compat
import tests.utils as tu


# Types of representation by encoding.
_ENCODING_REPRESENTATION_TYPE = {
    ENCODING_DICT: dict,
    ENCODING_JSON: compat.basestring,
}


# Module level fixture teardown.
teardown_module = tu.teardown


def yield_parameterizations():
    """Test parameterizations.

    """
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
        for encoding in ENCODING_SET:
            yield node_factory(), encoding


@pytest.mark.parametrize("node, encoding", yield_parameterizations())
def test_encode(node, encoding):
    """pyessv-tests: encode.

    """
    representation = encode(node, encoding)
    assert isinstance(representation, _ENCODING_REPRESENTATION_TYPE[encoding])
    decoded = decode(representation, encoding)
    assert isinstance(decoded, type(node))
    for field in STANDARD_NODE_FIELDS:
        assert getattr(decoded, field) == getattr(node, field)
