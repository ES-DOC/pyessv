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
    """Writes ES-DOC errata scope.

    """
    scope = pyessv.load('esdoc:errata', verbose=False) or pyessv.create_scope(authority,
        'errata',
        'Controlled Vocabularies (CVs) for use in dataset errata',
        create_date=utils.CREATE_DATE,
        label='Dataset Errata',
        url='https://github.com/ES-DOC/esdoc-errata-ws'
        )

    _write_projects(scope)
    _write_issue_severity(scope)
    _write_issue_status(scope)
    _write_pid_task_action(scope)
    _write_pid_task_status(scope)

    return scope


def _write_issue_status(scope):
    """Writes ES-DOC errata status terms.

    """
    collection = pyessv.create_collection(scope, 'status',
        create_date=utils.CREATE_DATE,
        label='Status',
        description="Errata status codes"
    )

    pyessv.create_term(collection, 'new',
        create_date=utils.CREATE_DATE,
        label='New',
        data={
            'color': '#00ff00'
        }
    )

    pyessv.create_term(collection, 'onhold',
        create_date=utils.CREATE_DATE,
        label='On Hold',
        data={
            'color': '#ff9900'
        }
    )

    pyessv.create_term(collection, 'resolved',
        create_date=utils.CREATE_DATE,
        label='Resolved',
        data={
            'color': '#0c343d'
        }
    )
    pyessv.create_term(collection, 'wontfix',
        create_date=utils.CREATE_DATE,
        label='Wont Fix',
        data={
            'color': '#38761d'
        }
    )


def _write_issue_severity(scope):
    """Writes ES-DOC errata severity terms.

    """
    collection = pyessv.create_collection(scope, 'severity',
        create_date=utils.CREATE_DATE,
        label='Severity',
        description="Errata severity codes"
    )

    pyessv.create_term(collection, 'low',
        create_date=utils.CREATE_DATE,
        label='Low',
        data={
            'color': '#e6b8af',
            'sortOrdinal': 0
        }
    )

    pyessv.create_term(collection, 'medium',
        create_date=utils.CREATE_DATE,
        label='Medium',
        data={
            'color': '#dd7e6b',
            'sortOrdinal': 1
        }
    )

    pyessv.create_term(collection, 'high',
        create_date=utils.CREATE_DATE,
        label='High',
        data={
            'color': '#cc4125',
            'sortOrdinal': 2
        }
    )

    pyessv.create_term(collection, 'critical',
        create_date=utils.CREATE_DATE,
        label='Critical',
        data={
            'color': '#a61c00',
            'sortOrdinal': 3
        }
    )


def _write_pid_task_action(scope):
    """Writes ES-DOC PID task action terms.

    """
    collection = pyessv.create_collection(scope, 'pid-task-action',
        create_date=utils.CREATE_DATE,
        label='Action',
        description="Errata PID task action codes"
    )

    pyessv.create_term(collection, 'insert',
        create_date=utils.CREATE_DATE,
        label='Insert'
    )

    pyessv.create_term(collection, 'delete',
        create_date=utils.CREATE_DATE,
        label='Delete'
    )


def _write_pid_task_status(scope):
    """Writes ES-DOC PID task status terms.

    """
    collection = pyessv.create_collection(scope, 'pid-task-status',
        create_date=utils.CREATE_DATE,
        label='Status',
        description="Errata PID task status codes"
    )

    pyessv.create_term(collection, 'complete',
        create_date=utils.CREATE_DATE,
        label='Complete',
        data={
            'color': '#e6b8af'
        }
    )

    pyessv.create_term(collection, 'error',
        create_date=utils.CREATE_DATE,
        label='Error',
        data={
            'color': '#a61c00'
        }
    )

    pyessv.create_term(collection, 'queued',
        create_date=utils.CREATE_DATE,
        label='Queued',
        data={
            'color': '#dd7e6b'
        }
    )


def _write_projects(scope):
    """Writes ES-DOC errata project terms.

    """
    collection = pyessv.create_collection(scope, 'project',
        create_date=utils.CREATE_DATE,
        label='Project',
        description="Errata supported project codes"
    )

    pyessv.create_term(collection, 'cmip5',
        create_date=utils.CREATE_DATE,
        label='CMIP5',
        data={
            "facets": [
                "wcrp:cmip5:institute",
                "wcrp:cmip5:experiment",
                "wcrp:cmip5:model",
                "wcrp:cmip5:variable"
            ],
            "is_pid_client": False,
            "is_documented": True
        }
    )

    pyessv.create_term(collection, 'cmip6',
        create_date=utils.CREATE_DATE,
        label='CMIP6',
        data={
            "facets": [
                "wcrp:cmip6:institution-id",
                "wcrp:cmip6:experiment-id",
                "wcrp:cmip6:source-id",
                "wcrp:cmip6:variable"
            ],
            "is_pid_client": True,
            "is_documented": True
        }
    )

    pyessv.create_term(collection, 'cordex',
        create_date=utils.CREATE_DATE,
        label='CORDEX',
        data={
            "facets": [
                "wcrp:cordex:institute",
                "wcrp:cordex:experiment",
                "wcrp:cordex:rcm-model",
                "wcrp:cordex:variable"
            ],
            "is_pid_client": False,
            "is_documented": False
        }
    )


# Entry point.
if __name__ == '__main__':
    _write()
