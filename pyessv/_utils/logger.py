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



# Set of logging levels.
LOG_LEVEL_DEBUG = 'DUBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_CRITICAL = 'CRITICAL'
LOG_LEVEL_FATAL = 'FATAL'

# Defaults.
_DEFAULT_APP = "PYESSV"
_DEFAULT_MODULE = "**"
_DEFAULT_INSTITUTE = "IPSL"

# Text to display when passed a null message.
_NULL_MSG = "-------------------------------------------------------------------------------"


def _get_formatted_message(msg, module, level, app, institute):
    """Returns a message formatted for logging.

    """
    if msg is None:
        return _NULL_MSG
    else:
        return "{0} [{1}] :: {2} {3} > {4} : {5}".format(
            unicode(arrow.get())[0:-6],
            level,
            institute,
            app,
            module,
            unicode(msg).strip()
            )


def log(
    msg=None,
    module=_DEFAULT_MODULE,
    level=LOG_LEVEL_INFO,
    app=_DEFAULT_APP,
    institute=_DEFAULT_INSTITUTE
    ):
    """Outputs a message to log.

    :param str msg: Message to be written to log.
    :param str module: Module emitting log message (e.g. MQ).
    :param str level: Message level (e.g. INFO).
    :param str app: Application emitting log message (e.g. libIGCM).
    :param str institute: Institute emitting log message (e.g. libIGCM).

    """
    # TODO use structlog.
    print _get_formatted_message(msg, module, level, app, institute)


def log_error(
    err,
    module=_DEFAULT_MODULE,
    app=_DEFAULT_APP,
    institute=_DEFAULT_INSTITUTE
    ):
    """Logs a runtime error.

    :param HermesClientException err: Error to be written to log.
    :param str module: Module emitting log message (e.g. MQ).
    :param str level: Message level (e.g. INFO).
    :param str app: Application emitting log message (e.g. libIGCM).
    :param str institute: Institute emitting log message (e.g. libIGCM).

    """
    msg = "!! {0} RUNTIME ERROR !! :: ".format(module)
    if issubclass(BaseException, err.__class__):
        msg += "{} :: ".format(err.__class__)
    msg += "{}".format(err)
    log(msg, module, LOG_LEVEL_ERROR, app, institute)
