from pyessv.cache import encache
from pyessv.cache import get_cached
from pyessv.io_manager import write
from pyessv.model import Authority


def archive(authority):
    """Archive authority to file system.

    """
    encache(authority)
    for authority in get_cached(Authority):
        write(authority)
