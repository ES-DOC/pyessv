# -*- coding: utf-8 -*-

"""
.. module:: pyessv._parser.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of names to match vocabulary entities.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
from pyessv._archive import load
from pyessv._constants import PARSING_STRICTNESS_SET
from pyessv._constants import PARSING_STRICTNESS_0
from pyessv._constants import PARSING_STRICTNESS_1
from pyessv._constants import PARSING_STRICTNESS_2
from pyessv._constants import PARSING_STRICTNESS_3
from pyessv._exceptions import ParsingError
from pyessv._utils.compat import str

from pyessv._model import Collection
from pyessv._model import Term



def parse_namespace(namespace, strictness=PARSING_STRICTNESS_1):
    """Parses a namespace within a vocabulary hierachy.

    :param str namespace: Vocabulary namespace, e.g. wcrp.
    :param int strictness: Strictness level to apply when applying lookup rules.

    """
    ns = str(namespace).split(':')
    assert len(ns) >= 1 and len(ns) <= 4, 'Invalid namespace'

    ns = ns + [None for i in range(4 - len(ns))]

    return parse(ns[0], ns[1], ns[2], ns[3], strictness)


def parse(
    authority,
    scope=None,
    collection=None,
    term=None,
    strictness=PARSING_STRICTNESS_1
    ):
    """Parses a name within a vocabulary hierachy.

    :param str authority: Vocabulary authority, e.g. wcrp.
    :param str scope: Vocabulary scope, e.g. global.
    :param str collection: Vocabulary collection, e.g. institute-id.
    :param str term: Vocabulary term, e.g. ipsl.
    :param int strictness: Strictness level to apply when applying lookup rules.

    """
    assert strictness in PARSING_STRICTNESS_SET, 'Invalid parsing strictness'

    # Set parsing targets.
    targets = [
        _NodeInfo('authority', authority, strictness),
        _NodeInfo('scope', scope, strictness),
        _NodeInfo('collection', collection, strictness),
        _NodeInfo('term', term, strictness)
    ]
    targets = [i for i in targets if i.name is not None]

    # Load parsed nodes.
    for target in targets:
        namespace = [i.get_name(target) for i in targets]
        namespace = [i for i in namespace if i is not None]
        namespace = ":".join(namespace)
        node = load(namespace)
        target.set_node(node)

    return target.node.canonical_name


class _NodeInfo(object):
    """Information about a node whose name is being parsed.

    """
    def __init__(self, typekey, name, strictness):
        """Instance constructor.

        """
        self.node = None
        self.name = name
        self.strictness = strictness
        self.typekey = typekey


    def get_name(self, target):
        """Gets parsing relative name.

        """
        if self.node is not None:
            return self.node.canonical_name
        elif self == target:
            return str(self.name).strip().lower()


    def set_node(self, node):
        """Sets node returned from archive search.

        """
        if node is None:
            raise ParsingError(self.typekey, self.name)

        # if isinstance(node, Term):
        #     print node.collection.term_regex
        #     print node.raw_name, node.canonical_name, node.label

        # Confirm match based upon the level of parsing strictness perform test.
        matched = False
        if self.name == node.canonical_name:
            matched = True

        if self.strictness >= PARSING_STRICTNESS_1 and \
           self.name == node.raw_name:
            matched = True

        if self.strictness >= PARSING_STRICTNESS_2 and \
           self.name in node.synonyms:
            matched = True

        if self.strictness >= PARSING_STRICTNESS_3:
            name = str(self.name).strip().lower()
            if name in [i.lower() for i in node.all_names]:
                matched = True

        # Raise parsing error if appropriate.
        if matched == False:
            raise ParsingError(self.typekey, self.name)

        self.node = node
