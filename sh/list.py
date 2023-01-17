import argparse

import pyessv


# Define command line options.
_ARGS = argparse.ArgumentParser('Writes an authority"s vocabularies to stdout.')
_ARGS.add_argument(
    '--authority',
    help='Authority to be displayed.',
    dest='authority',
    type=str
    )
_ARGS.add_argument(
    '--scope',
    help='scope to be displayed.',
    dest='scope',
    type=str,
    default=None
    )
_ARGS.add_argument(
    '--collection',
    help='Collection to be displayed.',
    dest='collection',
    type=str,
    default=None
    )
_ARGS.add_argument(
    '--term',
    help='Term to be displayed.',
    dest='term',
    type=str,
    default=None
    )


def _main(args):
    """Main entry point.

    """
    if args.authority is None or len(args.authority.strip()) == 0:
        raise ValueError('Authority is a required parameter')

    for scope in pyessv.load(args.authority):
        if args.scope and args.scope != scope.canonical_name:
            continue
        for collection in scope:
            if args.collection and args.collection != collection.canonical_name:
                continue
            for term in collection:
                if args.term and args.term != term.canonical_name:
                    continue
                print(term.namespace.replace(':', ' -> '))


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
