import collections
import datetime as dt
import sys

# Syntax sugar.
_ver = sys.version_info

# Is Python 2.x?
is_py2 = (_ver[0] == 2)

# Is Python 3.x?
is_py3 = (_ver[0] == 3)

# JSON.
try:
    import simplejson as json
except (ImportError, SyntaxError):
    # simplejson does not support Python 3.2, it throws a SyntaxError
    # because of u'...' Unicode literals.
    import json


# ------------------------------------------------------
# Python 2
# ------------------------------------------------------
if is_py2:
    from ConfigParser import ConfigParser
    from ConfigParser import NoOptionError
    from urllib import \
        quote, unquote, quote_plus, unquote_plus, urlencode, getproxies, proxy_bypass
    from urlparse import urlparse, urlunparse, urljoin, urlsplit, urldefrag
    from urllib2 import parse_http_list
    import cookielib
    from Cookie import Morsel
    from StringIO import StringIO
    import compat2_datetime

    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring
    numeric_types = (int, long, float)
    integer_types = (int, long)
    to_datetime = \
        lambda i: i if isinstance(i, dt.datetime) else \
        compat2_datetime.parse_datetime(i)

    Mapping = collections.Mapping
    Iterable = collections.Iterable

# ------------------------------------------------------
# Python 3
# ------------------------------------------------------
elif is_py3:
    from configparser import ConfigParser
    from configparser import NoOptionError
    from urllib.parse import urlparse, urlunparse, urljoin, urlsplit, urlencode, quote, unquote, quote_plus, unquote_plus, urldefrag
    from urllib.request import parse_http_list, getproxies, proxy_bypass
    from http import cookiejar as cookielib
    from http.cookies import Morsel
    from io import StringIO

    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)
    integer_types = (int,)
    to_datetime = lambda i: i if isinstance(i, dt.datetime) else dt.datetime.fromisoformat(i)

    try:
        Mapping = collections.abc.Mapping
    except AttributeError:
        Mapping = collections.Mapping

    try:
        Iterable = collections.abc.Iterable
    except AttributeError:
        Iterable = collections.Iterable
