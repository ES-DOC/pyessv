# -*- coding: utf-8 -*-

"""
.. module:: handlers.validate_identifier.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC pyessv - identifier validation endpoint.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime as dt

import tornado

import pyessv
from pyessv._ws.utils.http import process_request



# Query parameter names.
_PARAM_IDENTIFIER_TYPE = 'identifierType'
_PARAM_PROJECT = 'project'

# Payload body field names.
_FIELD_IDENTIFIER_SET = 'identifierSet'

# Map of identifier type to parser.
_PARSERS = {
    'dataset': pyessv.parse_dataset_identifers,
}


class ValidateIdentifierSetHandler(tornado.web.RequestHandler):
    """Dataset identifier set validation endpoint request handler.

    """
    def post(self):
        """HTTP POST handler.

        """
        def _parse_identifier():
            """Parses an identifier.

            """
            # Decode.
            identifier_type = self.get_argument(_PARAM_IDENTIFIER_TYPE)
            identifiers = self.request.data[_FIELD_IDENTIFIER_SET]
            project = self.get_argument(_PARAM_PROJECT)

            # Parse.
            parser = _PARSERS[identifier_type]
            parser(project, identifiers)


        def _set_output():
            """Sets response to be returned to client.

            """
            self.output = {
                "message": "Datasets are valid {} identifiers".format(
                    self.get_argument(_PARAM_IDENTIFIER_TYPE)
                ),
            }

        # Process request.
        process_request(self, [
            _parse_identifier,
            _set_output
            ])
