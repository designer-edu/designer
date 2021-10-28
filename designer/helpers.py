import designer
from designer.core.event import register
from designer.core.director import Director
import pygame


def check_initialized():
    """
    Checks if global state exists and creates one if it does not.

    :return: None
    """

    if not designer.GLOBAL_DIRECTOR:
        designer.GLOBAL_DIRECTOR = Director()
        designer.GLOBAL_DIRECTOR._setup_initial_window()


def draw(*objs):
    """
    Draws Designer Objects on window.

    :param objs: objects that have been created to draw on the window
    :type objs: DesignerObjects

    :return: None
    """

    check_initialized()
    #if not objs and not designer.GLOBAL_DIRECTOR.handlers:
    #    print("WARNING: you have not passed any DesignerObjects to draw!")
    designer.GLOBAL_DIRECTOR.start()


def stop():
    """ Stops the game. """
    check_initialized()
    designer.GLOBAL_DIRECTOR.stop()


def set_window_color(color):
    """
    Changes window color to given color.
    Must call before adding any DesignerObjects.

    :param color: color to change window to
    :type color: str or List[str]

    :return: None
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.background_color = color
    designer.GLOBAL_DIRECTOR.screen.fill(color)
    designer.GLOBAL_DIRECTOR.background.fill(color)


def set_window_title(caption: str):
    """
    Set the title of the game's window (usually the title of your game).

    :param caption: The caption that will be displayed in the window.
                    Typically the name of your game.
    :type caption: ``str``
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.window_title = caption


def set_window_size(width, height):
    """
    Set size of window in pixels.
    Must call before adding any DesignerObjects.

    :param width: number of pixels to set horizontal size of window
    :type width: int
    :param height: number of pixels to set vertical size of window
    :type height: int
    :return: None
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.window_size = width, height


def get_width():
    """
    Get the width of the window.

    :return: pixels of horizontal width of window
    :rtype: int
    """
    check_initialized()
    return designer.GLOBAL_DIRECTOR.window_size[0]


def get_height():
    """
    Get the height of the window.

    :return: pixels of vertical height of window
    :rtype: int
    """

    check_initialized()
    return designer.GLOBAL_DIRECTOR.window_size[1]


def when(event: str, *funcs):
    check_initialized()
    for func in funcs:
        register(event, func)


def colliding(*args):
    # TODO: Could use collide_circle and collide_mask for improved collisions
    check_initialized()
    if len(args) == 2:
        obj1 = args[0]
        obj2 = args[1]
        return obj1.collide_other(obj2)
    elif len(args) == 3:
        if isinstance(args[0], int) and isinstance(args[1], int):
            x, y, obj = args
        elif isinstance(args[1], int) and isinstance(args[2], int):
            obj, x, y = args
        else:
            raise ValueError()
        return obj.collide_point(x, y)


def destroy(*gobjects):
    check_initialized()
    for gobject in gobjects:
        gobject.destroy()
