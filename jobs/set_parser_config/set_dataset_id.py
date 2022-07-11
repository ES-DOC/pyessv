from pyessv import Authority
from pyessv import Scope
from pyessv.io_manager import write_scope_parser_config
from pyessv import PARSER_TYPE_DATASET_ID


def generate(a: Authority, s: Scope, template: str):
    template_parts = template.split(".")

    if s.canonical_name != "cmip6" and s.canonical_name != template_parts[0]:
        print(f"WARNING :: unmappable dataset_id :: {s} ")
        return

    template_parts = [f"{i[2:-2]}".replace("_", "-") for i in template_parts[1:]]

    write_scope_parser_config(s, PARSER_TYPE_DATASET_ID, {
        "template": template,
        "collections": [f"{s}:{i}" for i in template_parts]
    })
