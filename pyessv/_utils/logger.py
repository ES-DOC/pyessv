# -*- coding: utf-8 -*-

"""
.. module:: pyessv._utils.logger.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package logging utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import arrow

from pyessv._utils.compat import str



# Set of logging levels.
LOG_LEVEL_DEBUG = 'DUBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_CRITICAL = 'CRITICAL'
LOG_LEVEL_FATAL = 'FATAL'

# Defaults.
_DEFAULT_APP = 'PYESSV'
_DEFAULT_INSTITUTE = 'ES-DOC'

# Text to display when passed a null message.
_NULL_MSG = '-------------------------------------------------------------------------------'


def _get_formatted_message(msg, level, app, institute):
    """Returns a message formatted for logging.

    """
    if msg is None:
        return _NULL_MSG
    else:
        return '{0} [{1}] :: {2} {3} :: {4}'.format(
            str(arrow.get())[0:-6],
            level,
            institute,
            app,
            str(msg).strip()
            )


def log(
    msg=None,
    level=LOG_LEVEL_INFO,
    app=_DEFAULT_APP,
    institute=_DEFAULT_INSTITUTE
    ):
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str level: Message level (e.g. INFO).
    :param str app: Application emitting log message (e.g. libIGCM).
    :param str institute: Institute emitting log message (e.g. libIGCM).

    """
    # TODO use structlog/logstash.
    print(_get_formatted_message(msg, level, app, institute))


def log_error(
    err,
    app=_DEFAULT_APP,
    institute=_DEFAULT_INSTITUTE
    ):
    """Logs a runtime error.

    :param HermesClientException err: Error to be written to log.
    :param str level: Message level (e.g. INFO).
    :param str app: Application emitting log message (e.g. libIGCM).
    :param str institute: Institute emitting log message (e.g. libIGCM).

    """
    msg = '!! RUNTIME ERROR !! :: '
    if issubclass(BaseException, err.__class__):
        msg += '{} :: '.format(err.__class__)
    msg += '{}'.format(err)
    log(msg, LOG_LEVEL_ERROR, app, institute)
