import re

from pyessv import IDENTIFIER_TYPE_SET, IDENTIFIER_TYPE_FILENAME
from pyessv.parsing.identifiers.config import get_config


def build_identifier(scope, identifier_type, terms, regex_terms={}):
    """Build an identifier.

    :param scope: Scope associated with the identifier to be parsed.
    :param identifier_type: Type of parser to be used.
    :param terms: Set of known term.
    :param regex_terms: Dictionary of terms matching the regex term in spec : {term:value,...}

    """

    assert identifier_type in IDENTIFIER_TYPE_SET, f"Unsupported parser type: {identifier_type}"

    # Set parsing configuration.
    cfg = get_config(scope, identifier_type)

    # Template split from configuration
    template_part = re.findall("%\((\w*)\)s", cfg.template)
    ("root" in template_part) and template_part.remove("root")  # remove root from template_part if exist
    if len(template_part) != len(cfg.specs):
        msg = f'Invalid config file for identifier : {identifier_type} : different count between template and spec'
        raise ValueError(msg)

    # Check if all cfg.spec are in terms or in regex_terms
    known_terms = [term.collection.all_names for term in terms]
    known_terms.extend(set([(name,) for name in regex_terms.keys()]))  # hack to fake multiple name in regex_term
    known_terms = set.union(*known_terms)
    # print(set.union(*known_terms))
    for idx, spec in enumerate(cfg.specs):
        if not spec.startswith("const"):
            if spec.startswith("regex"):
                if template_part[idx] not in known_terms:
                    msg = f'Invalid known terms : missing {template_part[idx]} to build {identifier_type}'
                    raise ValueError(msg)
            elif spec.split(":")[-1] not in known_terms:
                msg = f'Invalid known terms : missing {spec.split(":")[-1]} to build {identifier_type}'
                raise ValueError(msg)

    # Building the identifier
    identifier_part = list()
    for idx, spec in enumerate(cfg.specs):
        # ... constants.
        if spec.startswith("const"):
            identifier_part.append(spec.split(":")[1])

        # ... regular expressions
        elif spec.startswith("regex"):
            identifier_part.append(regex_terms[template_part[idx]])

        # ... collection members.
        else:
            for term in terms:
                if spec.replace(term.scope.namespace + ":", "") in term.collection.all_names:
                    identifier_part.append(term.raw_name)
                    break

    result = cfg.seperator.join(identifier_part)

    # only for filename identifier_type:
    if identifier_type == IDENTIFIER_TYPE_FILENAME:
        result += "." + cfg.template.split(".")[-1]

    return result
