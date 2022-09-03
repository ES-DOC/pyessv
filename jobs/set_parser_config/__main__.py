import pyessv

from pyessv import io_manager
from pyessv import constants
from jobs.set_parser_config import set_dataset_id
from jobs.set_parser_config import set_directory_id
from jobs.set_parser_config import set_filename_id


# Map: parser type <-> generator.
_IDENTIFIER_TYPES = {
    "dataset_id": constants.IDENTIFIER_TYPE_DATASET,
    "directory_format": constants.IDENTIFIER_TYPE_DIRECTORY,
    "filename_format": constants.IDENTIFIER_TYPE_FILENAME,
}

# Map: parser type <-> generator.
_GENERATORS = {
    constants.IDENTIFIER_TYPE_DATASET: set_dataset_id,
    constants.IDENTIFIER_TYPE_DIRECTORY: set_directory_id,
    constants.IDENTIFIER_TYPE_FILENAME: set_filename_id
}

def _main():
    """Main entry point.

    """
    for a in pyessv.get_cached():
        for s in [i for i in a if i.data]:
            for identifier_type, template in s.data.items():
                try:
                    identifier_type = _IDENTIFIER_TYPES[identifier_type]
                except KeyError:
                    continue

                try:
                    generator = _GENERATORS[identifier_type]
                except KeyError:
                    continue
                else:
                    cfg = generator.get_config(a, s, template)
                    if cfg is not None:
                        io_manager.write_scope_parser_config(s, identifier_type, cfg)

_main()
