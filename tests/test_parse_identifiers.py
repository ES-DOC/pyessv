# -*- coding: utf-8 -*-

"""
.. module:: testmodel.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv model tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import pytest

import pyessv as LIB


# Test configuration: project, parsing function, template seperator, strictness, identifiers.
_CONFIG = {
    ('cmip5', LIB.parse_dataset_identifer, '.', (
        'cmip5.output1.IPSL.IPSL-CM5A-LR.aqua4K.3hr.atmos.3hr.r2i1p1',
        'cmip5.output2.IPSL.IPSL-CM5A-LR.historicalMisc.mon.ocean.Omon.r2i1p1'
    )),
    ('cmip6', LIB.parse_dataset_identifer, '.', (
        'CMIP6.FAFMIP.IPSL.IPSL-CM6A-LR.amip.r1i1p1f1.Amon.abs550aer.gm',
        # 'CMIP6.CMIP.MIROC.MIROC-ES2L.historical.r1i1p1f2.Emon.mrsoLut.gn#v20190823',
        # 'CMIP6.PMIP.MIROC.MIROC-ES2L.lgm.r1i1p1f2.Emon.mrsoLut.gn#v20191002'
        # 'CMIP6.cmip.miroc.miroc-es2l.historical.r1i1p1f2.emon.mrsolut.gn'
    )),
    ('cordex', LIB.parse_dataset_identifer, '.', (
        'cordex.output.AFR-44.MOHC.MOHC-HadGEM2-ES.rcp60.r12i1p1.HadGEM3-RA.v1.mon.areacella',
        'cordex.output.EUR-11.SMHI.ICHEC-EC-EARTH.rcp85.r12i1p1.RCA4.v1.sem.rsdt'
    )),
}


def _get_invalid_identifiers(identifier, seperator):
    """Returns a set of invalid identifiers by fuxxing a valid identifier.

    """
    # Set parts.
    parts = identifier.split(seperator)

    # Invalid as the number of parts is not as expected.
    yield seperator.join(parts[1:])

    # Invalid as a part has been replaced with invalid value.
    for idx in range(len(parts)):
        new_parts = list(parts)
        new_parts[idx] = 'X!X!X!X!'
        yield seperator.join(new_parts)


def _yield_parameterizations():
    """pyessv-tests: parsing: identifiers

    """
    for project, parser, seperator, identifiers in _CONFIG:
        for identifier in identifiers:
            yield parser, project, identifier, None
        for identifier in identifiers:
            for invalid_identifier in _get_invalid_identifiers(identifier, seperator):
                yield parser, project, invalid_identifier, LIB.TemplateParsingError


@pytest.mark.parametrize("parser, project, identifier, error_class", _yield_parameterizations())
def test_parse_identifiers(parser, project, identifier, error_class):
    """pyessv-tests: parsing: identifiers

    """
    if error_class:
        with pytest.raises(error_class):
            parser(project, identifier)
    else:
        parser(project, identifier)
