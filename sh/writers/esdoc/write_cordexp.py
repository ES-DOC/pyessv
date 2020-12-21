# -*- coding: utf-8 -*-
"""
.. module:: write_vocabs.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Writes ES-DOC errata vocabularies to file system.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
import utils



def _write():
    """Writes CORDEXP ES-DOC vocabularies to pyessv-archive.

    """
    pyessv.archive(_write_authority())


def _write_authority():
    """Writes ES-DOC authority.

    """
    authority = utils.write_authority()
    scope = _write_scope(authority)

    return authority


def _write_scope(authority):
    """Writes ES-DOC cmip6 scope.

    """
    scope = pyessv.load('esdoc:cordexp', verbose=False) or pyessv.create_scope(authority,
        'cordexp',
        'ES-DOC controlled Vocabularies (CVs) for use in cordexp',
        create_date=utils.CREATE_DATE,
        label='CORDEXP',
        url='https://github.com/ES-DOC'
        )

    _write_model_topic(scope)

    return scope


def _write_model_topic(scope):
    """Writes ES-DOC model topics.

    """
    collection = pyessv.create_collection(scope, 'model-topic',
        create_date=utils.CREATE_DATE,
        label='Topics',
        description="Model documentation topics"
    )

    pyessv.create_term(collection, 'toplevel',
        create_date=utils.CREATE_DATE,
        description='Top Level',
        label='Top Level'
    )

    pyessv.create_term(collection, 'atmos',
        create_date=utils.CREATE_DATE,
        description='Atmosphere',
        label='Atmosphere'
    )


# Entry point.
if __name__ == '__main__':
    _write()
