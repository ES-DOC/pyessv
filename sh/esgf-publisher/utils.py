# -*- coding: utf-8 -*-

"""
.. module:: utils.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Mapping utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import ConfigParser

import pyessv



def map_comma_delimited_options(ctx):
    """Maps comma delimited options to pyessv term attributes.

    :param object ctx: Mapping execution context information.

    :returns: Information to be mapped to a vocabulary term.
    :rtype: tuple

    """
    # Decode options from ini file.
    options = _get_ini_option(ctx)
    options = [i.strip() for i in options.split(',')]
    options = [i for i in options if len(i)]

    # Yield term information.
    for option in options:
        term_name = option.lower()
        term_label = option
        term_description = option

        yield term_name, term_label, term_description


def map_pipe_delimited_options(ctx):
    """Maps pipe delimited options to pyessv term attributes.

    :param object ctx: Mapping execution context information.

    :returns: Information to be mapped to a vocabulary term.
    :rtype: tuple

    """
    # Decode options from ini file.
    options = _get_ini_option(ctx)
    options = options.split('\n')
    options = options[1:]

    # Yield term information.
    for option in options:
        option = [i.strip() for i in option.split('|')[1:]]
        term_name = option[0]
        term_label = option[0]
        term_description = option[1]

        yield term_name, term_label, term_description


def _get_ini_option(ctx):
    """Returns an ini file option value.

    """
    try:
        return ctx.ini_section.get_option('{}_options'.format(ctx.collection_id))
    except ConfigParser.NoOptionError:
        return ctx.ini_section.get_option(ctx.collection_id)
