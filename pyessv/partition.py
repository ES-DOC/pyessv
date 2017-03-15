# -*- coding: utf-8 -*-

"""
.. module:: pyessv.partitions.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of partitions being managed by client.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import inspect
import os

import pyessv
from pyessv._constants import GOVERNANCE_STATUS_ACCEPTED
from pyessv._constants import GOVERNANCE_STATUS_DEPRECATED
from pyessv._constants import GOVERNANCE_STATUS_REJECTED
from pyessv._partition_cache import PartitionCache
from pyessv._partition_io import PartitionIO



class Partition(object):
    """Encpasulates info related to a partition.

    """
    def __init__(self, domain, io_dir):
        """Instance constructor.

        """
        if len(domain.split(".")) != 2:
            raise ValueError("Partition domain is invalid.")
        if not os.path.isdir(io_dir):
            raise ValueError("Partition I/O directory is invalid")

        self.io = PartitionIO(domain, io_dir)
        self.cache = PartitionCache(self.io)
        self.domain = unicode(domain)

        # Pull in delegated functions.
        self.is_cached = self.cache.exists
        self.is_written = self.io.exists
        self.query = self.cache.query
        self.show = self.cache.show
        self.get_count = self.cache.get_count
        self.load = self.cache.init


    def create(self, kind, name):
        """Factory function that returns a newly created term.

        :param str kind: Term kind (e.g. model-componenet)
        :param str name: Term preferred name (e.g. Aerosols)

        :returns: Instantiated term.
        :rtype: pyessv.Term

        """
        new_term = pyessv.Term(self.domain, kind, name)
        new_term.idx = self.get_count(kind) + 1

        return new_term


    def save(self, target):
        """Saves a set of newly created terms to file system.

        """
        def _save(term, emit_log_entry=False):
            """Saves term to file system & updates local cache.

            """
            self.io.write(term)
            if not term.is_cached:
                self.cache.add(term, emit_log_entry)

        if isinstance(target, pyessv.Term):
            _save(target, True)
        elif inspect.isfunction(target):
            for term in target(self):
                _save(term)
        elif inspect.isgenerator(target):
            for term in target:
                _save(term)
        else:
            raise ValueError("Cannot save term data")


    def _govern(self, term, status):
        """Sets governance state of a term.

        """
        if term.status != status:
            term.status = status
            self.save(term)

        return term


    def accept(self, term):
        """Marks a term as accepted.

        :param pyessv.Term term: Term being marked as accepted.

        """
        return self._govern(term, GOVERNANCE_STATUS_ACCEPTED)


    def deprecate(self, term):
        """Marks a term as deprecated.

        :param pyessv.Term term: Term being marked as deprecated.

        """
        return self._govern(term, GOVERNANCE_STATUS_DEPRECATED)


    def destroy(self, term):
        """Removes a term from existence leaving no trace.

        :param pyessv.Term term: Term to be destroyed.

        """
        self.io.delete(term)
        self.cache.remove(term)


    def reject(self, term):
        """Marks a term as rejected.

        :param pyessv.Term term: Term being marked as rejected.

        """
        return self._govern(term, GOVERNANCE_STATUS_REJECTED)


    def parse(self, kind, name):
        """Parses a term name and returns an input Removes a term from existence leaving no trace.

        :param str kind: Term kind (e.g. model-componenet)
        :param str name: Term preferred name (e.g. Aerosols)

        """
        name = unicode(name).lower()
        for term in self.cache.query(kind):
            for term_name in term.all_names:
                if term_name.lower() == name:
                    return term.name


    def add_synonym(self, kind, name, new_synonym):
        """Appends a synonym to a term's set of synonyms.

        :param str kind: Term kind (e.g. model)
        :param str name: Term preferred name (e.g. ipsl-cm5a-lr)
        :param str new_synonym: A new synonym for the term (e.g. IPSL-LR)

        """
        term = self.cache.query(kind, name)
        if term is None:
            raise ValueError("Term could not be found: {} :: {}".format(kind, name))

        term.add_synonym(new_synonym)
