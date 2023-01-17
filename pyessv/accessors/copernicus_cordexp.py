import pyessv


def get_scope():
    """Returns target scope.

    """
    return pyessv.COPERNICUS.CORDEXP


def get_institutes():
    """Returns set of participating institutes.

    """
    scope = get_scope()

    return scope.institution_id
