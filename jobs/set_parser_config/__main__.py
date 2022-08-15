import pyessv

from pyessv import io_manager
import set_dataset_id
import set_directory_format
import set_filename_format


# Map: parser type <-> generator.
_GENERATORS = {
    pyessv.IDENTIFIER_TYPE_DATASET_ID: set_dataset_id,
    pyessv.IDENTIFIER_TYPE_DIRECTORY: set_directory_format,
    pyessv.IDENTIFIER_TYPE_FILENAME: set_filename_format,
}


def _main():
    """Main entry point.

    """
    for authority in pyessv.get_cached():
        for scope in [i for i in authority if i.data]:
            for identifier_type, template in scope.data.items():
                try:
                    generator = _GENERATORS[identifier_type]
                except KeyError:
                    continue
                else:
                    cfg = generator.get_config(authority, scope, template)
                    if cfg is not None:
                        io_manager.write_scope_parser_config(scope, identifier_type, cfg)


_main()
