# -*- coding: utf-8 -*-

"""
.. module:: pyessv._factory.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates creation of domain model class instances.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import uuid

import arrow

from pyessv._constants import REGEX_CANONICAL_NAME
from pyessv._constants import PARSING_STRICTNESS_2
from pyessv._constants import PARSING_STRICTNESS_SET
from pyessv._cache import cache
from pyessv._exceptions import ValidationError
from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Node
from pyessv._model import Scope
from pyessv._model import Term
from pyessv._parser_template import TemplateParser
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
from pyessv._utils.formatter import format_canonical_name
from pyessv._utils.formatter import format_string
from pyessv._validation import validate



def create_authority(
    name,
    description,
    label=None,
    url=None,
    create_date=None,
    data=None,
    alternative_names=[]
    ):
    """Instantiates, initialises & returns a term authority.

    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.
    :param list alternative_names: Collection of associated alternative names.

    :returns: A vocabulary authority, e.g. wcrp.
    :rtype: pyessv.Authority

    """
    return _create_node(
        typeof=Authority,
        raw_name=name,
        description=description,
        label=label,
        url=url,
        create_date=create_date,
        alternative_names=alternative_names,
        data=data
        )


def create_scope(
    authority,
    name,
    description,
    label=None,
    url=None,
    create_date=None,
    data=None,
    alternative_names=[]
    ):
    """Instantiates, initialises & returns a term scope.

    :param pyessv.Authority authority: CV authority to which scope is bound.
    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.
    :param list alternative_names: Collection of associated alternative names.

    :returns: A vocabulary scope, e.g. cmip6.
    :rtype: pyessv.Scope

    """
    def _callback(instance):
        instance.authority = authority
        authority.scopes.append(instance)

    return _create_node(
        typeof=Scope,
        raw_name=name,
        description=description,
        label=label,
        url=url,
        create_date=create_date or authority.create_date,
        alternative_names=alternative_names,
        data=data,
        callback=_callback
        )


def create_collection(
    scope,
    name,
    description,
    label=None,
    url=None,
    create_date=None,
    data=None,
    alternative_names=[],
    term_regex=None
    ):
    """Instantiates, initialises & returns a regular expression term collection.

    :param pyessv.Scope scope: CV scope to which collection is bound.
    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.
    :param list alternative_names: Collection of associated alternative names.
    :param str|tuple term_regex: Regular expression information to be applied to terms.

    :returns: A vocabulary collection, e.g. insitution-id.
    :rtype: pyessv.Collection

    """
    if term_regex is None:
        term_regex = REGEX_CANONICAL_NAME

    def _callback(instance):
        instance.scope = scope
        instance.term_regex = term_regex
        scope.collections.append(instance)

    return _create_node(
        typeof=Collection,
        raw_name=name,
        description=description,
        label=label,
        url=url,
        create_date=create_date or scope.create_date,
        alternative_names=alternative_names,
        data=data,
        callback=_callback
        )

def create_term(
    collection,
    name,
    description=None,
    label=None,
    url=None,
    create_date=None,
    data=None,
    alternative_names=[]
    ):
    """Instantiates, initialises & returns a term.

    :param pyessv.Collection collection: The collection to which the term belongs.
    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.
    :param list alternative_names: Collection of associated alternative names.

    :returns: A vocabulary term, e.g. ipsl.
    :rtype: pyessv.Term

    """
    def _callback(instance):
        instance.collection = collection
        collection.terms.append(instance)

    return _create_node(
        typeof=Term,
        raw_name=name,
        description=description,
        label=label,
        url=url,
        create_date=create_date or collection.create_date,
        alternative_names=alternative_names,
        data=data,
        callback=_callback
        )


def create_template_parser(template, collections, strictness=PARSING_STRICTNESS_2, seperator='.'):
    """Instantiates, initialises & returns a template parser.

    :param str template: An expression template.
    :param tuple collections: Collections that the template maps to.
    :param int strictness: Strictness level to apply when applying name matching rules.
    :param str seprarator: Seperator to apply when parsing.

    :returns: A vocabulary expression parser.
    :rtype: pyessv.TemplateParser

    """
    assert isinstance(template, basestring), 'Invalid template'
    assert isinstance(collections, tuple), 'Invalid collections'
    assert len(template) > 0, 'Invalid template'
    assert template.count('{}') > 0, 'Invalid template'
    assert len(collections) > 0, 'Invalid collections'
    assert template.count('{}') == len(collections), 'Invalid template: collection count mismatch'
    assert strictness in PARSING_STRICTNESS_SET, 'Invalid parsing strictness: {}'.format(strictness)
    assert isinstance(seperator, basestring), 'Invalid seperator'

    return TemplateParser(template, collections, strictness, seperator)


def _create_node(
    typeof,
    raw_name,
    description,
    label,
    url,
    create_date,
    alternative_names,
    data,
    callback = None
    ):
    """Instantiates, initialises & returns a node.

    """
    # Set core attributes.
    node = typeof()
    node.alternative_names = alternative_names
    node.canonical_name = format_canonical_name(raw_name)
    node.create_date = create_date or arrow.utcnow().datetime
    node.data = data
    node.label = label or format_string(raw_name)
    node.raw_name = format_string(raw_name)
    node.uid = uuid.uuid4()

    # Set other attributes.
    if description is not None:
        node.description = format_string(description)
    if url is not None:
        node.url = format_string(url)

    # Invoke node specific callback.
    if callback is not None:
        callback(node)

    # Validate.
    errors = validate(node)
    if errors:
        raise ValidationError(errors)

    # Cache.
    cache(node)

    return node
