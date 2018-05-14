# -*- coding: utf-8 -*-

"""
.. module:: handlers.retrieve.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC pyessv - retrieve node endpoint.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from collections import OrderedDict

import tornado

import pyessv
from pyessv._ws.utils import constants
from pyessv._ws.utils.http import process_request




# Query parameters.
_PARAM_INCLUDE_META = 'includeMeta'


class RetrieveRequestHandler(tornado.web.RequestHandler):
    """Retrieve node request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def get(self):
        """HTTP GET handler.

        """
        def _set_output():
            """Sets response to be returned to client.

            """
            # Set include meta section flag.
            include_meta = self.get_argument(_PARAM_INCLUDE_META, 'false') == 'true'

            # Sets vocabulary identifier.
            identifier = ':'.join([i.strip().lower().replace('_', '-') for i in self.request.path.split('/')[3:]])

            # Set output to be returned to client.
            if len(identifier) == 0:
                self.output = {
                    'data': [_encode(i, include_meta) for i in pyessv.load()]
                }
            else:
                self.output = {
                    'data': _encode(pyessv.load(identifier), include_meta)
                }


        # Process request.
        process_request(self, [
            _set_output
            ])


def _encode(node, include_meta):
    """Encodes output according to node type.

    """
    obj = _encode_node(node, include_meta)
    if isinstance(node, pyessv.Authority):
        obj['scopes'] = [_encode(i, include_meta) for i in node.scopes]
    elif isinstance(node, pyessv.Scope):
        obj['collections'] = [_encode(i, include_meta) for i in node.collections]
    elif isinstance(node, pyessv.Collection):
        obj['terms'] = [_encode(i, include_meta) for i in node.terms]
        obj['term_regex'] = node.term_regex
    elif isinstance(node, pyessv.Term):
        obj['data'] = node.data
        obj['status'] = node.status

    return obj


def _encode_node(node, include_meta):
    """Returns encoded node base class.

    """
    obj = {
        'alternative_names': node.alternative_names,
        'canonical_name': node.canonical_name,
        'description': node.description,
        'label': node.label,
        'raw_name': node.raw_name,
        'url': node.url
    }
    if include_meta:
        obj['meta'] = {
            'create_date': node.create_date,
            'namespace': node.namespace,
            'typekey': node.typekey,
            'uid': node.uid
        }

    return obj
