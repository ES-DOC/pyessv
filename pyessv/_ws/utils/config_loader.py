# -*- coding: utf-8 -*-
"""
.. module:: utils.config.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Configuration utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os
import logger
import json

from pyessv._ws.utils.constants import HTTP_RESPONSE_SERVER_ERROR
from pyessv._ws.utils.convertor import json_file_to_namedtuple
from pyessv._ws.utils.convertor import to_namedtuple
from pyessv._ws.utils.exceptions import ConfigFileNotFoundException



# Default configuration file path.
_CONFIG_FPATH = "ws.conf"

# Default configuration.
_DEFAULT = {
    'cookie_secret': 'p2FAdrUN3tac',
    'host': 'localhost',
    'apply_security_policy': False,
    'mode': 'dev',
    'port': 5010
}

# Configuration data.
data = to_namedtuple(_DEFAULT)


def _get_config_fpath(config_path):
    """Returns configuration file path.

    """
    path = os.getenv('PYESSV_LIB_HOME')
    path = os.path.join(path, "ops/config")
    path = os.path.join(path, _CONFIG_FPATH)
    if os.path.exists(path):
        return path


def _init():
    """Initializes configuration.

    """
    global data

    fpath = _get_config_fpath('ws.conf')
    if fpath is not None:
        data = json_file_to_namedtuple(fpath)
        logger.log_web("Config file loaded @ {}".format(fpath))
    else:
        logger.log_web_warning("Web-service config file not found: reverted to default")


# Auto-initialize.
_init()
