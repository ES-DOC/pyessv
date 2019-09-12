# -*- coding: utf-8 -*-

"""
.. module:: utils.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import datetime as dt

import pyessv



# Ensure we use fixed creation date.
CREATE_DATE = dt.datetime(2017, 6, 21)


def write_authority():
    """Writes ES-DOC authority.

    """
    return pyessv.load('esdoc', verbose=False) or pyessv.create_authority(
        'esdoc',
        'Earth System Documentation',
        label='ES-DOC',
        url='https://es-doc.org',
        create_date=CREATE_DATE
        )
