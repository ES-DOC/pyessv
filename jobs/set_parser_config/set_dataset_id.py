import typing

from pyessv import Authority
from pyessv import Scope


def get_config(a: Authority, s: Scope, template_raw: str):
    """Returns dataset identifier parser configuration information derived
       from a previously declared parsing template.

    :param a: A vocabulary authority.
    :param s: A vocabulary scope.
    :param template: A raw dataset id parsing template.
    :returns: Dataset id parser configuration information.

    """
    # Set specs, i.e. set of parser specification embedded in the template.
    specs: typing.List[str] = template_raw.split(".")[1:]
    specs = [i[2:-2] for i in specs]
    specs = [i.replace("_", "-") for i in specs]

    # Set spec overrides.
    if s.namespace == "wcrp:cmip6":
        specs[0] = "activity-id"

    # Set template prefix.
    if s.namespace in ("ecmwf:cc4e", "wcrp:cmip6"):
        prefix = s.canonical_name.upper()
    else:
        prefix = s.canonical_name

    return {
        "template": template_raw,
        "seperator": ".",
        "specs": [f"const:{prefix}"] + [f"{s}:{i}" for i in specs],
        "suffix": "#"
    }
