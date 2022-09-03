from pyessv import Authority
from pyessv import Scope


def get_config(a: Authority, s: Scope, template_raw: str):
    """Returns directory identifier parser configuration information derived from a previously declared parsing template.

    :param a: A vocabulary authority.
    :param s: A vocabulary scope.
    :param template_raw: A raw dataset id parsing template.
    
    """
    # Skip ill-defined. 
    if s.namespace == "wcrp:e3sm":
        return

    # Set raw specs.
    specs = [i.split(")")[0] for i in template_raw.split("%(")[2:]]

    # Set spec overrides.
    if s.namespace == "wcrp:cmip6":
        specs[1] = "activity-id"
    
    if specs[0] == "project" or s.namespace != "wcrp:cmip6":
        specs = [f"const:{s.canonical_name}"] + [f"{s}:{i}" for i in specs[1:]]
    elif s.namespace == "wcrp:cmip6":
        specs = ["wcrp:global:mip-era"] + [f"{s}:{i}" for i in specs[1:]]
    else:
        specs = [f"{s}:{i}" for i in specs]

    return {
        "template": template_raw,
        "seperator": "/",
        "specs": specs
    }
