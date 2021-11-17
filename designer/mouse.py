"""The mouse modules provides an interface to adjust the mouse cursor.

.. attribute:: visible

    `Bool` that adjust whether the mouse cursor should be shown. This is useful
    if you want to, for example, use a Sprite instead of the regular mouse
    cursor.

.. attribute:: cursor

    `str` value that lets you choose from among the built-in options for
    cursors. The options are:

        * ``"arrow"`` : the regular arrow-shaped cursor
        * ``"diamond"`` : a diamond shaped cursor
        * ``"x"`` : a broken X, useful for indicating disabled states.
        * ``"left"``: a triangle pointing to the left
        * ``"right"``: a triangle pointing to the right

    .. warning:: Custom non-Sprite mouse cursors are currently not supported.

"""
import pygame

cursors = {"arrow": pygame.cursors.arrow,
           "diamond": pygame.cursors.diamond,
           "x": pygame.cursors.broken_x,
           "left": pygame.cursors.tri_left,
           "right": pygame.cursors.tri_right}


class MouseModule:
    def __init__(self):
        self._visible = True
        self._cursor = 'arrow'

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        if value in cursors:
            self._cursor = cursors[value]
        else:
            self._cursor = value
        pygame.mouse.set_cursor(*self._cursor)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        pygame.mouse.set_visible(value)
        self._visible = value


def get_mouse_position():
    return pygame.mouse.get_pos()

def set_mouse_position(x, y):
    pygame.mouse.set_pos((x, y))

def get_mouse_x():
    return get_mouse_position()[0]

def get_mouse_y():
    return get_mouse_position()[1]
