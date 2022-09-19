import re

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


def get_config(s: Scope, template_raw: str) -> dict:
    """Returns directory identifier parser configuration information derived
       from a previously declared parsing template.

    :param s: A vocabulary scope.
    :param template_raw: A raw dataset id parsing template.
    :returns: Directory name parser configuration information.

    """
    # Skip ill-defined.
    if s.namespace == "wcrp:e3sm":
        return

    parts = [i.replace("_", "-") for i in re.findall("%\((\w*)\)s", template_raw)[2:]]

    return {
        "seperator": "/",
        "template": template_raw,
        "specs": [_get_prefix_spec(s)] + [_get_part_spec(s, i) for i in parts],
        "suffix": "#"
    }


def _get_prefix_spec(s: Scope) -> dict:
    """Maps a scope to a constant specifiction acting as identifier prefix.
    
    """
    try:
        prefix: str = _PROJECT_PREFIX[s.namespace]
    except KeyError:
        prefix = s.canonical_name.upper()

    return {
        "type": "const",
        "value": prefix,
        "is_required": True
    }


def _get_part_spec(s: Scope, part: str) -> dict:
    """Maps a template part to a collection specifiction.
    
    """
    if s.namespace == "wcrp:cmip6" and part == "activity-drs":
        part = "activity-id"

    return {
        "type": "collection",
        "namespace": f"{s.namespace}:{part}",
        "is_required": True
    }
