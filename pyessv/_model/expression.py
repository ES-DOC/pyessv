# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.expression.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary constrained expression, e.g. a dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
from pyessv._model.collection import Collection



class Expression(object):
    """A vocabulary expression.

    """
    def __init__(self, template, collections):
        """Instance constructor.

        """
        if [i for i in collections if not isinstance(i, Collection)]:
            raise ValueError("Invalid collections")
        if template.count("{}") != len(collections):
            raise ValueError("Invalid expression: template & number of collections are mismatched")

        self.template = template
        self.parts = template.split("{}")
        self.collections = collections



    def parse(self, val):
        parsed = ''
        for idx, collection in enumerate(self.collections):
            parsed += self.parts[idx]
            found = False
            for term in collection:
                found = val.startswith(parsed + term.name)
                if found:
                    break
            if found == False:
                raise ValueError("Invalid expression")
            parsed += term.name

        parsed += self.parts[idx + 1]
        if not val == parsed:
            raise ValueError("Invalid expression")
