"""The keyboard modules provides an interface to adjust the keyboard's repeat
rate.

.. attribute:: repeat

    When the keyboard repeat is enabled, keys that are held down will keep
    generating new events over time. Defaults to `False`.

.. attribute:: delay

    `int` to control how many milliseconds before the repeats start.

.. attribute:: interval

    `int` to control how many milliseconds to wait between repeated events.

"""
import pygame


class KeyboardModule:
    DEFAULT_DELAY = 600
    DEFAULT_REPEAT = False
    DEFAULT_INTERVAL = 100

    def __init__(self):
        self._repeat = False
        self._delay = 600
        self._interval = 100

    def _update_repeat_status(self):
        if self._repeat:
            pygame.key.set_repeat(self._delay, self._interval)
        else:
            pygame.key.set_repeat()

    @property
    def repeat(self):
        return self._repeat

    @repeat.setter
    def repeat(self, value):
        self._repeat = value
        self._update_repeat_status()

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value
        self._update_repeat_status()

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value
        if value == 0:
            self._repeat = False
        self._update_repeat_status()

