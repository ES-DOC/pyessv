"""
.. module:: pyessv.archive.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates access to archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv.cache import cache
from pyessv.cache import get_cached
from pyessv.io_manager import write
from pyessv.model import Authority



def archive(authority):
    """Archive authority to file system.

    """
    cache(authority)
    for authority in get_cached(Authority):
        write(authority)
