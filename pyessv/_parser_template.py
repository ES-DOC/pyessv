# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.expression_parser.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary constrained expression, e.g. a dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
from pyessv._model.collection import Collection
from pyessv._exceptions import TemplateParsingError



class TemplateParser(object):
    """A vocabulary template parser.

    """
    def __init__(self, template, collections, field):
        """Instance constructor.

        """
        self.template = template
        self.term_field = field
        self.parts = template.split('{}')
        self.collections = tuple(self._get_collection_info(i) for i in collections)


    def parse(self, val):
        """Parses a val against a template.

        """
        parsed = ''
        for idx, collection_info in enumerate(self.collections):
            collection, field = collection_info
            parsed += self.parts[idx]
            found = False
            for term in collection:
                found = val.startswith(parsed + getattr(term, field))
                if found:
                    break
            if found == False:
                raise TemplateParsingError(val)
            parsed += getattr(term, field)

        parsed += self.parts[idx + 1]
        if not val == parsed:
            raise TemplateParsingError(val)


    def _get_collection_info(self, identifier):
        """Sets a collection to be used in parsing.

        """
        if isinstance(identifier, Collection):
            return identifier

        assert isinstance(identifier, basestring), 'Invalid collection identifier'
        identifier = identifier.split(':')
        assert len(identifier) in (3, 4), 'Invalid collection identifier'

        field = self.term_field if len(identifier) == 3 else identifier[-1]
        assert field in ('canonical_name', 'raw_name', 'label'), 'Invalid parsing field'

        collection = pyessv.load(identifier[0], identifier[1], identifier[2])
        assert isinstance(collection, Collection), 'Invalid collection identifier'

        return collection, field
