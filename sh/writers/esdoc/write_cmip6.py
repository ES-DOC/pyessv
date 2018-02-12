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
    """Writes errata vocabularies to pyessv-archive.

    """
    # Populate esdoc authority with errata vocabs & archive.
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
    scope = pyessv.load('esdoc:cmip6', verbose=False) or pyessv.create_scope(authority,
        'cmip6',
        'ES-DOC controlled Vocabularies (CVs) for use in cmip6',
        create_date=utils.CREATE_DATE,
        label='CMIP6',
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

    for term in pyessv.WCRP.cmip6.realm:
        pyessv.create_term(collection, term.raw_name,
            create_date=utils.CREATE_DATE,
            label=term.description,
        )


# Entry point.
if __name__ == '__main__':
    _write()
