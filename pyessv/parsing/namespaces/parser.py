from pyessv.loader import load
from pyessv.constants import PARSING_NODE_FIELDS
from pyessv.constants import PARSING_STRICTNESS_SET
from pyessv.constants import PARSING_STRICTNESS_0
from pyessv.constants import PARSING_STRICTNESS_1
from pyessv.constants import PARSING_STRICTNESS_2
from pyessv.constants import PARSING_STRICTNESS_3
from pyessv.constants import PARSING_STRICTNESS_4
from pyessv.exceptions import NamespaceParsingError
from pyessv.utils import compat


def parse_namespace(
    namespace,
    strictness=PARSING_STRICTNESS_2,
    field='canonical_name'
):
    """Parses a namespace within a vocabulary hierachy.

    :param str namespace: Vocabulary namespace, e.g. wcrp.
    :param int strictness: Strictness level to apply when applying lookup rules.
    :param str field: Term field to return.

    """
    assert strictness in PARSING_STRICTNESS_SET, 'Invalid parsing strictness'
    assert field in PARSING_NODE_FIELDS, 'Invalid field'

    # Set namespace
    ns = compat.str(namespace).strip().split(':')
    assert len(ns) >= 1 and len(ns) <= 4, 'Invalid namespace'
    ns = ns + [None for i in range(4 - len(ns))]

    # Destructure.
    authority, scope, collection, term = ns

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

    return getattr(target.node, field)


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
            return compat.str(self.name).strip().lower()

    def set_node(self, node):
        """Sets node returned from archive search.

        """
        if node is None:
            raise NamespaceParsingError(self.typekey, self.name)

        # Confirm match based upon the level of parsing strictness perform test.
        matched = False
        if self.strictness == PARSING_STRICTNESS_0:
            if self.name == node.canonical_name:
                matched = True

        elif self.strictness == PARSING_STRICTNESS_1:
            if self.name == node.raw_name:
                matched = True

        elif self.strictness == PARSING_STRICTNESS_2:
            if self.name in {node.canonical_name, node.raw_name}:
                matched = True

        elif self.strictness == PARSING_STRICTNESS_3:
            names = {node.canonical_name, node.raw_name}.union(set(node.alternative_names))
            if self.name in names:
                matched = True

        elif self.strictness == PARSING_STRICTNESS_4:
            name = compat.str(self.name).strip().lower()
            if name in [i.lower() for i in node.all_names]:
                matched = True

        # Raise parsing error if appropriate.
        if matched is False:
            raise NamespaceParsingError(self.typekey, self.name)

        self.node = node
