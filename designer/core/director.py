from typing import List

import designer
import sys
import inspect
from pprint import pprint
import pygame
from weakref import WeakSet

from designer.colors import _process_color
from designer.core.window import Window
from designer.core.event import handle, Event, _pygame_to_spyral, GameEndException, register
from designer.keyboard import KeyboardModule
from designer.mouse import MouseModule
from designer.music import MusicModule
from designer.sfx import SfxModule

DEFAULT_WINDOW_TITLE = "Designer Game"


class Director:
    def __init__(self, width=800, height=600, background_color=(255, 255, 255), fps=30):
        """
        Initializes the Director that will control the game state.

        :param width: width of the game window in pixels
        :type width: int
        :param height: height of the game window in pixels
        :type height: int
        :param background_color: color to initially fill the window with
        """
        pygame.init()
        self._window_size = width, height
        self._window_title = DEFAULT_WINDOW_TITLE
        self._window_color = background_color
        self._fps = fps
        self._tick = 0
        self.running = False
        self.paused = False

        self._windows: List[Window] = []

        self._all_sprites: WeakSet = WeakSet([])
        self._game_state = None

        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self._window_color)
        pygame.display.set_caption(self._window_title)

        self.keyboard = KeyboardModule()
        self.mouse = MouseModule()
        self.music = MusicModule()
        self.sfx = SfxModule()

    def _setup_initial_window(self):
        new_window = Window(self._window_size, self._fps)
        self._windows.append(new_window)
        register("system.quit", self.stop)
        new_window._register_default_events()

    def _switch_window(self):
        """
        Ensure that dead sprites are removed from the list and that sprites are
        redrawn on a window change.
        """
        self._all_sprites = WeakSet([s for s in self._all_sprites
                                     if s is not None and s._expire_static()])

    def _track_object(self, object):
        self._all_sprites.add(object)

    @property
    def tick(self):
        return self._tick

    @property
    def fps(self):
        return self._fps

    @property
    def current_window(self):
        return self._windows[-1]

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    def window_size(self, value):
        self._window_size = value

    @property
    def width(self):
        return self._window_size[0]

    @property
    def height(self):
        return self._window_size[1]

    @property
    def window_title(self):
        return self._window_title

    @window_title.setter
    def window_title(self, value):
        self._window_title = value
        if isinstance(value, str):
            pygame.display.set_caption(value)

    @property
    def window_color(self):
        return self._window_color

    @window_color.setter
    def window_color(self, value):
        self._window_color = value
        self.screen.fill(_process_color(value))
        # TODO: Director shouldn't do this, the window itself should handle that
        self.current_window.background.fill(_process_color(value))
        self.current_window.background._version += 1

    def replace(self, window):
        """
        Replace the currently running window on the stack with *window*.
        Execution will continue after this is called, so make sure you return;
        otherwise you may find unexpected behavior::

            designer.director.replace(Window())
            print("This will be printed!")
            return

        :param window: The new window.
        :type window: :class:`Window <designer.core.window.Window>`
        """
        if self._windows:
            handle('director.scene.exit')
            self._windows.pop()
            self._switch_window()
        self._windows.append(window)
        window._register_default_events()
        handle('director.scene.enter', event=Event(window=window))
        # Empty all events!
        pygame.event.get()

    def pop(self):
        """
        Pop the top window off the stack, returning control to the next window
        on the stack. If the stack is empty, the game will stop.
        This does return control, so remember to return immediately after
        calling it.
        """
        if len(self._windows) < 1:
            return
        handle('director.scene.exit')
        self._windows.pop()
        self._switch_window()
        if self._windows:
            handle('director.scene.enter')
        else:
            self.stop()
        # Empty all events!
        pygame.event.get()

    def push(self, window):
        """
        Place *window* on the top of the stack, and move control to it. This does
        return control, so remember to return immediately after calling it.

        :param window: The new window.
        :type window: :class:`Window <designer.core.window.Window>`
        """
        if self._windows:
            handle('director.scene.exit')
            self._switch_window()
        self._windows.append(window)
        window._register_default_events()
        handle('director.scene.enter')
        # Empty all events!
        pygame.event.get()

    def start(self, initial_game_state):
        """
        Starts Pygame main game loop. Checks for events and DirtySprite updates. Handles animations.

        :return: None
        """
        if not self._windows:
            return
        old_window = None
        window = self.current_window
        clock = window.clock
        stack = self._windows
        # Load up initial game state
        new_game_state = window._handle_event('director.start', Event(window=self))
        if new_game_state is not None:
            self._game_state = new_game_state
        else:
            self._game_state = initial_game_state
        del new_game_state
        del initial_game_state
        # Hide any unused references
        from designer.utilities.search import _detect_objects_recursively
        kept_objects = _detect_objects_recursively(self._game_state)
        for obj in self._all_sprites:
            if obj not in kept_objects:
                obj.visible = False
        self._all_sprites = WeakSet(kept_objects)
        del kept_objects
        # Start running the game!
        self.running = True
        try:
            while self.running:
                window = stack[-1]
                if window is not old_window:
                    clock = window.clock
                    old_window = window

                    def frame_callback(interpolation):
                        """
                        A closure for handling drawing, which includes forcing the
                        rendering-related events to be fired.
                        """
                        window._handle_event("director.pre_render")
                        window._handle_event("director.render", Event(world=self._game_state))
                        window._draw()
                        window._handle_event("director.post_render")

                    def update_callback(delta):
                        """
                        A closure for handling events, which includes firing the update
                        related events (e.g., pre_update, update, and post_update).
                        """
                        if self.paused:
                            window._event_source.tick()
                            for event in window._event_source.get():
                                if event.type == pygame.QUIT:
                                    self.stop()
                            self._tick += 1
                            return
                        if len(pygame.event.get([pygame.VIDEOEXPOSE])) > 0:
                            window.redraw()
                            window._handle_event("director.redraw")

                        window._event_source.tick()
                        events = window._event_source.get()
                        for event in events:
                            window._queue_event(*_pygame_to_spyral(event, world=self._game_state))
                        window._handle_event("director.pre_update")
                        window._handle_event('director.update', Event(world=self._game_state, delta=delta))
                        self._tick += 1
                        window._handle_event("director.post_update")

                    clock.frame_callback = frame_callback
                    clock.update_callback = update_callback
                clock.tick()
        except GameEndException:
            pass

    def stop(self):
        """ Cleanly quits the game. """
        self.running = False
        pygame.quit()
        raise GameEndException("The game has ended correctly")

    def pause(self, new_state=True):
        self.paused = new_state
