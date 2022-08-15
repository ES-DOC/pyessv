"""
.. module:: pyessv.exceptions.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package exceptions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
class NamespaceParsingError(ValueError):
	"""A parsing error raised by the package parser.

	"""
	def __init__(self, typeof, name):
		"""Object constructor.

		"""
		msg = 'A parsing error has occurred: typeof={}, name={}'.format(typeof, name)
		super(NamespaceParsingError, self).__init__(msg)


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
