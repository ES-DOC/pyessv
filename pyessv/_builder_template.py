# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model._builder_template.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary constrained template builder, e.g. a dataset identifier.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._model import Collection, Term
from pyessv._exceptions import TemplateParsingError, TemplateValueError
from pyessv._constants import BUILDER_FIELDS

class TemplateBuilder(object):
    """A vocabulary template builder.

    """
    def __init__(self, template, collections, strictness, separator='.'):
        """Instance constructor.

        :param str template: Identifier template.
        :param tuple collections: pyessv collection identifiers.
        :param int strictness: Strictness level to apply when applying name matching rules.
        :param str seprarator: Separator to apply when parsing.

        """
        from pyessv._loader import load

        self.separator = separator
        self.template_parts = template.split(separator)
        self.template = template
        self.strictness = strictness

        # Inject pyessv collections into template.
        collection_idx = 0
        for idx, part in enumerate(self.template_parts):
            if part == '{}':
                self.template_parts[idx] = load(collections[collection_idx])
                collection_idx += 1


    def build(self, terms, att='label', alt_name=0):
        """Build template instance from a list of pyessv terms.

        :returns: Template instance string.

        """
        assert isinstance(alt_name, int), 'Invalid alternative name index'
        assert att in BUILDER_FIELDS, 'Invalid name'

        # Instantiate string parts.
        string_parts = list()

        # Iterate template.
        for template_part in self.template_parts:

            # Append constant match.
            if isinstance(template_part, basestring):
                string_parts.append(template_part)
                continue

            # Append term match.
            collection = template_part
            term = None
            for term in terms:
                if term.collection == collection:
                    break

            # Verify collection is found among terms.
            if not term:
                raise TemplateValueError('Collection not found among terms :: {}'.format(collection))

            # Get term field.
            if att == 'alternative_names':
                string_parts.append(getattr(term, att)[alt_name])
            else:
                string_parts.append(getattr(term, att))


        return self.separator.join(string_parts)