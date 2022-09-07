from pyessv.utils import compat


def format_attribute_name(name):
    """Formats an attribute name prior to accessing either a collection or arbitrary data.

    """
    if name is not None:
        return compat.str(name) \
            .strip() \
            .replace('_', '-') \
            .replace(' ', '-') \
            .lower()


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
