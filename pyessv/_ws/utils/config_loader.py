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
from pyessv._ws.utils.exceptions import ConfigFileNotFoundException



# Default configuration file path.
_CONFIG_FPATH = "ws.conf"

# Configuration data.
data = None


def _get_config_fpath(config_path):
    """Returns configuration file path.

    """
    path = os.getenv('PYESSV_LIB_HOME')
    path = os.path.join(path, "ops/config")
    path = os.path.join(path, _CONFIG_FPATH)
    if not os.path.exists(path):
        raise ConfigFileNotFoundException(fpath)

    return path


def _init():
    """Initializes configuration.

    """
    global data

    # Get configuration file path (falling back to template if necessary).
    fpath = _get_config_fpath('ws.conf')

    # Convert config file to a named tuple.
    data = json_file_to_namedtuple(fpath)

    logger.log_web("Configuration file loaded @ {}".format(fpath))


# Auto-initialize.
_init()
