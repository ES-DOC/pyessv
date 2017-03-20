# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.authority.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary authority, e.g. WGCM.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
from pyessv._model.entity import Entity



class Authority(Entity):
    """An authority assuming responsibity for governance of vocabularies.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Authority, self).__init__(pyessv.ENTITY_TYPE_AUTHORITY)

        self.scopes = list()


    def __len__(self):
        """Returns number of items in managed collection.

        """
        return Entity.get_count(self)


    def __iter__(self):
        """Instance iterator initializer.

        """
        return Entity.get_iter(self)


    def __getitem__(self, key):
        """Returns a child section item.

        """
        return Entity.get_item(self, key)


    def __contains__(self, key):
        """Instance membership predicate.

        """
        return self[key] is not None


    def parse(self, scope_name, strict=True):
        """Parses an associated scope name.

        """
        return pyessv.parse(scope_name, self, strict=strict)
