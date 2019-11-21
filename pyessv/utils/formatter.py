"""
.. module:: pyessv.utils.formatter.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates name formatting operations.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.utils import compat



def format_canonical_name(name):
    """Formats a canonical name prior to accessing archive.

    """
    if name is not None:
        return compat.str(name) \
            .strip() \
            .replace('_', '-') \
            .replace(' ', '-') \
            .lower()


def format_string(val):
    """Formats a simple string.

    """
    if val is not None:
        return compat.str(val).strip()


def format_io_name(name):
    """Formats a simple string.

    """
    if name is not None:
        return compat.str(name) \
            .strip() \
            .replace('_', '-') \
            .replace(' ', '-') \
            .lower()
