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
_PARAM_IDENTIFIER = 'identifier'
_PARAM_IDENTIFIER_TYPE = 'identifierType'
_PARAM_PROJECT = 'project'

# Map of identifier type to parser.
_PARSERS = {
    'dataset': pyessv.parse_dataset_identifer,
}


class ValidateIdentifierHandler(tornado.web.RequestHandler):
    """Dataset identifier validation endpoint request handler.

    """
    def get(self):
        """HTTP GET handler.

        """
        def _parse_identifier():
            """Parses an identifier.

            """
            parser = _PARSERS[self.get_argument(_PARAM_IDENTIFIER_TYPE)]
            parser(self.get_argument(_PARAM_PROJECT), self.get_argument(_PARAM_IDENTIFIER))


        def _set_output():
            """Sets response to be returned to client.

            """
            self.output = {
                "message": "{} is a valid {} identifier".format(
                    self.get_argument(_PARAM_IDENTIFIER),
                    self.get_argument(_PARAM_IDENTIFIER_TYPE)
                ),
            }

        # Process request.
        process_request(self, [
            _parse_identifier,
            _set_output
            ])
