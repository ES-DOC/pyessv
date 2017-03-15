from pyessv._archive import load
from pyessv._exceptions import ParsingError



class _ParsingContext(object):
    def __init__(self, authority, scope, collection, term, reformat, parse_synonyms):
        self.authority = authority
        self.collection = collection
        self.reformat = reformat
        self.scope = scope
        self.term = term
        self.parse_synonyms = parse_synonyms


def parse(
    authority,
    scope=None,
    collection=None,
    term=None,
    reformat=True,
    parse_synonyms=False
    ):
    ctx = _ParsingContext(authority, scope, collection, term, reformat, parse_synonyms)

    parsers = [_parse_authority]
    if scope is not None:
        parsers.append(_parse_scope)
        if collection is not None:
            parsers.append(_parse_collection)
            if term is not None:
                parsers.append(_parse_term)

    for parser in parsers:
        if parser == parsers[-1]:
            return parser(ctx)
        parser(ctx)


def _parse_authority(ctx):
    name = _get_name(ctx.authority, ctx.reformat)
    authority = load(name)

    if authority is None:
        raise ParsingError("authority", ctx.authority)
    elif not ctx.reformat and authority.name != name:
        raise ParsingError("authority", ctx.authority)
    else:
        ctx.authority = authority.name

    return ctx.authority


def _parse_scope(ctx):
    name = _get_name(ctx.scope, ctx.reformat)
    scope = load(ctx.authority, name)

    if scope is None:
        raise ParsingError("scope", ctx.scope)
    elif not ctx.reformat and scope.name != name:
        raise ParsingError("scope", ctx.scope)
    else:
        ctx.scope = scope.name

    return ctx.scope


def _parse_collection(ctx):
    name = _get_name(ctx.collection, ctx.reformat)
    collection = load(ctx.authority, ctx.scope, name)

    if collection is None:
        raise ParsingError("collection", ctx.collection)
    elif not ctx.reformat and collection.name != name:
        raise ParsingError("collection", ctx.collection)
    else:
        ctx.collection = collection.name

    return ctx.collection


def _parse_term(ctx):
    name = _get_name(ctx.term, ctx.reformat)
    term = load(ctx.authority, ctx.scope, ctx.collection, name)

    if term is None:
        raise ParsingError("term", ctx.term)

    if term.name != ctx.term:
        if name == term.name:
            if ctx.reformat == False:
                raise ParsingError("term", ctx.term)
        elif name in term.synonyms:
            if ctx.parse_synonyms == False:
                raise ParsingError("term", ctx.term)

    if term is None:
        raise ParsingError("term", ctx.term)
    elif not ctx.reformat and term.name != name:
        raise ParsingError("term", ctx.term)
    else:
        ctx.term = term.name

    return ctx.term


def _get_name(name, reformat):
    """Returns a name formatted for lookup.

    """
    name = unicode(name)
    if reformat:
        name = name.strip().lower()

    return name


def _get_name1(name):
    """Returns a name formatted for lookup.

    """
    return unicode(name).strip().lower()
