"""
This magic was taken from
https://code.activestate.com/recipes/81253-weakmethod/#c4

This module provides classes and methods for weakly referencing functions and
bound methods; it turns out this is a non-trivial problem.
"""

import weakref


class DeadFunctionError(Exception):
    pass


class WeakMethodBound:
    """
    Holds a weak reference to a bound method for an object.

    .. attribute::method

        The function being called.
    """

    def __init__(self, func):
        self.func = func.__func__
        self.weak_object_ref = weakref.ref(func.__self__)

    def _func(self):
        return self.func

    method = property(_func)

    def __call__(self, *arg):
        if self.weak_object_ref() is None:
            raise DeadFunctionError('Method called on dead object')
        return self.func(self.weak_object_ref(), *arg)


class WeakMethodFree:
    """
    Holds a weak reference to an unbound function. Included only for
    completeness.

    .. attribute::method

        The function being called.
    """

    def __init__(self, func):
        self.func = weakref.ref(func)

    def _func(self):
        return self.func()

    method = property(_func)

    def __call__(self, *arg):
        if self.func() is None:
            raise DeadFunctionError('Function no longer exist')
        return self.func()(arg)


def WeakMethod(func):
    """
    Attempts to create a weak reference to this function; only bound methods
    require a weakreference.
    """
    try:
        func.__func__
    except AttributeError:
        return func
    return WeakMethodBound(func)
