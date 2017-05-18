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

import pyessv

from pyessv._constants import NODE_TYPE_AUTHORITY
from pyessv._constants import NODE_TYPE_COLLECTION
from pyessv._constants import NODE_TYPE_SCOPE
from pyessv._constants import NODE_TYPE_TERM
from pyessv._exceptions import ValidationError
from pyessv._model import NODE_TYPE_KEY_MAP
from pyessv._model import Authority
from pyessv._model import Node
from pyessv._model import Scope
from pyessv._model import Collection
from pyessv._model import Term
from pyessv._parser_template import TemplateParser
from pyessv._utils.compat import basestring
from pyessv._utils.compat import str
from pyessv._utils.formatter import format_canonical_name
from pyessv._utils.formatter import format_string
from pyessv._validation import validate_node



def create_authority(name, description, label=None, url=None, create_date=None, data=None):
    """Instantiates, initialises & returns a term authority.

    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.

    :returns: A vocabulary authority, e.g. wcrp.
    :rtype: pyessv.Authority

    """
    return _create_node(
        Authority,
        name,
        description,
        label,
        url,
        create_date,
        data
        )


def create_scope(
    authority,
    name,
    description,
    label=None,
    url=None,
    create_date=None,
    data=None
    ):
    """Instantiates, initialises & returns a term scope.

    :param pyessv.Authority authority: CV authority to which scope is bound.
    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.

    :returns: A vocabulary scope, e.g. cmip6.
    :rtype: pyessv.Scope

    """
    def _callback(instance):
        instance.authority = authority
        authority.scopes.append(instance)

    return _create_node(
        Scope,
        name,
        description,
        label,
        url,
        create_date,
        data,
        _callback
        )


def create_collection(
    scope,
    name,
    description,
    label=None,
    url=None,
    create_date=None,
    data=None,
    term_name_regex=None
    ):
    """Instantiates, initialises & returns a term collection.

    :param pyessv.Scope scope: CV scope to which collection is bound.
    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.

    :returns: A vocabulary collection, e.g. insitution-id.
    :rtype: pyessv.Collection

    """
    def _callback(instance):
        instance.scope = scope
        instance.term_name_regex = term_name_regex
        scope.collections.append(instance)

    return _create_node(
        Collection,
        name,
        description,
        label,
        url,
        create_date,
        data,
        _callback
        )


def create_term(
    collection,
    name,
    description=None,
    label=None,
    url=None,
    create_date=None,
    data=None
    ):
    """Instantiates, initialises & returns a term.

    :param pyessv.Collection collection: The collection to which the term belongs.
    :param str name: Canonical name.
    :param str description: Informative description.
    :param str label: Label for UI purposes.
    :param str url: Further information URL.
    :param datetime create_date: Creation date.
    :param dict data: Arbirtrary data.

    :returns: A vocabulary term, e.g. ipsl.
    :rtype: pyessv.Term

    """
    def _callback(instance):
        instance.collection = collection
        instance.idx = len(collection)
        instance.name_raw = format_string(name)
        collection.terms.append(instance)

    return _create_node(
        Term,
        name,
        description,
        label,
        url,
        create_date,
        data,
        callback=_callback
        )


def create_template_parser(template, collections):
    """Instantiates, initialises & returns a template parser.

    :param str template: An expression template.
    :param tuple collections: Collections that the template maps to.

    :returns: A vocabulary expression parser.
    :rtype: pyessv.TemplateParser

    """
    assert isinstance(template, basestring), 'Invalid template'
    assert isinstance(collections, tuple), 'Invalid collections'
    assert len(template) > 0, 'Invalid template'
    assert len(collections) > 0, 'Invalid collections'
    assert len([i for i in collections if not isinstance(i, Collection)]) == 0, 'Invalid collections'
    assert template.count('{}') == len(collections), 'Invalid template'

    return TemplateParser(template, collections)


def _create_node(
    typeof,
    name,
    description,
    label,
    url,
    create_date,
    data,
    callback = None
    ):
    """Instantiates, initialises & returns a node.

    """
    # Set core attributes.
    instance = typeof()
    instance.label = format_string(name)
    instance.name = format_canonical_name(name)
    instance.create_date = create_date or arrow.utcnow().datetime
    instance.data = data
    instance.uid = uuid.uuid4()

    # Set other attributes.
    if description is not None:
        instance.description = format_string(description)
    if url is not None:
        instance.url = format_string(url)

    # Set node specific attributes.
    if callback is not None:
        callback(instance)

    # Validate.
    errors = validate_node(instance)
    if errors:
        raise ValidationError(errors)

    return instance
