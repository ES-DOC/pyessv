# -*- coding: utf-8 -*-

"""
.. module:: utils.exceptions.py
   :platform: Unix
   :synopsis: Custom exceptions used in this module for better readability of code.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._ws.utils import constants



class WebServiceError(Exception):
    """Web service error wrapper.

    """
    def __init__(self, msg, response_code):
        """Instance constructor.

        """
        super(WebServiceError, self).__init__(msg)
        self.response_code = response_code


class RequestValidationException(WebServiceError):
    """Base class for request validation exceptions.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(RequestValidationException, self).__init__(msg, constants.HTTP_RESPONSE_BAD_REQUEST_ERROR)


class InvalidJSONError(RequestValidationException):
    """Raised if the submitted request data is invalid according to a JSON schema.

    """
    def __init__(self, json_err):
        """Instance constructor.

        """
        msg = json_err.message.strip()
        try:
            self.field = json_err.path[0]
        except Exception as err:
            self.field = msg.split("'")[1]
        super(InvalidJSONError, self).__init__(msg)


class UnknownEndpointException(WebServiceError):
    """Base class for unknown endpoint exceptions.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(UnknownEndpointException, self).__init__(msg, constants.HTTP_RESPONSE_BAD_REQUEST_ERROR)


class ConfigFileNotFoundException(WebServiceError):
    """Configuration file not found exception.

    """
    def __init__(self, path):
        """Instance constructor.

        """
        msg = "configuration file could not be found : {}".format(path)
        super(ConfigFileNotFoundException, self).__init__(msg, constants.HTTP_RESPONSE_SERVER_ERROR)


# Map of managed error codes.
ERROR_CODES = {
    InvalidJSONError: 900,
    ConfigFileNotFoundException: 901,
}
