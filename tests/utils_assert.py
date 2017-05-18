# -*- coding: utf-8 -*-

"""
.. module:: test_utils_assert.py

   :copyright: @2013 Earth System Documentation (https://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Exposes test assertion utility functions.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import datetime
import inspect
import os

from pyessv._utils.compat import str



# Integer assertion constants.
COMPARE_EXACT = 'EXACT'
COMPARE_GT = 'GT'
COMPARE_GTE = 'GTE'
COMPARE_LTE = 'LTE'
COMPARE_LT = 'LT'
COMPARE_TYPES = (
    COMPARE_EXACT,
    COMPARE_GT,
    COMPARE_GTE,
    COMPARE_LT,
    COMPARE_LTE
)


def assert_iter(collection,
                length=-1,
                item_type=None,
                length_compare=COMPARE_EXACT):
    """Asserts an object collection.

    :param list collection: An object collection.
    :param int length: Collection size.
    :param str length: Collection size comparason operator.
    :param class item_type: Type that each collection item should sub-class.

    """
    assert_object(collection)
    assert iter(collection) is not None
    if length != -1:
        assert_int(len(collection), length, length_compare)
    if item_type is not None:
        if isinstance(collection, dict):
            collection = collection.values()
        for instance in collection:
            assert_object(instance, item_type)


def assert_in_collection(collection, item_attr, items):
    """Asserts an item is within a collection.

    :param sequence collection: A collection.
    :param str item_attr: Attribute name upon from which to derive assertion collection.
    :param object items: Set of items to assert whether found in collection.

    """
    try:
        iter(items)
    except TypeError:
        items = {items}
    targets = None
    if item_attr is not None:
        targets = [getattr(i, item_attr) for i in collection]
    else:
        targets = collection
    for item in items:
        assert item in targets, item


def assert_has_member(mod, member):
    """Asserts that a module exposes a member.

    :param module mod: Module that should expose the passed member.
    :param str member: Name of a function, exception, class ..etc.

    """
    assert inspect.ismodule(mod)
    assert hasattr(mod, member), 'Missing member: {}'.format(member)


def assert_has_class(mod, cls):
    """Asserts that a container exposes a class.

    :param module mod: Container module that should expose the passed class.
    :param str cls: Name of a class.

    """
    assert_has_member(mod, cls)
    assert inspect.isclass(getattr(mod, cls)), \
           '{} is not a class'.format(cls)


def assert_has_constant(mod, constant):
    """Asserts that a container exposes a constant.

    :param module mod: Container module that should expose the passed constant.
    :param str constant: Name of a constant.

    """
    assert_has_member(mod, constant)


def assert_has_function(mod, func):
    """Asserts that a container exposes a function.

    :param module mod: Container module that should expose the passed function.
    :param str func: Name of a function.

    """
    assert_has_member(mod, func)
    assert inspect.isfunction(getattr(mod, func)), \
           '{} is not a function'.format(func)


def assert_has_exception(mod, err):
    """Asserts that a container exposes an exception.

    :param module mod: Container module that should expose an exception class.
    :param str err: Name of an exception class.

    """
    assert_has_class(mod, err)
    assert issubclass(getattr(mod, err), Exception), \
           'Exception type does not inherit from builtin Exception class.'


def assert_none(instance):
    """Asserts an instance is none.

    :param object instance: An object for testing.

    """
    assert instance is None, \
           'Instance null mismatch : actual = {0} - {1} :: expected = None'.format(type(instance), instance)


def assert_object(instance, instance_type=None):
    """Asserts an object instance.

    :param object instance: An object for testing.
    :param class instance_type: Type that object must either be or sub-class from.

    """
    assert instance is not None, 'Instance is none'
    if instance_type is not None:
        assert isinstance(instance, instance_type), \
               'Instance type mismatch : actual = {0} :: expected = {1}'.format(type(instance), instance_type)


def assert_objects(instance1, instance2, instance_type=None):
    """Asserts that 2 object instances are equal.

    :param object instance1: An object for testing.
    :param object instance2: An object for testing.

    """
    assert_object(instance1, instance_type)
    assert_object(instance2, instance_type)
    assert instance1 == instance2, 'Instances are not equal'


def assert_bool(actual, expected):
    """Asserts a boolean.

    :param str actual: Actual boolean value.
    :param str expected: Expected boolean value.

    """
    assert bool(actual) == bool(expected)


def assert_str(actual, expected, startswith=False):
    """Asserts a string.

    :param str actual: Actual string value.
    :param str expected: Expected string value.

    :param startswith: Flag indicating whether to perform startswith test.
    :type startswith: bool

    """
    # Format.
    actual = str(actual).strip()
    expected = str(expected).strip()

    # Assert.
    if startswith == False:
        assert actual == expected, \
               'String mismatch : actual = {0} :: expected = {1}'.format(actual, expected)
    else:
        assert actual.startswith(expected) == True, \
               'String startswith mismatch : actual = {0} :: expected = {1}'.format(actual, expected)


def assert_string(actual, expected):
    """Asserts a string.

    :param str actual: Actual string value.
    :param str expected: Expected string value.

    """
    assert_object(actual, str)
    assert_object(expected, str)
    assert actual == expected, \
           'Unicode mismatch : actual = {0} :: expected = {1}'.format(actual, expected)


def assert_date(actual, expected):
    """Asserts a datetime.

    :param str actual: Actual date value.
    :param str expected: Expected date value.

    """
    if not isinstance(actual, datetime.datetime):
        actual = get_date(actual)
    if not isinstance(expected, datetime.datetime):
        expected = get_date(expected)

    assert actual == expected, \
           'Date mismatch : actual = {0} :: expected = {1}'.format(actual, expected)


def assert_float(actual, expected):
    """Asserts a float.

    :param float actual: Actual float value.
    :param float expected: Expected float value.

    """
    assert_object(actual, float)
    assert_object(expected, float)
    assert actual == expected, \
           'Float mismatch : actual = {0} :: expected = {1}'.format(actual, expected)


def assert_path(actual):
    """Asserts a filepath.

    :param str actual: Actual file path.

    """
    assert_bool(os.path.exists(actual), True)


def assert_int(actual, expected, assert_type=COMPARE_EXACT, msg=None):
    """Asserts an integer.

    :param str actual: Actual integer value.
    :param str expected: Expected integer value.

    """
    # Parse actual value.
    # ... convert string
    if type(actual) == str:
        actual = int(actual)
    # ... collection length checks
    else:
        try:
            iter(actual)
        except TypeError:
            pass
        else:
            actual = len(actual)

    if assert_type == COMPARE_EXACT:
        assert expected == actual, \
               '{} != {} {}'.format(actual, expected, msg)
    elif assert_type == COMPARE_GT:
        assert expected > actual, \
               '{} !> {} {}'.format(actual, expected, msg)
    elif assert_type == COMPARE_GTE:
        assert expected >= actual, \
               '{} !>= {} {}'.format(actual, expected, msg)
    elif assert_type == COMPARE_LT:
        assert expected < actual, \
               '{} !< {} {}'.format(actual, expected, msg)
    elif assert_type == COMPARE_LTE:
        assert expected <= actual, \
               '{} !<= {} {}'.format(actual, expected, msg)
    else:
        assert expected == actual, \
               '{} != {} {}'.format(actual, expected, msg)


def assert_int_negative(actual, expected):
    """Negatively asserts an integer.

    :param str actual: Actual integer value.
    :param str expected: Expected integer value.

    """
    assert actual != expected


def assert_uuid(actual, expected):
    """Asserts a uuid.

    :param str actual: Actual uuid value.
    :param str expected: Expected uuid value.

    """
    if isinstance(actual, uuid.UUID) == False:
        actual = uuid.UUID(actual)
    if isinstance(expected, uuid.UUID) == False:
        expected = uuid.UUID(expected)

    assert actual == expected, '{0} != {1}'.format(actual, expected)
