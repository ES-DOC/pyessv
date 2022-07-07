import json

import pyessv


_TEMPLATE_SEPERATORS = {
   "dataset_id": ".",
   "directory_format": "/",
   "filename_format": ")s_",
}


def _parse_dataset_id(a: pyessv.Authority, s: pyessv.Scope):
    template = s.data["dataset_id"]
    template_parts = template.split(".")

    if s.canonical_name != "cmip6" and s.canonical_name != template_parts[0]:
        print(f"WARN: {s} dataset_id is unmappable : {template_parts}")
        print("###########################################")
        return

    template_parts = [f"{i[2:-2]}".replace("_", "-") for i in template_parts[1:]]

    obj: dict = {
        "parser_type": pyessv.PARSER_TYPE_DATASET_ID,
        "scope": s.namespace,
        "template": template,
        "collections": [f"{s}:{i}" for i in template_parts]
    }

    print(json.dumps(obj, indent=4))
    print("###########################################")


for a in pyessv.get_cached():
    for s in a:        
        if not s.data:
            continue
        if "dataset_id" in s.data:
            _parse_dataset_id(a, s)
        
        continue


        parsers: list = []
        for parser_type, template in s.data.items():
            if parser_type != "dataset_id":
                continue

            template_parts = template.split(_TEMPLATE_SEPERATORS[parser_type])

            if s.canonical_name == "cmip6":
                template_parts = ["cmip6"] + template_parts[1:]

            if s.canonical_name != template_parts[0]:
                print(s.canonical_name, template_parts[0])
                print(template_parts)
                print("###########################################")
                continue

            obj: dict = {
                "scope": s.canonical_name,
                "template": template,
                "parser_type": parser_type,
                "collections": []
            }

            print(s, parser_type)
            print(template)
            print(template_parts)
            print("###########################################")
            parsers.append(obj)

        # print(parsers)
