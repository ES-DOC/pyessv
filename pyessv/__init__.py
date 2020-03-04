"""
.. module:: pyessv.__init__.py

   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Python Earth Science Standard Vocabulary library intializer.

.. moduleauthor:: IPSL (ES-DOC) <dev@esdocumentation.org>

"""
__title__ = 'pyessv'
__version__ = '0.8.4.0'
__author__ = 'ES-DOC'
__license__ = 'COSL'
__copyright__ = 'Copyright 2020 Casper Labs LLC'


from pyessv.archive import archive

from pyessv.cache import get_cached

from pyessv.codecs import decode
from pyessv.codecs import encode

from pyessv.constants import DIR_ARCHIVE
from pyessv.constants import ENCODING_DICT
from pyessv.constants import ENCODING_JSON
from pyessv.constants import NODE_TYPEKEY_AUTHORITY
from pyessv.constants import NODE_TYPEKEY_COLLECTION
from pyessv.constants import NODE_TYPEKEY_SCOPE
from pyessv.constants import NODE_TYPEKEY_TERM
from pyessv.constants import GOVERNANCE_STATUS_ACCEPTED
from pyessv.constants import GOVERNANCE_STATUS_DEPRECATED
from pyessv.constants import GOVERNANCE_STATUS_PENDING
from pyessv.constants import GOVERNANCE_STATUS_REJECTED
from pyessv.constants import PARSING_STRICTNESS_0
from pyessv.constants import PARSING_STRICTNESS_1
from pyessv.constants import PARSING_STRICTNESS_2
from pyessv.constants import PARSING_STRICTNESS_3
from pyessv.constants import PARSING_STRICTNESS_4
from pyessv.constants import REGEX_CANONICAL_NAME

from pyessv.exceptions import InvalidAssociationError
from pyessv.exceptions import TemplateParsingError
from pyessv.exceptions import ParsingError
from pyessv.exceptions import ValidationError

from pyessv.factory import create_authority
from pyessv.factory import create_collection
from pyessv.factory import create_template_parser
from pyessv.factory import create_scope
from pyessv.factory import create_term

from pyessv.factory_for_testing import get_datasets_for_testing

from pyessv.governance import accept
from pyessv.governance import deprecate
from pyessv.governance import reject
from pyessv.governance import reset

from pyessv.initializer import init

from pyessv.loader import load_random
from pyessv.loader import load

from pyessv.model import Authority
from pyessv.model import Collection
from pyessv.model import Scope
from pyessv.model import Term

from pyessv.parser import parse
from pyessv.parsers import parse_dataset_identifer
from pyessv.parsers import parse_dataset_identifers

from pyessv.utils.logger import log
from pyessv.utils.logger import log_error
from pyessv.utils.logger import log_warning

from pyessv.validation import get_errors
from pyessv.validation import is_valid
from pyessv.validation import validate


# Auto-initialize.
init()
