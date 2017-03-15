# -*- coding: utf-8 -*-

"""
.. module:: pyessv._constants.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package constants.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Directory containing vocabulary archive.
DIR_ARCHIVE = "~/.esdoc/pyessv"

# Dictionary encoding.
ENCODING_DICT = "dict"

# JSON encoding.
ENCODING_JSON = "json"

# Set of supported encodings.
ENCODING_SET = {
    ENCODING_DICT,
    ENCODING_JSON
}

# Governance state - the term is pending review.
GOVERNANCE_STATUS_PENDING = u'pending'

# Governance state - the term is accepted.
GOVERNANCE_STATUS_ACCEPTED = u'accepted'

# Governance state - the term is rejected.
GOVERNANCE_STATUS_REJECTED = u'rejected'

# Governance state - the term is obsolete.
GOVERNANCE_STATUS_DEPRECATED = u'obsolete'

# Set of allowed governance states.
GOVERNANCE_STATUS_SET = set([
    GOVERNANCE_STATUS_PENDING,
    GOVERNANCE_STATUS_ACCEPTED,
    GOVERNANCE_STATUS_REJECTED,
    GOVERNANCE_STATUS_DEPRECATED
])

# Regular expression for validating a canonical name.
REGEX_CANONICAL_NAME = u"/&"

# Regular expression for validating a label.
REGEX_LABEL = u"/&"

# Regular expression for validating a url.
REGEX_URL = u""

# Name type - an authority governing vocabularies.
NAME_TYPE_AUTHORITY = "authority"

# Name type - a scope constraining collection of vocabularies.
NAME_TYPE_SCOPE = "scope"

# Name type - a collection constraining collection of term.
NAME_TYPE_COLLECTION = "collection"

# Name type - a term.
NAME_TYPE_TERM = "term"

# Set of allowed name types.
NAME_TYPE_SET = set([
  NAME_TYPE_AUTHORITY,
  NAME_TYPE_COLLECTION,
  NAME_TYPE_SCOPE,
  NAME_TYPE_TERM
  ])
