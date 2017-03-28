# -*- coding: utf-8 -*-

"""
.. module:: pyessv._exceptions.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package exceptions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
class ParsingError(ValueError):
	"""A parsing error raised by the package parser.

	"""
	def __init__(self, typeof, name):
		"""Object constructor.

		"""
		msg = 'A parsing error has occurred: typeof={}, name={}'.format(typeof, name)
		super(ParsingError, self).__init__()


class ValidationError(ValueError):
	"""A validation error raised by the package validator.

	"""
	def __init__(self, msg):
		"""Object constructor.

		"""
		super(ValidationError, self).__init__(msg)


class InvalidAssociationError(ValueError):
	"""An error raised an invalid association is declared.

	"""
	def __init__(self, association):
		"""Object constructor.

		"""
		msg = 'Unsupported association: {}'.format(association)
		super(InvalidAssociationError, self).__init__(msg)
