# -*- coding: utf-8 -*-

"""
.. module:: pyessv._constants.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package constants.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os
import re


# In memory cache type.
CACHE_STORE_MEMORY = 'memory'

# Set of allowed cache types.
CACHE_STORE_TYPES = (
    CACHE_STORE_MEMORY,
    )

# Directory containing vocabulary archive.
DIR_ARCHIVE = os.getenv('PYESSV_ARCHIVE_HOME', os.path.expanduser('~/.esdoc/pyessv-archive'))

# Dictionary encoding.
ENCODING_DICT = 'dict'

# JSON encoding.
ENCODING_JSON = 'json'

# Set of supported encodings.
ENCODING_SET = {
    ENCODING_DICT,
    ENCODING_JSON
}

# Node type key - an authority governing vocabularies.
NODE_TYPEKEY_AUTHORITY = 'authority'

# Node type key - a scope constraining collection of vocabularies.
NODE_TYPEKEY_SCOPE = 'scope'

# Node type key - a collection constraining collection of terms by composing keys from other collections.
NODE_TYPEKEY_COLLECTION = 'collection'

# Node type key - a term.
NODE_TYPEKEY_TERM = 'term'

# Set of allowed name types.
NODE_TYPEKEY_SET = (
  NODE_TYPEKEY_AUTHORITY,
  NODE_TYPEKEY_COLLECTION,
  NODE_TYPEKEY_SCOPE,
  NODE_TYPEKEY_TERM
  )

# Governance state - the term is accepted.
GOVERNANCE_STATUS_ACCEPTED = 'accepted'

# Governance state - the term is obsolete.
GOVERNANCE_STATUS_DEPRECATED = 'obsolete'

# Governance state - the term is pending review.
GOVERNANCE_STATUS_PENDING = 'pending'

# Governance state - the term is rejected.
GOVERNANCE_STATUS_REJECTED = 'rejected'

# Set of allowed governance states.
GOVERNANCE_STATUS_SET = (
    GOVERNANCE_STATUS_PENDING,
    GOVERNANCE_STATUS_ACCEPTED,
    GOVERNANCE_STATUS_REJECTED,
    GOVERNANCE_STATUS_DEPRECATED
    )

# Parsing strictness: canonical-name;
PARSING_STRICTNESS_0 = 0

# Parsing strictness: raw-name;
PARSING_STRICTNESS_1 = 1

# Parsing strictness: canonical-name + raw-name;
PARSING_STRICTNESS_2 = 2

# Parsing strictness: 2 + alternative_names
PARSING_STRICTNESS_3 = 3

# Parsing strictness: 3 + case-insensitive
PARSING_STRICTNESS_4 = 4

# Set of allowed parsing stricness.
PARSING_STRICTNESS_SET = (
    PARSING_STRICTNESS_0,
    PARSING_STRICTNESS_1,
    PARSING_STRICTNESS_2,
    PARSING_STRICTNESS_3,
    PARSING_STRICTNESS_4
    )

# Regular expression for validating a canonical name.
REGEX_CANONICAL_NAME = r'^[a-z0-9\-]*$'

# Standard node fields.
STANDARD_NODE_FIELDS = (
    'alternative_names',
    'canonical_name',
    'create_date',
    'description',
    'label',
    'raw_name',
    'typekey',
    'uid',
    'url',
    )

# Parsing node fields.
PARSING_NODE_FIELDS = (
    'canonical_name',
    'label',
    'raw_name'
    )
