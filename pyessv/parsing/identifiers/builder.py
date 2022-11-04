import re

from pyessv import IDENTIFIER_TYPE_SET, IDENTIFIER_TYPE_FILENAME
from pyessv.parsing.identifiers.config import get_config
from pyessv.parsing.identifiers.config import CollectionParsingSpecification
from pyessv.parsing.identifiers.config import ConstantParsingSpecification
from pyessv.parsing.identifiers.config import RegExParsingSpecification


def build_identifier(scope, identifier_type, terms, regex_terms={}):
    """Build an identifier.

    :param scope: Scope associated with the identifier to be parsed.
    :param identifier_type: Type of parser to be used.
    :param terms: Set of known term.
    :param regex_terms: Dictionary of terms matching the regex term in spec : {term:value,...}

    :return: str of identifer according to template and input terms
    :rtype: str | ValueError

    Note : currently, if a term is optional in the template (i.e in bracket []) and if there is no input term
    corresponding : this function return the result with all known term but the identifier could be invalid

    Note 2 :  currently, the regex for time period is NOT dependant of the time frequency whereas in fact there are.
    A possible upgrade would be to find a method to take into account the time_frequency either in config, or in pyessv
    or let the pyessv client to deal with it
    """

    assert identifier_type in IDENTIFIER_TYPE_SET, "Unsupported parser type: {}".format(identifier_type)

    # Set parsing configuration.
    cfg = get_config(scope, identifier_type)

    # retrieve optional collection in spec
    all_optional_template_str = re.findall("\[(.+?)\]", cfg.template)
    optional_template_part = [it for sub in
                              [re.findall("%\((\w+)\)s", opt_col) for opt_col in all_optional_template_str] for it in
                              sub]

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
        if not isinstance(spec, ConstantParsingSpecification) and \
           template_part[idx] not in optional_template_part:
            if isinstance(spec, RegExParsingSpecification):
                if template_part[idx] not in known_terms:
                    msg = f'Invalid known terms : missing {template_part[idx]} to build {identifier_type}'
                    raise ValueError(msg)
            elif spec.namespace.split(":")[-1] not in known_terms:
                msg = f'Invalid known terms : missing {spec.namespace.split(":")[-1]} to build {identifier_type}'
                raise ValueError(msg)

    # Building the identifier
    identifier_part = list()
    for idx, spec in enumerate(cfg.specs):
        # ... collection members.
        if isinstance(spec, CollectionParsingSpecification):
            for term in terms:
                if spec.namespace.replace(term.scope.namespace + ":", "") in term.collection.all_names:
                    identifier_part.append(term.raw_name)
                    break

        # ... constants.
        elif isinstance(spec, ConstantParsingSpecification):
            identifier_part.append(spec.value)

        # ... regular expressions
        elif isinstance(spec, RegExParsingSpecification):
            if template_part[idx] in regex_terms.keys():
                identifier_part.append(regex_terms[template_part[idx]])

        else:
            raise ValueError("Unsupported specification type")

    result = cfg.seperator.join(identifier_part)

    # only for filename identifier_type:
    if identifier_type == IDENTIFIER_TYPE_FILENAME:
        result += "." + cfg.template.split(".")[-1]

    return result
