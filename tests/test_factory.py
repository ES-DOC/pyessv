# -*- coding: utf-8 -*-

"""
.. module:: test_authoring.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyessv authoring tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import nose
import pyessv

from pyessv._utils.compat import str
import tests.utils as tu



@nose.with_setup(None, tu.teardown)
def test_create():
    """Test creating an authority.

    """
    def _test(factory, typeof):
        """Inner test.

        """
        tu.assert_object(factory(), typeof)


    for factory, typeof in (
        (tu.create_authority, pyessv.Authority),
        (tu.create_scope, pyessv.Scope),
        (tu.create_collection, pyessv.Collection),
        (tu.create_term, pyessv.Term)
        ):
        desc = 'create --> {}'.format(str(typeof).split('.')[-1][0:-2].lower())
        tu.init(_test, desc)
        yield _test, factory, typeof



# @nose.with_setup(_setup, tu.teardown)
# def test_delete():
#     """pyessv-tests: authoring: deleting a term.

#     """
#     count = pyessv.get_count()
#     term = tu.get_term()
#     pyessv.delete(term)
#     tu.assert_int(pyessv.get_count(), count - 1)
#     term = tu.get_term()
#     tu.assert_none(term)


# def test_update():
#     """Test updating a term.

#     """
#     def _update_create_date(term):
#         """Update term create date."""
#         term.create_date = tu.get_date()

#     def _update_description(term):
#         """Update term description."""
#         term.description = tu.get_uuid()

#     def _update_domain(term):
#         """Update term domain."""
#         term.domain = tu.get_string(existing=term.domain)

#     def _update_id(term):
#         """Update term id."""
#         term.idx = tu.get_int(existing=term.idx)

#     def _update_kind(term):
#         """Update term kind."""
#         term.kind = tu.get_string(existing=term.kind)

#     def _update_name(term):
#         """Update term name."""
#         term.canonical_name = tu.get_string(existing=term.canonical_name)

#     def _update_status(term):
#         """Update term status."""
#         term.status = tu.get_string(existing=term.status)

#     def _update_subdomain(term):
#         """Update term subdomain."""
#         term.subdomain = tu.get_string(existing=term.subdomain)

#     def _update_uid(term):
#         """Update term uid."""
#         term.uid = tu.get_uuid()

#     def _assert(term):
#         """Asserts an update."""
#         count = pyessv.get_count()
#         pyessv.save(term)
#         tu.assert_int(pyessv.get_count(), count)
#         term_ = pyessv.get_term(term.domain, term.subdomain, term.kind, term.name)
#         tu.assert_terms(term, term_)

#     @nose.with_setup(_setup, tu.teardown)
#     def _test(update_callback):
#         """Performs update test."""
#         term = tu.get_term()
#         update_callback(term)
#         _assert(term)

#     for func  in (
#         _update_create_date,
#         _update_description,
#         _update_domain,
#         _update_id,
#         _update_kind,
#         _update_name,
#         _update_status,
#         _update_subdomain,
#         _update_uid
#         ):
#         tu.init(_test, 'authoring', inspect.getdoc(func))
#         yield _test, func
