import glob
import json
import os
import shutil
from os.path import join
from os.path import isdir

from pyessv.codecs import decode
from pyessv.codecs import encode
from pyessv.constants import DIR_ARCHIVE
from pyessv.constants import DIR_CONFIG
from pyessv.constants import ENCODING_JSON
from pyessv.constants import IDENTIFIER_TYPE_SET
from pyessv.model import Authority
from pyessv.model import Collection
from pyessv.model import Scope
from pyessv.model import Term
from pyessv.model import Node
from pyessv.validation import get_errors
from pyessv.validation import is_valid


# Manifest file name.
_MANIFEST = 'MANIFEST'


def delete(target):
    """Deletes vocabulary data from file system.

    """
    if not isinstance(target, Node):
        raise TypeError()

    elif isinstance(target, Authority):
        action = shutil.rmtree
        io_path = join(DIR_ARCHIVE, target.io_name)

    elif isinstance(target, Scope):
        action = shutil.rmtree
        io_path = join(DIR_ARCHIVE, target.authority.io_name)
        io_path = join(io_path, target.io_name)

    elif isinstance(target, Collection):
        action = shutil.rmtree
        io_path = join(DIR_ARCHIVE, target.authority.io_name)
        io_path = join(io_path, target.scope.io_name)
        io_path = join(io_path, target.io_name)

    elif isinstance(target, Term):
        action = os.remove
        io_path = join(DIR_ARCHIVE, target.authority.io_name)
        io_path = join(io_path, target.scope.io_name)
        io_path = join(io_path, target.collection.io_name)
        io_path = join(io_path, target.io_name)

    try:
        action(io_path)
    except OSError:
        pass


def read(archive_dir=DIR_ARCHIVE, authority=None, scope=None):
    """Reads vocabularies from archive folder (~/.esdoc/pyessv-archive) upon file system.

    :param archive_dir: Directory hosting vocabulary archive.
    :param authority: Authority to be loaded (if unspecified then all will be loaded).
    :param scope: Scope to be loaded (if unspecified then all will be loaded).
    :returns: List of vocabulary authorities loaded from archive folder.

    """
    if authority is not None:
        return _read_authority("{}/{}".format(archive_dir, authority), scope)
    else:
        return [_read_authority(i) for i in glob.glob('{}/*'.format(archive_dir)) if isdir(i)]


def read_scope_parser_config(s, identifier_type, config_dir=DIR_CONFIG):
    """Writes an identifier parser to the file system.

    :param s: Scope associated with parser.
    :param identifier_type: Type of parser being processed.
    :param obj: Config data to be written.
    :param config_dir: Directory hosting identifier parsing configuration.

    """
    io_path = _get_path_to_scope_parser_config(s, identifier_type, config_dir)
    with open(io_path, 'r') as fstream:
        return json.loads(fstream.read())


def write(authority, archive_dir=DIR_ARCHIVE):
    """Writes authority CV data to file system.

    :param pyessv.Authority authority: Authority class instance to be written to file-system.
    :param archive_dir: Directory hosting vocabulary archive.

    """
    assert isinstance(authority, Authority), \
        'Invalid authority: unknown type'
    assert isdir(archive_dir), \
        'Invalid authority directory.'
    assert is_valid(authority), \
        'Invalid authority: {} : {}'.format(authority, get_errors(authority))

    # Set directory.
    dpath = join(archive_dir, authority.io_name)
    try:
        os.makedirs(dpath)
    except OSError:
        pass

    # Write manifest.
    with open(join(dpath, _MANIFEST), 'w') as fstream:
        fstream.write(encode(authority))

    # Write collections/terms.
    for scope in authority:
        for collection in scope:
            for term in collection:
                _write_term(dpath, term)


def write_scope_parser_config(scope, identifier_type, cfg, config_dir=DIR_CONFIG):
    """Writes an identifier parser to the file system.

    :param scope: Scope associated with parser.
    :param identifier_type: Type of parser being processed.
    :param obj: Config data to be written.
    :param config_dir: Directory hosting identifier parsing configuration.

    """
    assert identifier_type in IDENTIFIER_TYPE_SET

    # Inject meta attributes.
    cfg = {**{
        "identifier_type": identifier_type,
        "scope": scope.namespace
    }, **cfg}

    # Write to fs.
    io_path = _get_path_to_scope_parser_config(scope, identifier_type, config_dir)
    with open(io_path, 'w') as fstream:
        fstream.write(json.dumps(cfg, indent=4))


def _get_path_to_scope_parser_config(s, identifier_type, config_dir):
    """Returns path to a scope parser configuration file.

    """
    io_path = join(config_dir, s.authority.io_name)
    io_path = join(io_path, s.io_name)
    try:
        os.makedirs(io_path)
    except OSError:
        pass

    return join(io_path, "{}.json".format(identifier_type))


def _read_authority(dpath, scope_id=None):
    """Reads authority CV data from file system.

    """
    # Read authority from manifest.
    try:
        with open(join(dpath, _MANIFEST), 'r') as fstream:
            authority = decode(fstream.read(), ENCODING_JSON)
    except IOError:
        raise IOError('Invalid authority MANIFEST: {}/MANIFEST'.format(dpath))

    # Read terms.
    termcache = {}
    for scope in authority:
        if scope_id is not None and scope.canonical_name != scope_id:
            authority.scopes.remove(scope)
            continue
        for collection in scope:
            for term in _read_terms(dpath, scope, collection, termcache):
                term.collection = collection
                collection.terms.append(term)

    # Set inter-term hierarchies.
    for term in termcache.values():
        if term.parent in termcache:
            term.parent = termcache[term.parent]

    # Set intra-term hierarchies.
    for term in [i for i in termcache.values() if i.associations]:
        term.associations = [termcache[i] if i in termcache else i for i in term.associations]

    return authority


def _read_terms(dpath, scope, collection, termcache):
    """Reads terms from file system.

    """
    dpath = join(dpath, scope.io_name)
    dpath = join(dpath, collection.io_name)
    dpath = join(dpath, '*')

    return [_read_term(i, collection, termcache) for i in glob.iglob(dpath)]


def _read_term(fpath, collection, termcache):
    """Reads terms from file system.

    """
    with open(fpath, 'r') as fstream:
        term = decode(fstream.read(), ENCODING_JSON)

    term.collection = collection
    termcache[term.namespace] = term

    return term


def _write_term(dpath, term):
    """Writes a term to the file system.

    """
    # Set directory.
    dpath = join(dpath, term.scope.io_name)
    dpath = join(dpath, term.collection.io_name)
    try:
        os.makedirs(dpath)
    except OSError:
        pass

    # Set file path.
    fpath = join(dpath, term.io_name)

    # Write term JSON file.
    with open(fpath, 'w') as fstream:
        fstream.write(encode(term))
