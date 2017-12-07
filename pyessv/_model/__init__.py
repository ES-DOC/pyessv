# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.__init__.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Model of vocabulary entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._model.authority import Authority
from pyessv._model.scope import Scope
from pyessv._model.collection import Collection
from pyessv._model.node import Node
from pyessv._model.node import IterableNode
from pyessv._model.term import Term

# Set of node types.
NODE_TYPES = {
    Authority,
    Collection,
    Scope,
    Term
}
