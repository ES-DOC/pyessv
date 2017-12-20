# -*- coding: utf-8 -*-

"""
.. module:: utils.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import arrow

import pyessv



# Ensure we use fixed creation date.
CREATE_DATE = arrow.get('2017-06-21 00:00:00.000000+0000').datetime


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
