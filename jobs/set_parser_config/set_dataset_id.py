import re

from pyessv import Scope


def get_config(s: Scope, template_raw: str) -> dict:
    """Returns dataset identifier parser configuration information derived
       from a previously declared parsing template.

    :param s: A vocabulary scope.
    :param template: A raw dataset id parsing template.
    :returns: Dataset id parser configuration information.

    """
    parts = [i.replace("_", "-") for i in re.findall("%\((\w*)\)s", template_raw)]
    if s.namespace == "wcrp:input4mips":
        parts = parts[1:]

    return {
        "seperator": ".",
        "template": template_raw,
        "specs": [_get_prefix_spec(s)] + [_get_part_spec(s, i) for i in parts],
        "suffix": "#"
    }


def _get_prefix_spec(s: Scope) -> dict:
    """Maps a scope to a constant specifiction acting as identifier prefix.
    
    """
    if s.namespace in ("ecmwf:cc4e", "wcrp:cmip6"):
        prefix = s.canonical_name.upper()
    elif s.namespace in ("wcrp:input4mips"):
        prefix = s["activity-id"]["input4mips"].raw_name
    else:
        prefix = s.canonical_name

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
