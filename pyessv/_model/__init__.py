# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.__init__.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Model of vocabulary entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._constants import ENTITY_TYPE_AUTHORITY
from pyessv._constants import ENTITY_TYPE_COLLECTION
from pyessv._constants import ENTITY_TYPE_SCOPE
from pyessv._constants import ENTITY_TYPE_TERM
from pyessv._model.authority import Authority
from pyessv._model.collection import Collection
from pyessv._model.entity import Entity
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
