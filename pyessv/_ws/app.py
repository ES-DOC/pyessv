# -*- coding: utf-8 -*-
"""

.. module:: app.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC Errata - web-service entry point.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

import tornado.web

import pyessv
from pyessv._ws import handlers
from pyessv._ws import schemas
from pyessv._ws.utils import config
from pyessv._ws.utils.logger import log_web as log



def _get_path_to_front_end():
    """Return path to the front end javascript application.

    """
    dpath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'fe')
    log("Front-end static files @ {0}".format(dpath))

    return dpath


def _get_app_endpoints():
    """Returns map of application endpoints to handlers.

    """
    endpoints = [r'/1/retrieve']
    for authority in pyessv.get_cached():
        endpoints.append(r'/1/retrieve/{}'.format(authority.canonical_name))
        for scope in authority:
            endpoints.append(r'/1/retrieve/{}/{}'.format(
                authority.canonical_name,
                scope.canonical_name)
                )
            for collection in scope:
                endpoints.append(r'/1/retrieve/{}/{}/{}'.format(
                    authority.canonical_name,
                    scope.canonical_name,
                    collection.canonical_name)
                    )
                for term in collection:
                    endpoints.append(r'/1/retrieve/{}/{}/{}/{}'.format(
                        authority.canonical_name,
                        scope.canonical_name,
                        collection.canonical_name,
                        term.canonical_name)
                        )
    endpoints = [(i, handlers.RetrieveRequestHandler) for i in endpoints]
    endpoints += [
        (r'/', handlers.HeartbeatRequestHandler),
        (r'/status', handlers.HeartbeatRequestHandler),
        (r'/1/validate-identifier', handlers.ValidateIdentifierHandler),
        (r'/1/validate-identifier-set', handlers.ValidateIdentifierSetHandler)
        ]

    return set(endpoints)


def _get_app_settings():
    """Returns app settings.

    """
    return {
        "cookie_secret": config.cookie_secret,
        "compress_response": True
    }


def _get_app():
    """Returns application instance.

    """
    endpoints = _get_app_endpoints()
    log("Assigned endpoint to handler mappings")

    schemas.init([i[0] for i in endpoints])
    return tornado.web.Application(endpoints,
                                   debug=True,
                                   **_get_app_settings())


def run():
    """Runs web service.

    """
    # Initialize application.
    log("Initializing")
    app = _get_app()

    # Open port.
    app.listen(config.port)
    log("Ready")

    # Start processing requests.
    tornado.ioloop.IOLoop.instance().start()


def stop():
    """Stops web service.

    """
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(lambda x: x.stop(), ioloop)
