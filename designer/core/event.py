"""This module contains functions and classes for creating and issuing events.
For a list of the events that are built into Designer, check the
:ref:`Event List<ref.events>`.

    .. attribute:: keys

        A special attribute for accessing the constants associated with a given
        key. For instance, ``designer.keys.down`` and ``designer.keys.f``. This is
        useful for testing for keyboard events. A complete list of all the key
        constants can be found in the
        :ref:`Keyboard Keys <ref.keys>` appendix.

    .. attribute:: mods

        A special attribute for accessing the constants associated with a given
        mod key. For instance, ``designer.mods.lshift`` (left shift) and
        ``designer.mods.ralt`` (Right alt). This is useful for testing for keyboard
        events. A complete list of all the key
        constants can be found in the
        :ref:`Keyboard Modifiers <ref.mods>` appendix.

"""
import inspect

import pygame

import json
import os
import random
import base64

import designer
from weakref import WeakMethod
from designer.utilities.weak_method import WeakMethod as _wm


def WeakMethod(func):
    try:
        return _wm(func)
    except TypeError:
        return func


class GameEndException(Exception):
    pass


class Event:
    """
    A class for building for attaching data to an event.
    Keyword arguments will be named attributes of the Event when it is passed
    into :func:`queue <designer.core.event.queue>`::

        collision_event = Event(ball=ball, paddle=paddle)
        designer.core.event.queue("ball.collides.paddle", collision_event)
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __repr__(self):
        return f"<Event {self.__dict__!r}>"


# This might actually be unused!
_EVENT_NAMES = ['QUIT', 'ACTIVEEVENT', 'USEREVENT',
                'KEYDOWN', 'KEYUP',
                'MOUSEMOTION', 'MOUSEBUTTONUP', 'MOUSEBUTTONDOWN',
                'VIDEORESIZE', 'VIDEOEXPOSE',
                ]
MOUSE_MAP = ['left', 'middle', 'right', 'scroll_up', 'scroll_down']

_TYPE_TO_ATTRS = {
    pygame.QUIT: tuple(),
    pygame.ACTIVEEVENT: ('gain', 'state'),
    pygame.KEYDOWN: ('key', 'unicode', 'mod'),
    pygame.KEYUP: ('key', 'mod'),
    pygame.MOUSEMOTION: ('pos', 'rel', 'buttons'),
    pygame.MOUSEBUTTONUP: ('pos', 'button'),
    pygame.MOUSEBUTTONDOWN: ('pos', 'button'),
    pygame.VIDEORESIZE: ('size', 'w', 'h'),
    pygame.VIDEOEXPOSE: tuple(),
    pygame.AUDIODEVICEADDED: ('which', 'iscapture'),
    pygame.AUDIODEVICEREMOVED: ('which', 'iscapture'),
    pygame.FINGERMOTION: ('touch_id', 'finger_id', 'x', 'y', 'dx', 'dy'),
    pygame.FINGERDOWN: ('touch_id', 'finger_id', 'x', 'y', 'dx', 'dy'),
    pygame.FINGERUP: ('touch_id', 'finger_id', 'x', 'y', 'dx', 'dy'),
    pygame.MOUSEWHEEL: ('which', 'flipped', 'x', 'y'),
    pygame.MULTIGESTURE: ('touch_id', 'x', 'y', 'pinched', 'rotated', 'num_fingers'),
    pygame.TEXTEDITING: ('text', 'start', 'length'),
    pygame.TEXTINPUT: ('text', ),
    #pygame.WINDOWEVENT: ('event', ),
}

COMMON_EVENT_NAMES = {
    'drawing': 'director.render',
    'starting': 'director.start',
    'updating': 'director.update',
    'quitting': 'system.quit',
    'typing': 'input.keyboard.down',
    'done typing': 'input.keyboard.up',
    'scrolling': 'input.mouse.wheel',
    'tapping': 'input.touch.gesture',
    'clicking': 'input.mouse.down',
    'done clicking': 'input.mouse.down',
    'mouse motion': 'input.mouse.motion',
}

COMMON_EVENT_NAME_LOOKUP = {v: k for k, v in COMMON_EVENT_NAMES.items()}

_TYPE_TO_TYPE = {
    pygame.QUIT: "system.quit",
    pygame.ACTIVEEVENT: "system.focus_change",
    pygame.KEYDOWN: "input.keyboard.down",
    pygame.KEYUP: "input.keyboard.up",
    pygame.MOUSEMOTION: "input.mouse.motion",
    pygame.MOUSEBUTTONUP: "input.mouse.up",
    pygame.MOUSEBUTTONDOWN: "input.mouse.down",
    pygame.VIDEORESIZE: "system.video_resize",
    pygame.VIDEOEXPOSE: "system.video_expose",
    pygame.AUDIODEVICEADDED: 'system.audio_added',
    pygame.AUDIODEVICEREMOVED: 'system.audio_removed',
    pygame.FINGERMOTION: 'input.finger.motion',
    pygame.FINGERDOWN: 'input.finger.down',
    pygame.FINGERUP: 'input.finger.up',
    pygame.MOUSEWHEEL: 'input.mouse.wheel',
    pygame.MULTIGESTURE: 'input.touch.gesture',
    pygame.TEXTEDITING: 'input.text.editing',
    pygame.TEXTINPUT: 'input.text.input',
}

KNOWN_EVENTS = [*_TYPE_TO_TYPE.values(), *COMMON_EVENT_NAMES.keys()]


def get_positional_event_parameters(event_type: str, event):
    if event_type in ("updating", "director.update"):
        return "world", "delta"
    elif event_type in ("typing", ) or event_type.startswith("input.keyboard"):
        return "world", "key", "modifier", "character"
    elif event_type.startswith("input.mouse.motion"):
        return "world", "x", "y", "left", "middle", "right"
    elif event_type in ("clicking",) or event_type.startswith("input.mouse"):
        return "world", "x", "y", "button"
    elif event_type in ("starting", "director.start"):
        return "window"
    return [key for key in dir(event) if not key.startswith("__")]


def queue(event_name, event=None):
    """
    Queues a new event in the system, meaning that it will be run at the next
    available opportunity.

    :param str event_name: The type of event (e.g., ``"system.quit"``,
                           ``"input.mouse.up"``, or ``"pong.score"``.
    :param event: An Event object that holds properties for the event.
    :type event: :class:`Event <spyral.event.Event>`
    """
    designer.GLOBAL_DIRECTOR.current_window._queue_event(event_name, event)


def handle(event_name, event=None):
    """
    Instructs spyral to execute the handlers for this event right now. When you
    have a custom event, this is the function you call to have the event occur.

    :param str event_name: The type of event (e.g., ``"system.quit"``,
                           ``"input.mouse.up"``, or ``"pong.score"``.
    :param event: An Event object that holds properties for the event.
    :type event: :class:`Event <spyral.event.Event>`
    """
    designer.GLOBAL_DIRECTOR.current_window._handle_event(event_name, event)


def register(event_namespace, handler,
             args=None, kwargs=None, priority=0):
    """
    Registers an event `handler` to a namespace. Whenever an event in that
    `event_namespace` is fired, the event `handler` will execute with that
    event.

    :param event_namespace: the namespace of the event, e.g.
                            ``"input.mouse.left.click"`` or ``"pong.score"``.
    :type event_namespace: str
    :param handler: A function that will handle the event. The first
                    argument to the function will be the event.
    :type handler: function
    :param args: any additional arguments that need to be passed in
                 to the handler.
    :type args: sequence
    :param kwargs: any additional keyword arguments that need to be
                   passed into the handler.
    :type kwargs: dict
    :param int priority: the higher the `priority`, the sooner this handler will
                         be called in reaction to the event, relative to the
                         other event handlers registered.
    """
    event_namespace = COMMON_EVENT_NAMES.get(event_namespace, event_namespace)
    designer.GLOBAL_DIRECTOR.current_window._reg_internal(event_namespace, (WeakMethod(handler),),
                                                          args, kwargs, priority, False)


def unregister(event_namespace, handler):
    """
    Unregisters a registered handler for that namespace. Dynamic handler
    strings are supported as well.

    :param str event_namespace: An event namespace
    :param handler: The handler to unregister.
    :type handler: a function or string.
    """
    designer.GLOBAL_DIRECTOR.current_window._unregister(event_namespace, handler)


def clear_namespace(namespace):
    """
    Clears all handlers from namespaces that are at least as specific as the
    provided `namespace`.

    :param str namespace: The complete namespace.
    """
    designer.GLOBAL_DIRECTOR.current_window._clear_namespace(namespace)


class KeyboardKey:
    def __init__(self, value):
        self._value = value

    def __hash__(self):
        return hash(pygame.key.name(self._value))

    def __eq__(self, other):
        if isinstance(other, KeyboardKey):
            return self._value == other._value
        elif isinstance(other, int):
            return self._value == other
        elif isinstance(other, str):
            return self._value == pygame.key.key_code(other)
        else:
            raise TypeError(f"You attempted to compare a string Key ({self!r}) with the value {other!r}, but those types were not compatible.")

    def __repr__(self):
        return pygame.key.name(self._value)


def _pygame_to_spyral(event, **kwargs):
    """
    Convert a Pygame event to a Spyral event, correctly converting arguments to
    attributes.
    """
    event_attrs = _TYPE_TO_ATTRS.get(event.type, tuple())
    event_type = _TYPE_TO_TYPE.get(event.type, f'unknown.event[{event.type}]')
    e = Event(**kwargs)
    for attr in event_attrs:
        setattr(e, attr, getattr(event, attr))
    if event_type.startswith("input"):
        setattr(e, "type", event_type.split(".")[-1])
    if event_type.startswith('input.keyboard'):
        k = keys.reverse_map.get(event.key, 'unknown')
        event_type += '.' + k
        e.key = KeyboardKey(event.key)
        e.modifier = event.mod
        e.character = event.unicode
    if event_type.startswith('input.mouse.motion'):
        e.left, e.middle, e.right = map(bool, event.buttons)
    elif event_type.startswith('input.mouse.up') or event_type.startswith('input.mouse.down'):
        try:
            m = MOUSE_MAP[event.button - 1]
            setattr(e, "button", m)
        except IndexError:
            m = str(event.button)
        event_type += '.' + m
    if event_type.startswith('input.mouse.wheel'):
        e.pos = designer.utilities.Vec2D(e.x, e.y) / designer.GLOBAL_DIRECTOR.current_window._scale
        e.x = e.pos[0]
        e.y = e.pos[1]
    elif event_type.startswith('input.mouse') or event_type.startswith('input.touch'):
        e.pos = designer.utilities.Vec2D(e.pos) / designer.GLOBAL_DIRECTOR.current_window._scale
        e.x = e.pos[0]
        e.y = e.pos[1]

    return (event_type, e)


class EventHandler(object):
    """
    Base event handler class.
    """

    def __init__(self):
        self._events = []
        self._mouse_pos = (0, 0)

    def tick(self):
        """
        Should be called at the beginning of update cycle. For the
        event handler which is part of a scene, this function will be
        called automatically. For any additional event handlers, you
        must call this function manually.
        """
        pass

    def get(self, types=None):
        """
        Gets events from the event handler. Types is an optional
        iterable which has types which you would like to get.
        """
        if types is None:
            types = []
        try:
            types[0]
        except IndexError:
            pass
        except TypeError:
            types = (types,)

        if types == []:
            ret = self._events
            self._events = []
            return ret

        ret = [e for e in self._events if e['type'] in types]
        self._events = [e for e in self._events if e['type'] not in types]
        return ret


class LiveEventHandler(EventHandler):
    """
    An event handler which pulls events from the operating system.

    The optional output_file argument specifies the path to a file
    where the event handler will save a custom json file that can
    be used with the `ReplayEventHandler` to show replays of a
    game in action, or be used for other clever purposes.

    .. note::

        If you use the output_file parameter, this function will
        reseed the random number generator, save the seed used. It
        will then be restored by the ReplayEventHandler.
    """

    def __init__(self, output_file=None):
        EventHandler.__init__(self)
        self._save = output_file is not None
        if self._save:
            self._file = open(output_file, 'w')
            seed = os.urandom(4)
            info = {'random_seed': base64.encodestring(seed)}
            random.seed(seed)
            self._file.write(json.dumps(info) + "\n")

    def tick(self):
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        self._mouse_pos = mouse
        self._events.extend(events)
        # if self._save:
        #     d = {'mouse': mouse, 'events': events}
        #     self._file.write(json.dumps(d) + "\n")

    def __del__(self):
        if self._save:
            self._file.close()


class ReplayEventHandler(EventHandler):
    """
    An event handler which replays the events from a custom json
    file saved by the `LiveEventHandler`.
    """

    def __init__(self, input_file):
        EventHandler.__init__(self)
        self._file = open(input_file)
        info = json.loads(self._file.readline())
        random.seed(base64.decodestring(info['random_seed']))
        self.paused = False

    def pause(self):
        """
        Pauses the replay of the events, making tick() a noop until
        resume is called.
        """
        self.paused = True

    def resume(self):
        """
        Resumes the replay of events.
        """
        self.paused = False

    def tick(self):
        if self.paused:
            return
        try:
            d = json.loads(self._file.readline())
        except ValueError:
            # spyral.director.pop()
            pass
        events = d['events']
        events = [Event(e) for e in events]
        self._mouse_pos = d['mouse']
        self._events.extend(events)


class Mods(object):
    def __init__(self):
        self.none = pygame.KMOD_NONE
        self.lshift = pygame.KMOD_LSHIFT
        self.rshift = pygame.KMOD_RSHIFT
        self.shift = pygame.KMOD_SHIFT
        self.caps = pygame.KMOD_CAPS
        self.ctrl = pygame.KMOD_CTRL
        self.lctrl = pygame.KMOD_LCTRL
        self.rctrl = pygame.KMOD_RCTRL
        self.lalt = pygame.KMOD_LALT
        self.ralt = pygame.KMOD_RALT
        self.alt = pygame.KMOD_ALT


class Keys(object):

    def __init__(self):
        self.reverse_map = {}
        self.load_keys_from_file(designer.utilities.file_system.get_resource('default_key_mappings.txt'))
        self._fix_bad_names([("return", "enter"), ("break", "brk")])

    def _fix_bad_names(self, renames):
        """
        Used to replace any binding names with non-python keywords.
        """
        for original, new in renames:
            setattr(self, new, getattr(self, original))
            delattr(self, original)

    def load_keys_from_file(self, filename):
        fp = open(filename)
        key_maps = fp.readlines()
        fp.close()
        for single_mapping in key_maps:
            mapping = single_mapping[:-1].split(' ')
            if len(mapping) == 2:
                if mapping[1][0:2] == '0x':
                    setattr(self, mapping[0], int(mapping[1], 16))
                    self.reverse_map[int(mapping[1], 16)] = mapping[0]
                else:
                    setattr(self, mapping[0], int(mapping[1]))
                    self.reverse_map[int(mapping[1])] = mapping[0]

    def add_key_mapping(self, name, number):
        setattr(self, name, number)


keys = Keys()
mods = Mods()
