import typing

from pyessv import Authority
from pyessv import Scope


# Map: project namespace -> project drs prefix.
_PROJECT_PREFIX = {
    "ecmwf:c3s-cmip5": "c3s-cmip5",
    "ecmwf:c3s-cordex": "c3s-cordex",
    "wcrp:cordex-adjust": "CORDEX-adjust",
    "wcrp:geomip": "GeoMIP", 
    "wcrp:input4mips": "input4MIPs", 
    "wcrp:obs4mips": "obs4MIPs", 
}


def get_config(a: Authority, s: Scope, template_raw: str):
    """Returns directory identifier parser configuration information derived
       from a previously declared parsing template.

    :param a: A vocabulary authority.
    :param s: A vocabulary scope.
    :param template_raw: A raw dataset id parsing template.
    :returns: Directory name parser configuration information.

    """
    # Skip ill-defined.
    if s.namespace == "wcrp:e3sm":
        return

    # Set specs.
    specs: typing.List[str] = template_raw.split("%(")[2:]
    specs = [i.split(")")[0] for i in specs]
    specs = [i.replace("_", "-") for i in specs]

    # Set spec overrides.
    if s.namespace == "wcrp:cmip6":
        specs[1] = "activity-id"

    # Set directory prefix. 
    try:
        prefix: str = _PROJECT_PREFIX[s.namespace]
    except KeyError:
        prefix = s.canonical_name.upper()

    return {
        "template": template_raw,
        "seperator": "/",
        "specs": [f"const:{prefix}"] + [f"{s}:{i}" for i in specs[1:]]
    }
