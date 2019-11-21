"""
.. module:: pyessv.model.__init__.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Model of vocabulary entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.model.authority import Authority
from pyessv.model.scope import Scope
from pyessv.model.collection import Collection
from pyessv.model.node import Node
from pyessv.model.node import IterableNode
from pyessv.model.term import Term

# Set of node types.
NODE_TYPES = {
    Authority,
    Collection,
    Scope,
    Term
}
