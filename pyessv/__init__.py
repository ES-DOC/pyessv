# -*- coding: utf-8 -*-
"""
.. module:: pyessv.__init__.py

   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Python Earth Science Standard Vocabulary package intializer.

.. moduleauthor:: IPSL (ES-DOC) <dev@esdocumentation.org>

"""
from pyessv._archive import load

from pyessv._codecs import decode
from pyessv._codecs import encode

from pyessv._constants import *

from pyessv._exceptions import *

from pyessv._factory import create_authority
from pyessv._factory import create_collection
from pyessv._factory import create_scope
from pyessv._factory import create_term

from pyessv._io import read_authority
from pyessv._io import write_authority

from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._model import Term

from pyessv._parser import parse
from pyessv._parser import parse_namespace

from pyessv._validation import get_errors
from pyessv._validation import is_valid
from pyessv._validation import validate_entity as validate

