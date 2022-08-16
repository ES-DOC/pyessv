import typing

from pyessv import Authority
from pyessv import Scope


def get_config(a: Authority, s: Scope, template_raw: str):
    """Returns dataset identifier parser configuration information derived from a previously declared parsing template.

    :param a: A vocabulary authority.
    :param s: A vocabulary scope.
    :param template_raw: A raw dataset id parsing template.
    
    """
    # Set slots, i.e. set of vocabulary nodes embedded in the template.
    slots: typing.List[str] = \
        [f"{i[2:-2]}".replace("_", "-") for i in template_raw.split(".")[1:]]

    # Set slot overrides.
    if s.namespace == "wcrp:cmip6":
        slots[0] = "activity-id"

    # Set template prefix.
    if s.namespace in ("ecmwf:cc4e", "wcrp:cmip6"):
        prefix = s.canonical_name.upper()
    else:
        prefix = s.canonical_name

    # Set template.
    template: str = f"{prefix}." + ".".join(["{}" for i in slots])

    return {
        "template": template,
        "template_raw": template_raw,
        "seperator": ".",
        "collections": [f"{s}:{i}" for i in slots]
    }
