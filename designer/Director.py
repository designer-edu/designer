from typing import List

import designer
import sys
import pygame
import weakref
import inspect


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
        self.window_size = width, height
        self.screen = pygame.display.set_mode(self.window_size)
        self.bkgr_color = background_color
        self.screen.fill(background_color)

        self.width = width
        self.height = height
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.bkgr_color)

        self.fps = fps
        self.running = False
        self.all_game_objects = pygame.sprite.LayeredDirty()
        self.groups = []

        self.handlers = {
            'updating': [],
            'starting': [],
            'typing': [],
            'clicking': []
        }

    def start(self):
        """
        Starts Pygame main game loop. Checks for events and DirtySprite updates. Handles animations.

        :return: None
        """
        self.running = True
        self.all_game_objects.clear(self.screen, self.background)
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self.bkgr_color)

        self._game_state = {}
        for handler in self.handlers.get('starting', {}):
            self._game_state = handler()

        time = 0
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
            self.handle_events('updating', time)
            time += 1
            self.all_game_objects.update()
            rects = self.all_game_objects.draw(self.screen)
            pygame.display.update(rects)
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def handle_events(self, event_name, *events):
        for func in self.handlers.get(event_name, []):
            parameters_expected = len(inspect.signature(func).parameters)-1
            result = func(self._game_state, *events[:parameters_expected])
            if result is not None:
                self._game_state = result
            self.remove_dead_objects()

    def remove_dead_objects(self):
        pass
        #self.all_game_objects = [gobject for gobject in self.all_game_objects if gobject is not None]
        #self.all_game_objects.remove([None])
        #self.groups = [g for g in self.groups if g is not None]
        #for gobject in self.all_game_objects:
        #    print(gobject, sys.getrefcount(gobject))

    def add(self, *images):
        """
        Adds a DirtySprite to Director's DirtySprite collection.

        :param images: images to add to self's DirtySprite collection
        :type images: designer.DesignerObjects

        :return: nOne
        """
        for image in images:
            self.all_game_objects.add(image)
        rects = self.all_game_objects.draw(self.screen)
        pygame.display.update(rects)

    def add_group(self, *groups):
        """
        Adds group of DirtySprites to Director's group collection.

        :param groups: groups to add to self's group collection
        :type groups: designer.DesignerGroups

        :return: None
        """
        for group in groups:
            self.groups.append(group)
        rects = self.all_game_objects.draw(self.screen)
        pygame.display.update(rects)

    def add_handler(self, event, func):
        """
        Registers the given handler for the event.

        :param event:
        :param func:
        :return:
        """
        if event not in self.handlers:
            raise ValueError(f"Unknown event: {event}")
        self.handlers[event].append(func)

