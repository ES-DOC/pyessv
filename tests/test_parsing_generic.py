import pyessv


# Test configuration: project, parsing function, template seperator, strictness, identifiers.
_CONFIG = {
    ('cmip5', pyessv.parse_dataset_identifer, '.', (
        'cmip5.output1.IPSL.IPSL-CM5A-LR.aqua4K.3hr.atmos.3hr.r2i1p1',
        'cmip5.output2.IPSL.IPSL-CM5A-LR.historicalMisc.mon.ocean.Omon.r2i1p1'
    )),
    ('cmip6', pyessv.parse_dataset_identifer, '.', (
        'CMIP6.FAFMIP.IPSL.IPSL-CM6A-LR.amip.r1i1p1f1.Amon.abs550aer.gm',
        # 'CMIP6.CMIP.MIROC.MIROC-ES2L.historical.r1i1p1f2.Emon.mrsoLut.gn#v20190823',
        # 'CMIP6.PMIP.MIROC.MIROC-ES2L.lgm.r1i1p1f2.Emon.mrsoLut.gn#v20191002'
        # 'CMIP6.cmip.miroc.miroc-es2l.historical.r1i1p1f2.emon.mrsolut.gn'
    )),
    ('cordex', pyessv.parse_dataset_identifer, '.', (
        'cordex.output.AFR-44.MOHC.MOHC-HadGEM2-ES.rcp60.r12i1p1.HadGEM3-RA.v1.mon.areacella',
        'cordex.output.EUR-11.SMHI.ICHEC-EC-EARTH.rcp85.r12i1p1.RCA4.v1.sem.rsdt'
    )),
}


def test_parse_dataset_identifiers():
    scope = pyessv.get_cached("wcrp:cmip6")
    parser_type = pyessv.PARSER_TYPE_DATASET_ID
    identifier = "CMIP6.FAFMIP.IPSL.IPSL-CM6A-LR.amip.r1i1p1f1.Amon.abs550aer.gm"

    pyessv.parse_identifer(scope, parser_type, identifier)
