import os
from typing import List

import pygame

try:
    from weakref import WeakSet
except ImportError:
    WeakSet = set

from designer.colors import _process_color
from designer.core.scene import Scene
from designer.core.event import handle, Event, _pygame_to_spyral, GameEndException, register
from designer.keyboard import KeyboardModule
from designer.mouse import MouseModule
from designer.music import MusicModule
from designer.sfx import SfxModule

DEFAULT_WINDOW_TITLE = os.environ.get('DESIGNER_WINDOW_TITLE', "Designer Game")
DEFAULT_WINDOW_WIDTH = os.environ.get('DESIGNER_WINDOW_WIDTH', 800)
DEFAULT_WINDOW_HEIGHT = os.environ.get('DESIGNER_WINDOW_HEIGHT', 600)


class Director:
    def __init__(self, width=DEFAULT_WINDOW_WIDTH, height=DEFAULT_WINDOW_HEIGHT,
                 background_color=(255, 255, 255, 255), fps=30):
        """
        Initializes the Director that will control the game state.

        :param width: width of the game window in pixels
        :type width: int
        :param height: height of the game window in pixels
        :type height: int
        :param background_color: color to initially fill the window with
        """
        pygame.init()
        self._window_size = int(width), int(height)
        self._window_title = DEFAULT_WINDOW_TITLE
        self._window_color = background_color
        self._fps = fps
        self._tick = 0
        self.running = False
        self.paused = False
        self.restarting = False
        self.debug_mode = False
        self.debug_window = None

        self._all_sprites = WeakSet()

        self._first_scene = None
        self.scene_name = ""
        self._scenes: List[Scene] = []
        self._delayed_event_registrations = {None: []}
        self._scene_changed = False

        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self._window_color)
        pygame.display.set_caption(self._window_title)

        self.keyboard = KeyboardModule()
        self.mouse = MouseModule()
        self.music = MusicModule()
        self.sfx = SfxModule()

    def _setup_initial_scene(self):
        new_scene = Scene(self._window_size, self._fps)
        self._scenes.append(new_scene)
        register("system.quit", self.stop)
        new_scene._register_default_events()

    def _switch_scene(self):
        """
        Ensure that dead sprites are removed from the list and that sprites are
        redrawn on a scene change.
        """
        self._all_sprites = WeakSet({s for s in self._all_sprites
                                     if s is not None and s._scene() is not None and s._parent() is not None
                                     and s._expire_static()})

    def _track_object(self, object):
        self.all_sprites.add(object)

    def _untrack_object(self, object):
        self.all_sprites.remove(object)

    @property
    def tick(self):
        return self._tick

    @property
    def fps(self):
        return self._fps

    @property
    def current_scene(self):
        return self._scenes[-1]

    @property
    def game_state(self):
        return self._scenes[-1]._game_state

    @game_state.setter
    def game_state(self, value):
        self._scenes[-1]._game_state = value


    @property
    def all_sprites(self):
        return self._all_sprites

    @all_sprites.setter
    def all_sprites(self, value):
        self._all_sprites = WeakSet(value)

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
        self.current_scene.background.fill(_process_color(value))
        self.current_scene.background._version += 1

    scene_title = window_title
    scene_size = window_size
    scene_color = window_color

    def register(self, event_namespace, handlers, args, kwargs, priority, dynamic, targets):
        if not targets:
            self.current_scene._reg_internal(event_namespace, handlers, args, kwargs, priority, dynamic)
            self._delayed_event_registrations[None].append(
                (event_namespace, handlers, args, kwargs, priority, dynamic))
        else:
            if self._first_scene is None:
                self._first_scene = targets[0]
                self.scene_name = self._first_scene
            for target in targets:
                if target not in self._delayed_event_registrations:
                    self._delayed_event_registrations[target] = []
                self._delayed_event_registrations[target].append((event_namespace, handlers, args, kwargs, priority, dynamic))

    def register_delayed_events(self, new_scene, scene_name):
        if scene_name in self._delayed_event_registrations:
            events = self._delayed_event_registrations[scene_name]
            for event in events:
                new_scene._reg_internal(*event)
        # Global default events
        events = self._delayed_event_registrations[None]
        for event in events:
            new_scene._reg_internal(*event)

    def change_scene(self, scene_name, kwargs):
        self._scene_changed = ('replace', scene_name, kwargs)

    def push_scene(self, scene_name, kwargs):
        self._scene_changed = ('push', scene_name, kwargs)

    def pop_scene(self, kwargs):
        self._scene_changed = ('pop', None, kwargs)

    def _do_scene_change(self, change_type, scene_name, kwargs):
        if self._scenes:
            old_scene = self._scenes[-1]
            old_scene._handle_event('director.scene.exit',
                                    Event(world=old_scene._game_state, scene=old_scene, **kwargs))
            if change_type in ('replace', 'pop'):
                self._scenes.pop()
            self._switch_scene()
            del old_scene

        if change_type in ('replace', 'push'):
            new_scene = Scene(self._window_size, self._fps)
            self._scenes.append(new_scene)
            register("system.quit", self.stop)
            new_scene._register_default_events(True)
            self.scene_name = scene_name
            self.register_delayed_events(new_scene, scene_name)

            # Run new starting, if necessary
            new_game_state = new_scene._handle_event('director.start', Event(scene=new_scene, **kwargs))
            if new_game_state is not None:
                self.game_state = new_game_state
            del new_game_state

        latest_scene = self._scenes[-1]
        handle('director.scene.enter',
               event=Event(world=latest_scene._game_state, scene=latest_scene, **kwargs))
        # Empty all events!
        pygame.event.get()
        self._scene_changed = True

    def print_all_sprites(self):
        print(len(self._all_sprites))
        print({repr(s) for s in self._all_sprites if s is not None})
        import gc
        gc.collect()
        import objgraph
        print(">>>", len(self._all_sprites))
        #for obj in list(self._all_sprites):
        #    name = ''.join(filter(str.isalnum, repr(obj)))
        #    objgraph.show_backrefs([obj], filename=f'graphs/{self.scene_name}_{name}.png',
        #                           max_depth=6, refcounts=True, extra_info=lambda x: hex(id(x)))


    def replace(self, scene):
        """
        Replace the currently running scene on the stack with *scene*.
        Execution will continue after this is called, so make sure you return;
        otherwise you may find unexpected behavior::

            designer.director.replace(Scene())
            print("This will be printed!")
            return

        :param scene: The new scene.
        :type scene: :class:`Scene <designer.core.scene.Scene>`
        """
        if self._scenes:
            handle('director.scene.exit')
            self._scenes.pop()
            self._switch_scene()
        self._scenes.append(scene)
        scene._register_default_events()
        handle('director.scene.enter', event=Event(scene=scene))
        # Empty all events!
        pygame.event.get()

    def pop(self):
        """
        Pop the top scene off the stack, returning control to the next scene
        on the stack. If the stack is empty, the game will stop.
        This does return control, so remember to return immediately after
        calling it.
        """
        if len(self._scenes) < 1:
            return
        handle('director.scene.exit')
        self._scenes.pop()
        self._switch_scene()
        if self._scenes:
            handle('director.scene.enter')
        else:
            self.stop()
        # Empty all events!
        pygame.event.get()

    def push(self, scene):
        """
        Place *scene* on the top of the stack, and move control to it. This does
        return control, so remember to return immediately after calling it.

        :param scene: The new scene.
        :type scene: :class:`Scene <designer.core.scene.Scene>`
        """
        if self._scenes:
            handle('director.scene.exit')
            self._switch_scene()
        self._scenes.append(scene)
        scene._register_default_events()
        handle('director.scene.enter')
        # Empty all events!
        pygame.event.get()

    def debug(self, initial_game_state):
        self.debug_mode = True
        self.start(initial_game_state)

    def stop_debug_mode(self):
        self.debug_mode = False
        self.debug_window = None

    def start(self, initial_game_state, run_once=False):
        """
        Starts Pygame main game loop. Checks for events and DirtySprite updates. Handles animations.

        :return: None
        """
        if not self._scenes:
            return
        old_scene = None
        scene = self.current_scene
        clock = scene.clock
        stack = self._scenes
        # Finish scene setup
        if self._first_scene is not None:
            self.scene_name = self._first_scene
            self.register_delayed_events(scene, self._first_scene)
        # Load up initial game state
        new_game_state = scene._handle_event('director.start', Event(scene=self))
        if new_game_state is not None:
            self.game_state = new_game_state
        else:
            self.game_state = initial_game_state
        del new_game_state
        del initial_game_state
        # Hide any unused references
        from designer.utilities.search import _detect_objects_recursively
        self.all_sprites = _detect_objects_recursively(self.game_state)
        for object in self.all_sprites:
            if object:
                object._reactivate()
        # Set up debug window
        if self.debug_mode:
            from designer.tk.debug import DebugWindow
            self.debug_window = DebugWindow(self)
        # Start running the game!
        self.running = True
        try:
            while self.running:
                scene = stack[-1]
                if scene is not old_scene:
                    clock = scene.clock
                    old_scene = scene

                    def frame_callback(interpolation):
                        """
                        A closure for handling drawing, which includes forcing the
                        rendering-related events to be fired.
                        """
                        scene._handle_event("director.pre_render")
                        scene._handle_event("director.render", Event(world=self.game_state))
                        scene._draw()
                        scene._handle_event("director.post_render")

                    def update_callback(delta):
                        """
                        A closure for handling events, which includes firing the update
                        related events (e.g., pre_update, update, and post_update).
                        """
                        if self.paused:
                            scene._event_source.tick()
                            for event in scene._event_source.get():
                                if event.type == pygame.QUIT:
                                    self.stop()
                            self._tick += 1
                            return
                        if self.restarting:
                            scene._handle_event("director.restart")
                            self.restart()
                        if len(pygame.event.get([pygame.VIDEOEXPOSE])) > 0:
                            scene.redraw()
                            scene._handle_event("director.redraw")

                        scene._event_source.tick()
                        events = scene._event_source.get()
                        for event in events:
                            scene._queue_event(*_pygame_to_spyral(event, world=self.game_state))
                        scene._handle_event("director.pre_update")
                        scene._handle_event('director.update', Event(world=self.game_state, delta=delta))
                        self._tick += 1
                        scene._handle_event("director.post_update")

                    clock.frame_callback = frame_callback
                    clock.update_callback = update_callback
                clock.tick()
                if self._scene_changed:
                    self._do_scene_change(*self._scene_changed)
                    self._scene_changed = False
                if run_once:
                    frame_callback(0)
                    self.running = False
        except GameEndException:
            pass

    def stop(self):
        """ Cleanly quits the game. """
        self.running = False
        pygame.quit()
        raise GameEndException("The game has ended correctly")

    def pause(self, new_state=True):
        self.paused = new_state

    def restart(self):
        # TODO: This logic should adjust to new game starting concept
        for object in set(self.all_sprites):
            object.destroy()
        scene = self.current_scene
        self.game_state = scene._handle_event('director.start', Event(scene=self))
        # Hide any unused references
        from designer.utilities.search import _detect_objects_recursively
        self.all_sprites = _detect_objects_recursively(self.game_state)
        self.restarting = False