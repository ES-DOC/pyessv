# -*- coding: utf-8 -*-

"""
.. module:: pyessv._model.term.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A vocabulary term, e.g. IPSL.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv
from pyessv._model.entity import Entity



class Term(Entity):
    """A vocabulary term.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(Term, self).__init__(pyessv.ENTITY_TYPE_TERM)

        self.alternative_name = None    # primary synonym
        self.alternative_url = None     # an alternative URL
        self.associations = list()      # associated terms
        self.collection = None          # collection of which term is a member
        self.idx = None                 # collection ordinal
        self.parent = None              # parent term within collection
        self.status = pyessv.GOVERNANCE_STATUS_PENDING
        self.synonyms = list()          # name synonyms


    def __contains__(self, key):
        """Instance membership predicate.

        """
        key = unicode(key).strip().lower()

        return key in self.all_names


    @property
    def owner(self):
        """Gets owner within vocabulary model.

        """
        return self.collection


    @property
    def authority(self):
        """Gets associated governing authority.

        """
        return self.scope.authority


    @property
    def scope(self):
        """Gets associated scope.

        """
        return self.collection.scope


    @property
    def all_names(self):
        """Returns all term names.

        """
        result = [self.name, self.alternative_name] + self.synonyms
        result = [t for t in result if t is not None and len(t) > 0]

        return set(sorted(result))


    @property
    def depth(self):
        """Gets hierarchical depth.

        """
        return len(self.ancestors)


    @property
    def ancestors(self):
        """Gets ancestral hierarchy.

        """
        result = []
        ancestor = self.parent
        while ancestor:
            result.append(ancestor)
            ancestor = ancestor.parent
        result.reverse()

        return result


    def add_synonym(self, new_synonym):
        """Adds a new synonym to the term's synnym set.

        """
        # Validate new synonym.
        _validate_term_synonym(new_synonym)

        # Format.
        new_synonym = unicode(new_synonym).strip()

        # Escape if already aliased.
        for synonym in self.synonyms:
            if synonym == new_synonym:
                return

        # Update synonym set.
        self.synonyms = sorted(self.synonyms + [new_synonym])

        # Save term.
        # self.partition.save(self)


    def accept(self):
        """Marks as accepted.

        """
        self.partition.accept(self)


    def reject(self):
        """Marks as rejected.

        """
        self.partition.reject(self)


    def save(self):
        """Saves term to persistant state stores.

        """
        self.partition.save(self)


    def deprecate(self):
        """Marks as deprecated.

        """
        self.partition.deprecate(self)


    def destroy(self):
        """Destroys term from all persistant state stores.

        """
        self.partition.destroy(self)


    def associate(self, term):
        """Appends an associated term to managed collection.

        :param pyessv.Term term: Associated term to be added.

        """
        self.associations.add(term)
