# -*- coding: utf-8 -*-

"""
.. module:: test_model.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv model tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import inspect
import nose

import pyessv as LIB
import tests.utils as tu



# Test configuration: project, parsing function, template seperator, strictness, identifiers.
_CONFIG = {
    ('cmip5', LIB.parse_dataset_identifer, '.', LIB.PARSING_STRICTNESS_1, (
        'cmip5.output1.IPSL.IPSL-CM5A-LR.aqua4K.3hr.atmos.3hr.r2i1p1',
        'cmip5.output2.IPSL.IPSL-CM5A-LR.historicalMisc.mon.ocean.Omon.r2i1p1'
    )),
    ('cmip6', LIB.parse_dataset_identifer, '.', LIB.PARSING_STRICTNESS_1, (
        'cmip6.fafmip.IPSL.IPSL-CM6A-LR.amip.r1i1p1f1.amon.abs550aer.gm',
    )),
    ('cordex', LIB.parse_dataset_identifer, '.', LIB.PARSING_STRICTNESS_1, (
        'cordex.output.AFR-44.MOHC.MOHC-HadGEM2-ES.rcp60.r12i1p1.HadGEM3-RA.v1.mon.areacella',
        'cordex.output.EUR-11.SMHI.ICHEC-EC-EARTH.rcp85.r12i1p1.RCA4.v1.sem.rsdt'
    )),
}



def test_parse_identifiers():
    """pyessv-tests: parsing: identifiers

    """
    def positive_test(parser, project, identifier, strictness):
        parser(project, identifier, strictness)

    @nose.tools.raises(LIB.TemplateParsingError)
    def negative_test(parser, project, identifier, strictness):
        parser(project, identifier, strictness)

    # Iterate identifiers & perform +ve / -ve tests:
    for project, parser, seperator, strictness, identifiers in _CONFIG:
        assert inspect.isfunction(parser)
        for identifier in identifiers:
            # ... +ve test:
            desc = 'identifier parsing test (+ve) --> {} :: {}'.format(project, identifier)
            tu.init(positive_test, desc)
            yield positive_test, parser, project, identifier, strictness

            # ... -ve tests:
            for invalid_identifier in _get_invalid_identifiers(identifier, seperator):
                desc = 'identifier parsing test (-ve) --> {} :: {}'.format(project, invalid_identifier)
                tu.init(negative_test, desc)
                yield negative_test, parser, project, invalid_identifier, strictness


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
