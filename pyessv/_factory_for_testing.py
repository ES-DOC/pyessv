# -*- coding: utf-8 -*-
"""
.. module:: utils.factory.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: Test issue factory.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv


# Collection of materials, i.e. supporting images, graphs ... etc.
_MATERIALS = []

# Collection of data set patters used when generating test dataset identifiers.
_DATASETS_PATTERNS = {
    'cmip5': u'cmip5.{}.{}.{}.{}.{}.{}.{}.r1i1p1#v20180101',
    'cmip6': u'CMIP6.{}.{}.{}.{}.r1i1p1f1.{}.Emon.{}#v20180101',
    'cordex': u'cordex.{}.{}.{}.{}.{}.r12i1p1.{}.v1.{}.{}#v20180101'
}


def get_test_datasets(project, existing=[]):
    """Returns a collection of test dataset identifiers.

    :param str project: Project code.
    :param list existing: Dataset identifiers to be included in the result.

    :returns: Collection of test datasets.
    :rtype: list

    """
    return [_get_test_dataset(project) for i in range(5)] + existing


def _get_test_dataset(project):
    """Returns a test dataset identifier.

    """
    pattern = _DATASETS_PATTERNS[project]

    if project == 'cmip5':
        return pattern.format(
            pyessv.load_random('wcrp:cmip5:product', field='raw_name'),
            pyessv.parse('wcrp:cmip5:institute:ipsl', field='raw_name'),
            pyessv.load_random('wcrp:cmip5:model', field='raw_name'),
            pyessv.load_random('wcrp:cmip5:experiment', field='raw_name'),
            pyessv.load_random('wcrp:cmip5:time-frequency', field='raw_name'),
            pyessv.load_random('wcrp:cmip5:realm', field='raw_name'),
            pyessv.load_random('wcrp:cmip5:cmor-table', field='raw_name')
            )

    elif project == 'cmip6':
        return pattern.format(
            pyessv.load_random('wcrp:cmip6:activity-id', field='raw_name'),
            pyessv.parse('wcrp:cmip6:institution-id:ipsl', field='raw_name'),
            pyessv.load_random('wcrp:cmip6:source-id', field='raw_name'),
            pyessv.load_random('wcrp:cmip6:experiment-id', field='raw_name'),
            pyessv.load_random('wcrp:cmip6:table-id', field='raw_name'),
            pyessv.load_random('wcrp:cmip6:grid-label', field='raw_name')
            )

    elif project == 'cordex':
        return pattern.format(
            pyessv.load_random('wcrp:cordex:product', field='raw_name'),
            pyessv.load_random('wcrp:cordex:domain', field='raw_name'),
            pyessv.parse('wcrp:cordex:institute:ipsl-ineris', field='raw_name'),
            pyessv.load_random('wcrp:cordex:driving-model', field='raw_name'),
            pyessv.load_random('wcrp:cordex:experiment', field='raw_name'),
            pyessv.load_random('wcrp:cordex:rcm-name', field='raw_name'),
            pyessv.load_random('wcrp:cordex:time-frequency', field='raw_name'),
            pyessv.load_random('wcrp:cordex:variable', field='raw_name')
            )
