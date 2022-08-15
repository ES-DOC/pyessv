import typing

from pyessv import Authority
from pyessv import Scope


def get_config(a: Authority, s: Scope, template_raw: str):
    """Returns dataset identifier parser configuration information derived from a previously declared parsing template.

    :param a: A vocabulary authority.
    :param s: A vocabulary scope.
    :param template_raw: A raw dataset id parsing template.
    
    """
    # Destructure raw template into prefix and slots.
    prefix, slots = _parse_template(a, s, template_raw)

    # Set pyessv template.
    template: str = f"{prefix}." + ".".join(["{}" for i in slots])

    # Strip surrounding interpolation instruction.
    slots: typing.List[str] = [f"{i[2:-2]}".replace("_", "-") for i in slots]

    # Perform scope level parsing.
    _parse_slots(s, slots)

    # Transform slots so that they are valid pyessv collection namespaces.
    collections: typing.List[str] = [f"{s}:{i}" for i in slots]

    return {
        "prefix": prefix,
        "template": template,
        "template_raw": template_raw,
        "seperator": ".",
        "collections": collections
    }


def _parse_template(a: Authority, s: Scope, template_raw: str) -> typing.Tuple[str, typing.List[str]]:
    """Returns 2 member tuple consisting of a template prefix plus collection references.
    
    """
    if s.namespace in ("ecmwf:cc4e", "wcrp:cmip6"):
        return s.canonical_name.upper(), template_raw.split(".")[1:]

    return s.canonical_name, template_raw.split(".")[1:]


def _parse_slots(s: Scope, slots: typing.List[str]):
    """Parses template slots modifying as appropriate.
    
    """
    if s.namespace == "wcrp:cmip6":
        slots[0] = "activity-id"
