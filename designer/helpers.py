from typing import Union

from urllib.request import urlopen, Request
import pygame
import sys
import os
import io

import designer
from designer.mouse import get_mouse_position
from designer.core.event import register, KNOWN_EVENTS
from designer.core.director import Director
from designer.core.internal_image import InternalImage
from designer.utilities.vector import Vec2D
from designer.utilities.argument_checks import make_suggestions
from designer.system import running_on_skulpt
from designer.utilities.weak_functions import weak_function

try:
    import imghdr

    ALT_MODE = False
except:
    FileNotFoundError = Exception
    ALT_MODE = True


def check_initialized(**kwargs):
    """
    Checks if global state exists and creates one if it does not.

    :return: bool Indicates whether a new director got set up
    """

    if not designer.GLOBAL_DIRECTOR:
        designer.GLOBAL_DIRECTOR = Director(**kwargs)
        designer.GLOBAL_DIRECTOR._setup_initial_scene()
        return True
    return False


def draw(*objs):
    """
    Draws Designer Objects on scene.

    :param objs: objects that have been created to draw on the scene
    :type objs: DesignerObjects

    :return: None
    """
    check_initialized()
    if len(objs) == 1:
        objs = objs[0]
    else:
        objs = list(objs)
    designer.GLOBAL_DIRECTOR.start(objs, running_on_skulpt())


def set_first_scene(scene: str):
    check_initialized()
    if scene is not None:
        designer.GLOBAL_DIRECTOR._first_scene = scene


def start(*objs, scene=None):
    check_initialized()
    if len(objs) == 1:
        objs = objs[0]
    else:
        objs = list(objs)
    if scene is not None:
        designer.GLOBAL_DIRECTOR._first_scene = scene
    designer.GLOBAL_DIRECTOR.start(objs)


def debug(*objs, scene=None):
    check_initialized()
    if len(objs) == 1:
        objs = objs[0]
    else:
        objs = list(objs)
    if scene is not None:
        designer.GLOBAL_DIRECTOR._first_scene = scene
    designer.GLOBAL_DIRECTOR.debug(objs)


def stop():
    """ Stops the game. """
    check_initialized()
    designer.GLOBAL_DIRECTOR.stop()


def pause():
    """ Pauses event processing in the game. """
    check_initialized()
    designer.GLOBAL_DIRECTOR.pause()


def restart():
    check_initialized()
    designer.GLOBAL_DIRECTOR.restarting = True


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


set_scene_color = set_window_color
get_scene_color = get_window_color


def set_game_state(new_state):
    check_initialized()
    designer.GLOBAL_DIRECTOR.game_state = new_state


def set_world_state(new_state):
    set_game_state(new_state)


def set_window_state(new_state):
    set_game_state(new_state)


def set_window_layers(new_layers):
    check_initialized()
    if designer.GLOBAL_DIRECTOR.current_scene:
        designer.GLOBAL_DIRECTOR.current_scene.layers = new_layers


def get_window_layers():
    check_initialized()
    if designer.GLOBAL_DIRECTOR.current_scene:
        return designer.GLOBAL_DIRECTOR.current_scene.layers
    else:
        return []


get_scene_layers = get_window_layers
set_scene_layers = set_window_layers


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
        designer.GLOBAL_DIRECTOR.screen = pygame.display.set_mode((width, height))
    designer.GLOBAL_DIRECTOR.window_size = width, height


def get_width(object=None):
    check_initialized()
    if object is None:
        return designer.GLOBAL_DIRECTOR.window_size[0]
    return object.width


def get_height(object=None):
    check_initialized()
    if object is None:
        return designer.GLOBAL_DIRECTOR.window_size[1]
    return object.height


def get_window_width():
    """
    Get the width of the window.

    :return: pixels of horizontal width of window
    :rtype: int
    """
    return get_width()


def get_window_height():
    """
    Get the height of the window.

    :return: pixels of vertical height of window
    :rtype: int
    """
    return get_height()


get_scene_width = get_window_width
get_scene_height = get_window_height


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
                    scene = designer.GLOBAL_DIRECTOR.current_scene
                    scene._send_event_to_handler(event, 'updating', weak_function(func), None, None, None, None)

            return _inner_dynamic_event

        funcs = [_dynamic_event(f) for f in funcs]
    # Event must be a string
    targets = None
    if ':' in event:
        event, *targets = event.split(':')
        event = event.strip()
        targets = [t.strip() for t in targets]
    if event not in KNOWN_EVENTS and not any(e.startswith(event) for e in KNOWN_EVENTS):
        suggestions = make_suggestions(event, KNOWN_EVENTS)
        if suggestions:
            raise ValueError(f"Unrecognized event {event!r}. Perhaps you meant one of: {suggestions}")
        else:
            raise ValueError(
                f"Unrecognized event {event!r}. Check the documentation to see possible events (like 'updating' and 'starting').")
    if funcs:
        for func in funcs:
            register(event, func, targets=targets)
    else:
        def decorated(function):
            register(event, function, targets=targets)

        return decorated


def starting(*funcs):
    return when('starting', *funcs)


def updating(*funcs):
    return when('updating', *funcs)


def typing(*funcs):
    return when('typing', *funcs)


def clicking(*funcs):
    return when('clicking', *funcs)


# TODO: would_be_colliding function to test a hypothetical move

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


def colliding_with_mouse(object):
    return object.collide_point(get_mouse_position())


def would_collide(*args):
    if len(args) == 3:
        obj1, (new_x, new_y), obj2 = args
    elif len(args) == 4:
        obj1, new_x, new_y, obj2 = args
    else:
        raise ValueError(f"Incorrect number of arguments to would_collide - expected 3 or 4, got {len(args)}")
    return obj1.collide_other_at(obj2, new_x, new_y)


def destroy(*gobjects):
    check_initialized()
    for gobject in gobjects:
        gobject.destroy()


# TODO: Fix to centralize
_USER_AGENT = "Designer Game Library for Python"


def background_image(path):
    check_initialized()
    if ALT_MODE:
        designer.GLOBAL_DIRECTOR.current_scene.background = InternalImage(filename=path)
    else:
        try:
            path_strs = path.split('/')
            fixed_paths = os.path.join(*path_strs)
            if os.path.exists(fixed_paths):
                designer.GLOBAL_DIRECTOR.current_scene.background = InternalImage(fixed_paths)
            else:
                raise FileNotFoundError(fixed_paths)
        except FileNotFoundError as err:
            try:
                req = Request(path, headers={'User-Agent': _USER_AGENT})
                with urlopen(req) as opened_image:
                    image_str = opened_image.read()
                    image_file = io.BytesIO(image_str)
                    designer.GLOBAL_DIRECTOR.current_scene.background = InternalImage(filename=path,
                                                                                       fileobj=image_file)
            except:
                print(f"Unexpected error while loading background image: {path}\n", sys.exc_info()[0])
                raise


set_background_image = background_image
set_window_image = set_background_image
set_scene_image = set_background_image

def get_background_image():
    return designer.GLOBAL_DIRECTOR.current_scene.background

get_window_image = get_background_image
get_scene_image = get_background_image


def get_director():
    check_initialized()
    return designer.GLOBAL_DIRECTOR


def change_scene(window_name, **kwargs):
    check_initialized()
    designer.GLOBAL_DIRECTOR.change_scene(window_name, kwargs)
