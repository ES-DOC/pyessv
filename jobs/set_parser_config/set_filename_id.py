from pyessv import Authority
from pyessv import Scope


def get_config(a: Authority, s: Scope, template_raw: str):
    """Returns directory identifier parser configuration information derived
       from a previously declared parsing template.

    :param a: A vocabulary authority.
    :param s: A vocabulary scope.
    :param template_raw: A raw dataset id parsing template.
    :returns: File name parser configuration information.

    """
    # Skip ill-defined.
    if s.namespace == "wcrp:e3sm":
        return

    # Discard period start/end + file type.
    template = template_raw.split("[")[0]

    # Set specs.
    specs = [i.split(")")[0] for i in template.split("%(")[1:]]
    specs = [i.replace("_", "-") for i in specs]
    specs = [f"{s}:{i}" for i in specs]

    # Set spec overrides.
    if s.namespace == "ecmwf:cc4e":
        specs[0] = "const:cc4e"

    # Append period start - end regex.
    if s.namespace != "wcrp:input4mips":
        specs.append("regex:^[0-9]{4}-[0-9]{4}$")

    # Append file type.
    specs.append("regex:^nc$")

    return {
        "template": template_raw,
        "seperator": "_",
        "specs": specs
    }
