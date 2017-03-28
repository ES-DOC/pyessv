# -*- coding: utf-8 -*-

"""
.. module:: json.encoder.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encodes a term to JSON.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyessv._codecs.dictionary import encoder as dict_encoder
from pyessv._utils import convert



def encode(instance):
    """Encodes an instance of a domain model class as a JSON text blob.

    :param pyessv.Entity instance: A domain model class instance to be encoded as a JSON text blob.

    :returns: Instance encoded as a JSON text blob.
    :rtype: str

    """
    # Convert to dictionary.
    as_dict = dict_encoder.encode(instance)

    # Return JSON.
    return convert.dict_to_json(as_dict)
