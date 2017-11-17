# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model._parser_template.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary constrained template parser, e.g. a dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._exceptions import TemplateParsingError
from pyessv._model.collection import Collection
from pyessv._utils.compat import  basestring



class TemplateParser(object):
    """A vocabulary template parser.

    """
    def __init__(self, template, collections, field, seperator='.'):
        """Instance constructor.

        :param str template: Identifier template.
        :param list collections: pyessv collection identifiers.
        :param str field: Default parsing field.
        :param str seprarator: Seperator to apply when parsing.

        """
        self._seperator = seperator
        self._template_parts = template.split(seperator)
        self.template = template
        self.term_field = field

        collection_idx = 0
        for idx, part in enumerate(self._template_parts):
            if part == '{}':
                self._template_parts[idx] = Collection.get_info(collections[collection_idx])
                collection_idx += 1


    def parse(self, val):
        """Parses a val against a template.

        """
        # Error: number of parts is unequal.
        parts = val.split(self._seperator)
        if len(parts) != len(self._template_parts):
            raise TemplateParsingError(val)

        # Iterate template.
        for template_part, part in [(self._template_parts[i], j) for i, j in enumerate(parts)]:
            # Error: constant mismatch.
            if isinstance(template_part, basestring):
                if part != template_part:
                    raise TemplateParsingError(val)

            # Error: collection mismatch.
            else:
                collection, field = template_part
                if collection.is_matched(part, field) == False:
                    raise TemplateParsingError('{} :: {} :: {}'.format(collection, field, val))
