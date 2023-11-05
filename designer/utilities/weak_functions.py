"""
https://docs.python.org/3/library/weakref.html
"""

try:
    from weakref import WeakMethod, ref

    NO_WEAK_METHODS = False
except ImportError:
    NO_WEAK_METHODS = True


if NO_WEAK_METHODS:
    def weak_function(func):
        return func

else:
    def weak_function(func):
        if hasattr(func, '__self__'):
            return WeakMethod(func)
        return ref(func)
