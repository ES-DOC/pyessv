import datetime
import uuid

from pyessv._constants import GOVERNANCE_STATUS_SET
from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._constants import REGEX_LABEL
from pyessv._constants import REGEX_URL
from pyessv._model.authority import Authority
from pyessv._model.collection import Collection
from pyessv._model.scope import Scope
from pyessv._model.term import Term


# Set of supported types.
TYPES = (
    Authority,
    Collection,
    Scope,
    Term,
)

# Map of types to tuples containing validation info.
TYPE_INFO = {
    Authority: {
        ("description", unicode, "1.1"),
        ("label", unicode, "0.1", REGEX_LABEL),
        ("name", unicode, "1.1", REGEX_CANONICAL_NAME),
        ("scopes", Scope, "0.N"),
        ("url", unicode, "1.1", REGEX_URL),
    },
    Collection: {
        ("create_date", datetime.datetime, "1.1"),
        ("description", unicode, "1.1"),
        ("idx", int, "1.1"),
        ("label", unicode, "0.1", REGEX_CANONICAL_NAME),
        ("name", unicode, "1.1", REGEX_CANONICAL_NAME),
        ("scope", Scope, "1.1"),
        ("terms", Term, "0.N"),
        ("uid", uuid.UUID, "1.1"),
        ("url", unicode, "0.1", REGEX_URL),
    },
    Scope: {
        ("authority", Authority, "1.1"),
        ("collections", Collection, "0.N"),
        ("description", unicode, "0.1"),
        ("idx", int, "1.1"),
        ("label", unicode, "1.1", REGEX_LABEL),
        ("name", unicode, "1.1", REGEX_CANONICAL_NAME),
        ("uid", uuid.UUID, "1.1"),
        ("url", unicode, "1.1", REGEX_URL),
    },
    Term: {
        ("alternative_name", unicode, "0.1", REGEX_CANONICAL_NAME),
        ("alternative_url", unicode, "0.1", REGEX_URL),
        ("collection", Collection, "1.1"),
        ("create_date", datetime.datetime, "1.1"),
        ("description", unicode, "0.1"),
        ("idx", int, "1.1"),
        ("label", unicode, "1.1"),
        ("name", unicode, "1.1", REGEX_CANONICAL_NAME),
        ("parent", Term, "0.1"),
        ("status", unicode, "1.1", tuple(GOVERNANCE_STATUS_SET)),
        ("synonyms", unicode, "0.N", REGEX_CANONICAL_NAME),
        ("uid", uuid.UUID, "1.1"),
        ("url", unicode, "0.1", REGEX_URL),
    }
}
