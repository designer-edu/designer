from typing import List

import designer
import sys
import weakref
import inspect
from pprint import pprint
from weakref import ref as _wref

from designer.core.window import Window
from designer.core.event import handle, Event, _pygame_to_spyral, GameEndException, register

DEFAULT_WINDOW_TITLE = "Designer Game"
import pygame


class Director:
    def __init__(self, width=800, height=600, background_color=(255, 255, 255), fps=50):
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
        self._fps = fps
        self._tick = 0
        self.running = False

        self._windows: List[Window] = []

        self._all_sprites: List[_wref] = []
        self._game_state = None

        self.screen = pygame.display.set_mode(self.window_size)
        self.background_color = background_color
        self.screen.fill(self.background_color)

    def _setup_initial_window(self):
        new_window = Window()
        self._windows.append(new_window)
        register("system.quit", self.stop)
        new_window._register_default_events()

    def _switch_window(self):
        """
        Ensure that dead sprites are removed from the list and that sprites are
        redrawn on a window change.
        """
        self._all_sprites = [s for s in self._all_sprites
                             if s() is not None and s()._expire_static()]

    def _track_object(self, object):
        self._all_sprites.append(_wref(object))

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

    @property
    def width(self):
        return self._window_size[0]

    @property
    def height(self):
        return self._window_size[1]

    @property
    def window_title(self):
        return self._window_title

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

    def start(self):
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
        self._game_state = window._handle_event('starting')
        try:
            while True:
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
                        new_graphics = window._handle_event("drawing", Event(world=self._game_state), collect_results=True)
                        window._draw()
                        window._handle_event("director.post_render")

                    def update_callback(delta):
                        """
                        A closure for handling events, which includes firing the update
                        related events (e.g., pre_update, update, and post_update).
                        """
                        if len(pygame.event.get([pygame.VIDEOEXPOSE])) > 0:
                            window.redraw()
                            window._handle_event("director.redraw")

                        window._event_source.tick()
                        events = window._event_source.get()
                        for event in events:
                            window._queue_event(*_pygame_to_spyral(event, world=self._game_state))
                        window._handle_event("director.pre_update")
                        window._handle_event('updating', Event(world=self._game_state, delta=delta))
                        window._handle_event("director.update", Event(world=self._game_state, delta=delta))
                        self._tick += 1
                        window._handle_event("director.post_update")

                    clock.frame_callback = frame_callback
                    clock.update_callback = update_callback
                clock.tick()
        except GameEndException:
            pass

        '''
        self.running = True
        self.all_game_objects.clear(self.screen, self.background)
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self.background_color)

        self._game_state = {}
        for handler in self.handlers.get('starting', {}):
            self._game_state = handler()

        while self.running:
            pygame.time.Clock().tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_events('typing', event.key, event.mod, event.unicode, event.scancode)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_events('clicking', *event.pos, event.button)
            self.remove_dead_objects()
            for gobject in self.all_game_objects:
                gobject._handle_animation()
            for group in self.groups:
                group._handle_animation()
            self.handle_events('updating', self.tick)
            self.tick += 1
            self.all_game_objects.update()
            rects = self.all_game_objects.draw(self.screen)
            pygame.display.update(rects)
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        '''

    def stop(self):
        """ Cleanly quits the game. """
        pygame.quit()
        raise GameEndException("The game has ended correctly")
