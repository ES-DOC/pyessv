# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.__init__.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Model of vocabulary entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime
import uuid

from pyessv._constants import ENTITY_TYPE_AUTHORITY
from pyessv._constants import ENTITY_TYPE_COLLECTION
from pyessv._constants import ENTITY_TYPE_SCOPE
from pyessv._constants import ENTITY_TYPE_TERM
from pyessv._constants import GOVERNANCE_STATUS_SET
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._constants import REGEX_LABEL
from pyessv._constants import REGEX_URL
from pyessv._model.entity import Entity
from pyessv._model.authority import Authority
from pyessv._model.collection import Collection
from pyessv._model.scope import Scope
from pyessv._model.term import Term



# Set of supported entity types.
ENTITY_TYPES = (
    Authority,
    Collection,
    Scope,
    Term,
)

# Map of type keys to types.
ENTITY_TYPE_KEY_MAP = {
    Authority: ENTITY_TYPE_AUTHORITY,
    Collection: ENTITY_TYPE_COLLECTION,
    Scope: ENTITY_TYPE_SCOPE,
    Term: ENTITY_TYPE_TERM
}

# Type information applying to all entities.
_STANDARD_TYPE_INFO = {
    ("create_date", datetime.datetime, "1.1"),
    ("description", unicode, "1.1"),
    ("label", unicode, "1.1"),
    ("name", unicode, "1.1", REGEX_CANONICAL_NAME),
    ("typeof", str, "1.1"),
    ("uid", uuid.UUID, "1.1"),
    ("url", unicode, "0.1", REGEX_URL)
}

# Map of types to tuples containing validation info.
ENTITY_TYPE_INFO = {
    Authority: _STANDARD_TYPE_INFO.union({
        ("scopes", Scope, "0.N"),
    }),
    Collection: _STANDARD_TYPE_INFO.union({
        ("scope", Scope, "1.1"),
        ("terms", Term, "0.N"),
    }),
    Scope: _STANDARD_TYPE_INFO.union({
        ("authority", Authority, "1.1"),
        ("collections", Collection, "0.N"),
    }),
    Term: _STANDARD_TYPE_INFO.union({
        ("alternative_name", unicode, "0.1", REGEX_CANONICAL_NAME),
        ("alternative_url", unicode, "0.1", REGEX_URL),
        ("collection", Collection, "1.1"),
        ("idx", int, "1.1"),
        ("parent", Term, "0.1"),
        ("status", unicode, "1.1", tuple(GOVERNANCE_STATUS_SET)),
        ("synonyms", unicode, "0.N", REGEX_CANONICAL_NAME),
    })
}
