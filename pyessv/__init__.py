# -*- coding: utf-8 -*-
"""
.. module:: pyessv.__init__.py

   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Python Earth Science Standard Vocabulary library intializer.

.. moduleauthor:: IPSL (ES-DOC) <dev@esdocumentation.org>

"""
__title__ = 'pyessv'
__version__ = '0.6.2.0'
__author__ = 'ES-DOC'
__license__ = 'GPL'
__copyright__ = 'Copyright 2017 ES-DOC'


from pyessv._archive import archive

from pyessv._cache import get_cached

from pyessv._codecs import decode
from pyessv._codecs import encode

from pyessv._constants import DIR_ARCHIVE
from pyessv._constants import ENCODING_DICT
from pyessv._constants import ENCODING_JSON
from pyessv._constants import NODE_TYPEKEY_AUTHORITY
from pyessv._constants import NODE_TYPEKEY_COLLECTION
from pyessv._constants import NODE_TYPEKEY_SCOPE
from pyessv._constants import NODE_TYPEKEY_TERM
from pyessv._constants import GOVERNANCE_STATUS_ACCEPTED
from pyessv._constants import GOVERNANCE_STATUS_DEPRECATED
from pyessv._constants import GOVERNANCE_STATUS_PENDING
from pyessv._constants import GOVERNANCE_STATUS_REJECTED
from pyessv._constants import PARSING_STRICTNESS_0
from pyessv._constants import PARSING_STRICTNESS_1
from pyessv._constants import PARSING_STRICTNESS_2
from pyessv._constants import PARSING_STRICTNESS_3
from pyessv._constants import PARSING_STRICTNESS_4
from pyessv._constants import REGEX_CANONICAL_NAME

from pyessv._exceptions import InvalidAssociationError
from pyessv._exceptions import TemplateParsingError
from pyessv._exceptions import ParsingError
from pyessv._exceptions import ValidationError

from pyessv._factory import create_authority
from pyessv._factory import create_collection
from pyessv._factory import create_template_parser
from pyessv._factory import create_scope
from pyessv._factory import create_term

from pyessv._factory_for_testing import get_test_datasets

from pyessv._governance import accept
from pyessv._governance import deprecate
from pyessv._governance import destroy
from pyessv._governance import reject
from pyessv._governance import reset

from pyessv._initializer import init

from pyessv._loader import load_random
from pyessv._loader import load

from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._model import Term

from pyessv._parser import parse
from pyessv._parsers import parse_dataset_identifer
from pyessv._parsers import parse_dataset_identifers

from pyessv._utils.logger import log
from pyessv._utils.logger import log_error
from pyessv._utils.logger import log_warning

from pyessv._validation import get_errors
from pyessv._validation import is_valid
from pyessv._validation import validate

from pyessv._ws import app as web_service


# Auto-initialize.
init()
