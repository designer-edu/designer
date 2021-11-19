import imghdr
from typing import Optional, Union

from urllib.request import urlopen, Request
import pygame
import math
import sys
import os
import io

import designer
from designer.core.event import register, KNOWN_EVENTS
from designer.core.director import Director
from designer.core.internal_image import InternalImage
from designer.utilities.vector import Vec2D
from designer.utilities.argument_checks import make_suggestions


def check_initialized(**kwargs):
    """
    Checks if global state exists and creates one if it does not.

    :return: bool Indicates whether a new director got set up
    """

    if not designer.GLOBAL_DIRECTOR:
        designer.GLOBAL_DIRECTOR = Director(**kwargs)
        designer.GLOBAL_DIRECTOR._setup_initial_window()
        return True
    return False


def draw(*objs):
    """
    Draws Designer Objects on window.

    :param objs: objects that have been created to draw on the window
    :type objs: DesignerObjects

    :return: None
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.start(objs)


def start(*objs):
    check_initialized()
    if len(objs) == 1:
        objs = objs[0]
    else:
        objs = list(objs)
    designer.GLOBAL_DIRECTOR.start(objs)


def stop():
    """ Stops the game. """
    check_initialized()
    designer.GLOBAL_DIRECTOR.stop()


def pause():
    """ Pauses event processing in the game. """
    check_initialized()
    designer.GLOBAL_DIRECTOR.pause()


def set_window_color(color):
    """
    Changes window color to given color.
    Must call before adding any DesignerObjects.

    :param color: color to change window to
    :type color: str or List[str]

    :return: None
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.window_color = color


def get_window_color():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.window_color


def set_window_title(caption: str):
    """
    Set the title of the game's window (usually the title of your game).

    :param caption: The caption that will be displayed in the window.
                    Typically the name of your game.
    :type caption: ``str``
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.window_title = caption


def get_window_title() -> str:
    check_initialized()
    return designer.GLOBAL_DIRECTOR.window_title


def set_game_state(new_state):
    check_initialized()
    designer.GLOBAL_DIRECTOR._game_state = new_state


def set_world_state(new_state):
    set_game_state(new_state)


def set_window_state(new_state):
    set_game_state(new_state)


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
    if not check_initialized(width=width, height=height):
        designer.GLOBAL_DIRECTOR.screen = pygame.display.set_mode(size=(width, height))
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


def get_mouse_cursor():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.mouse.cursor


def set_mouse_cursor(value):
    check_initialized()
    designer.GLOBAL_DIRECTOR.mouse.cursor = value


def get_mouse_visible():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.mouse.visible


def set_mouse_visible(value):
    check_initialized()
    designer.GLOBAL_DIRECTOR.mouse.visible = value


def get_keyboard_delay():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.keyboard.delay


def set_keyboard_delay(value):
    check_initialized()
    designer.GLOBAL_DIRECTOR.keyboard.delay = value


def get_keyboard_interval():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.keyboard.interval


def set_keyboard_interval(value):
    check_initialized()
    designer.GLOBAL_DIRECTOR.keyboard.interval = value


def get_keyboard_repeat():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.keyboard.repeat


def set_keyboard_repeat(value):
    check_initialized()
    designer.GLOBAL_DIRECTOR.keyboard.repeat = value


def enable_keyboard_repeating():
    check_initialized()
    designer.GLOBAL_DIRECTOR.keyboard.repeat = True
    designer.GLOBAL_DIRECTOR.keyboard.delay = 1


def disable_keyboard_repeating():
    check_initialized()
    designer.GLOBAL_DIRECTOR.keyboard.repeat = designer.GLOBAL_DIRECTOR.keyboard.DEFAULT_REPEAT
    designer.GLOBAL_DIRECTOR.keyboard.delay = designer.GLOBAL_DIRECTOR.keyboard.DEFAULT_DELAY


def background_music(filename, volume=1.0, loop=True):
    check_initialized()
    designer.GLOBAL_DIRECTOR.music.filename = filename
    designer.GLOBAL_DIRECTOR.music.play(loop=-1 if loop is True else loop)
    designer.GLOBAL_DIRECTOR.music.volume = volume


def play_music(filename, volume=1.0, loop=True):
    return background_music(filename, volume, loop)


def pause_music():
    check_initialized()
    designer.GLOBAL_DIRECTOR.music.pause()


def set_music_volume(volume):
    check_initialized()
    designer.GLOBAL_DIRECTOR.music.volume = volume


def is_music_playing():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.music.playing


def get_music_volume():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.music.volume


def play_sound(path, volume=1.0):
    check_initialized()
    designer.GLOBAL_DIRECTOR.sfx.play(path, volume)


def stop_music():
    check_initialized()
    designer.GLOBAL_DIRECTOR.music.stop()


def rewind_music():
    check_initialized()
    designer.GLOBAL_DIRECTOR.music.rewind()


def continue_music():
    check_initialized()
    designer.GLOBAL_DIRECTOR.music.unpause()


def set_music_position(time):
    check_initialized()
    designer.GLOBAL_DIRECTOR.music.set_time_position(time)


def get_music_position():
    check_initialized()
    return designer.GLOBAL_DIRECTOR.music.get_time_position()


def when(event: Union[str, callable], *funcs):
    check_initialized()
    if callable(event):
        event_function = event
        event = 'updating'

        def _dynamic_event(func):
            def _inner_dynamic_event(event, world):
                if event_function(world):
                    window = designer.GLOBAL_DIRECTOR.current_window
                    window._send_event_to_handler(event, 'updating', func, None, None, None, None)

            return _inner_dynamic_event

        funcs = [_dynamic_event(f) for f in funcs]
    if event not in KNOWN_EVENTS and not any(e.startswith(event) for e in KNOWN_EVENTS):
        suggestions = make_suggestions(event, KNOWN_EVENTS)
        if suggestions:
            raise ValueError(f"Unrecognized event {event!r}. Perhaps you meant one of: {suggestions}")
        else:
            raise ValueError(
                f"Unrecognized event {event!r}. Check the documentation to see possible events (like 'updating' and 'starting').")
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
        if isinstance(args[0], (int, float)) and isinstance(args[1], (int, float)):
            x, y, obj = args
        elif isinstance(args[1], (int, float)) and isinstance(args[2], (int, float)):
            obj, x, y = args
        else:
            raise ValueError(f"Could not recognize the type of the arguments: {args!r}")
        return obj.collide_point(Vec2D(x, y))


def destroy(*gobjects):
    check_initialized()
    for gobject in gobjects:
        gobject.destroy()


# TODO: Fix to centralize
_USER_AGENT = "Designer Game Library for Python"


def background_image(path):
    check_initialized()
    try:
        path_strs = path.split('/')
        fixed_paths = os.path.join(*path_strs)
        if os.path.exists(fixed_paths):
            designer.GLOBAL_DIRECTOR.current_window.background = InternalImage(fixed_paths)
        else:
            raise FileNotFoundError(fixed_paths)
    except FileNotFoundError as err:
        try:
            req = Request(path, headers={'User-Agent': _USER_AGENT})
            with urlopen(req) as opened_image:
                image_str = opened_image.read()
                image_file = io.BytesIO(image_str)
                designer.GLOBAL_DIRECTOR.current_window.background = InternalImage(filename=path, fileobj=image_file)
        except:
            print(f"Unexpected error while loading background image: {path}\n", sys.exc_info()[0])
            raise


def get_director():
    check_initialized()
    return designer.GLOBAL_DIRECTOR
