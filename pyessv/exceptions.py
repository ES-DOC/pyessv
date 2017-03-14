# -*- coding: utf-8 -*-

"""
.. module:: pyessv.exceptions.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package exceptions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
class ValidationError(ValueError):
	"""A validation error raised by the package validator.

	"""
	def __init__(self, msg):
		"""Object constructor.

		"""
		super(ValidationError, self).__init__(msg)


class InvalidPartitionError(ValueError):
	"""An error raised when user tries to access an invalid parition.

	"""
	def __init__(self, key):
		"""Object constructor.

		"""
		msg = "Unsupported pyessv partition: {}".format(key)
		super(InvalidPartitionError, self).__init__(msg)


class InvalidOptionError(ValueError):
	"""An error raised when user tries to access an invalid option.

	"""
	def __init__(self, option):
		"""Object constructor.

		"""
		msg = "Unsupported pyessv option: {}".format(option)
		super(InvalidOptionError, self).__init__(msg)


class InvalidAssociationError(ValueError):
	"""An error raised an invalid association is declared.

	"""
	def __init__(self, association):
		"""Object constructor.

		"""
		msg = "Unsupported association: {}".format(association)
		super(InvalidAssociationError, self).__init__(msg)
