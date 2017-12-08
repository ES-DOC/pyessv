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
from pyessv._model.term import Term
from pyessv._utils.compat import  basestring



class TemplateParser(object):
    """A vocabulary template parser.

    """
    def __init__(self, template, collections, strictness, seperator='.'):
        """Instance constructor.

        :param str template: Identifier template.
        :param list collections: pyessv collection identifiers.
        :param int strictness: Strictness level to apply when applying name matching rules.
        :param str seprarator: Seperator to apply when parsing.

        """
        from pyessv._loader import load

        self.seperator = seperator
        self.template_parts = template.split(seperator)
        self.template = template
        self.strictness = strictness

        # Inject pyessv collections into template.
        collection_idx = 0
        for idx, part in enumerate(self.template_parts):
            if part == '{}':
                self.template_parts[idx] = load(collections[collection_idx])
                collection_idx += 1


    def parse(self, val):
        """Parses a val against a template.

        :returns: Set of terms extracted during parsing process.

        """
        # Verify that number of parts is equal.
        parts = val.split(self.seperator)
        if len(parts) != len(self.template_parts):
            raise TemplateParsingError('Number of elements is invalid: {}: is {}, expected {}'.format(val, len(parts), len(self.template_parts)))

        # Iterate template.
        terms = set()
        for template_part, name in [(self.template_parts[i], j) for i, j in enumerate(parts)]:
            # Verify constant match.
            if isinstance(template_part, basestring):
                if template_part != name:
                    raise TemplateParsingError('{} :: {}'.format(name, val))
                continue

            # Verify collection match.
            collection = template_part
            term = collection.is_matched(name, self.strictness)
            if term == False:
                raise TemplateParsingError('vocab={} :: strictness={} :: value={}'.format(collection, self.strictness, val))
            if isinstance(term, Term):
                terms.add(term)

        return terms
