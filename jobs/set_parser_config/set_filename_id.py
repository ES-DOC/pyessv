import re

from pyessv import Scope


def get_config(s: Scope, template_raw: str) -> dict:
    """Returns directory identifier parser configuration information derived
       from a previously declared parsing template.

    :param s: A vocabulary scope.
    :param template_raw: A raw dataset id parsing template.
    :returns: File name parser configuration information.

    """
    if s.namespace == "wcrp:e3sm":
        return

    parts = [i for i in re.findall("%\((\w*)\)s", template_raw)]
    if parts[-2] == "period_start" and parts[-1] == "period_end":
        parts = parts[:-2] + ["time_range"]

    return {
        "seperator": "_",
        "template": template_raw,
        "specs": [_get_part_spec(s, i) for i in parts] + [_get_suffix_spec()]
    }


def _get_part_spec(s: Scope, part: str) -> dict:
    """Maps a template part to a collection specifiction.
    
    """
    if s.namespace == "wcrp:cmip6" and part == "activity-drs":
        part = "activity-id"

    if s.namespace == "ecmwf:cc4e" and part == "project":
        return {
            "type": "const",
            "value": "cc4e",
            "is_required": True
        }

    elif part == "time_range":
        return {
            "type": "regex",
            "expression": "^[0-9]*-[0-9]*$",
            "is_required": False
        }

    else:
        for c in s:
            if part in c.all_names:
                return {
                    "type": "collection",
                    "namespace": f"{c}",
                    "is_required": True
                }
        print(f"Pyessv doesn't know this collection : {part} for this scope : {s}")
    return {
        "type": "collection",
        "namespace": f"{s.namespace}:{part}",
        "is_required": True
    }


def _get_suffix_spec() -> dict:
    """Maps a scope to a constant specifiction acting as identifier prefix.
    
    """
    return {
        "type": "regex",
        "expression": "^nc$",
        "is_required": True
    }
