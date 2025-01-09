try:
    from weakref import ref
except ImportError:
    ref = lambda *x: x[0]

try:
    from collections.abc import MutableMapping
    NO_REFS = False
except AttributeError:
    NO_REFS = True
    MutableMapping = dict


class MultiWeakKeyDict(MutableMapping):
    """
    https://stackoverflow.com/a/74270121/1718155
    A dictionary that uses weak references to keys, and can have multiple keys
    """
    def __init__(self, initial_data=None):
        self.data = {}
        self.helpers = {}

        if initial_data is not None:
            for key, value in initial_data.items():
                self[key] = value

    def _remove(self, wref):
        for data_key in self.helpers.pop(wref, ()):
            try:
                del self.data[data_key]
            except KeyError:
                pass

    def _build_key(self, keys):
        if isinstance(keys, tuple):
            return tuple(ref(item, self._remove) if not isinstance(item, str) else item
                         for item in keys)
        else:
            return (ref(keys, self._remove) if not isinstance(keys, str) else keys
                    ,)

    def __setitem__(self, keys, value):
        weakrefs = self._build_key(keys)
        for item in weakrefs:
            self.helpers.setdefault(item, set()).add(weakrefs)
        self.data[weakrefs] = value

    def __getitem__(self, keys):
        return self.data[self._build_key(keys)]

    def __delitem__(self, keys):
        del self.data[self._build_key(keys)]

    def __iter__(self):
        for key in self.data:
            yield tuple(item if isinstance(item, str) else item()
                        for item in key)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join('{!r}:{!r}'.format(k, v) for k, v in self.items())})"


if NO_REFS:
    MultiWeakKeyDict = lambda *args: args[0]
