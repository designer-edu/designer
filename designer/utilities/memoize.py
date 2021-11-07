"""This module contains classes to handle memoization, a time-saving method that
caches previously seen results from function calls."""


class Memoize:
    """
    This is a decorator to allow memoization of function calls. It is a
    completely dumb cache, and will cache anything given to it indefinitely.

    :param object func: Any function (although any object will work).
    .. warning:: This may be deprecated.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        """
        Attempts to return the results of this function call from the cache;
        if it can't find it, then it will execute the function and add it to the
        cache.
        """
        try:
            return self.cache[args]
        except KeyError:
            res = self.func(*args)
            self.cache[args] = res
            return res
        except TypeError:
            print("WARNING: Unhashable type passed to memoize."
                  "Reconsider using this decorator.")
            return self.func(*args)


class SmartMemoize:
    """
    This is a decorator to allow memoization of function calls. Its cache
    is cleared on scene changes, and also clears items from the cache which
    haven't been used in at least 250 frames.

    :param object func: Any function (although any object will work).
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.window = None
        self.last_clear = 0

    def __call__(self, *args):
        """
        Attempts to return the results of this function call from the cache;
        if it can't find it, then it will execute the function and add it to the
        cache.
        """
        from designer import GLOBAL_DIRECTOR
        frame = GLOBAL_DIRECTOR.tick
        if GLOBAL_DIRECTOR.current_window is not self.window:
            self.window = GLOBAL_DIRECTOR.current_window
            self.cache = {}
        if frame - self.last_clear > 100:
            for key, value in list(self.cache.items()):
                data, oldframe = value
                if frame - oldframe > 250:
                    self.cache.pop(key)
            self.last_clear = frame
        try:
            data, oldframe = self.cache[args]
            self.cache[args] = (data, frame)
            return data
        except KeyError:
            res = self.func(*args)
            self.cache[args] = (res, frame)
            return res
        except TypeError as e:
            print("WARNING: Unhashable type passed to SmartMemoize."
                  "Reconsider using this decorator", e, hash(args))
            return self.func(*args)


class _ImageMemoize(SmartMemoize):
    """
    A subclass of SmartMemoize that is built explicitly for image related calls.
    It allows images to be cleared from its cache when they are updated.
    """

    def clear(self, clear_image):
        """
        Removes the given image from the cache.
        :param clear_image: The image to remove.
        :type clear_image: :class:`InternalImage <designer.core.internal_image.InternalImage>`
        """
        self.cache = dict(((image, scale) for (image, scale)
                           in self.cache.items()
                           if image is clear_image))
