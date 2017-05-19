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



# Directory containing vocabulary archive.
DIR_ARCHIVE = os.path.expanduser('~/.esdoc/pyessv-archive')

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

# Node type key - a collection constraining collection of term.
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

# Regular expression for validating a canonical name.
REGEX_CANONICAL_NAME = r'^[A-z0-9\_\-\ \.]*$'
