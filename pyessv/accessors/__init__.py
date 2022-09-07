from pyessv.accessors import copernicus_cordexp
from pyessv.accessors import esdoc_cmip6
from pyessv.accessors import wcrp_cmip6


ACCESSORS = {
    'copernicus': {
        'cordexp': copernicus_cordexp
    },
    'esdoc': {
        'cmip6': esdoc_cmip6
    },
    'wcrp': {
        'cmip6': wcrp_cmip6
    }
}
