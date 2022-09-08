import typing

from pyessv import Authority
from pyessv import Scope


def get_config(a: Authority, s: Scope, template: str):
    """Returns dataset identifier parser configuration information derived
       from a previously declared parsing template.

    :param a: A vocabulary authority.
    :param s: A vocabulary scope.
    :param template: A raw dataset id parsing template.

    """
    # Set specs, i.e. set of parser specification embedded in the template.
    specs: typing.List[str] = [f"{i[2:-2]}".replace("_", "-") for i in template.split(".")[1:]]

    # Set spec overrides.
    if s.namespace == "wcrp:cmip6":
        specs[0] = "activity-id"

    # Set template prefix.
    if s.namespace in ("ecmwf:cc4e", "wcrp:cmip6"):
        prefix = s.canonical_name.upper()
    else:
        prefix = s.canonical_name

    return {
        "template": template,
        "seperator": ".",
        "specs": [f"const:{prefix}"] + [f"{s}:{i}" for i in specs],
        "suffix": "#"
    }
