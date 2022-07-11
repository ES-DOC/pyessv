import argparse

import pyessv

import set_dataset_id
import set_directory_format
import set_filename_format


_GENERATORS = {
    pyessv.PARSER_TYPE_DATASET_ID: set_dataset_id.generate,
    pyessv.PARSER_TYPE_DIRECTORY: set_directory_format.generate,
    pyessv.PARSER_TYPE_FILENAME: set_filename_format.generate,
}


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    for a in pyessv.get_cached():
        for s in [i for i in a if i.data]:
            for parser_type, template in s.data.items():
                try:
                    generator = _GENERATORS[parser_type]
                except KeyError:
                    continue
                else:
                    generator(a, s, template)

parser = argparse.ArgumentParser("Maps parsing templates -> configuration files.")

_main(parser.parse_args())
