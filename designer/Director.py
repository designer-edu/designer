from typing import List

import designer
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

    def start(self):
        """
        Starts Pygame main game loop. Checks for events and DirtySprite updates. Handles animations.

        :return: None
        """
        self.running = True
        self.all_game_objects.clear(self.screen, self.background)
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(self.bkgr_color)

        time = 0
        while self.running:
            pygame.time.Clock().tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for gobject in self.all_game_objects:
                gobject._handle_animation()
            for group in self.groups:
                group._handle_animation()
            time += 1
            self.all_game_objects.update()
            rects = self.all_game_objects.draw(self.screen)
            pygame.display.update(rects)
        pygame.display.quit()
        pygame.quit()

    def add(self, *images):
        """
        Adds a DirtySprite to Director's DirtySprite collection.

        :param images: images to add to self's DirtySprite collection
        :type images: designer.DesignerObjects

        :return: nOne
        """
        for image in images:
            self.all_game_objects.add(image)

    def add_group(self, *groups):
        """
        Adds group of DirtySprites to Director's group collection.

        :param groups: groups to add to self's group collection
        :type groups: designer.DesignerGroups

        :return: None
        """
        for group in groups:
            self.groups.append(group)


def check_initialized():
    """
    Checks if global state exists and creates one if it does not.

    :return: None
    """

    if not designer.GLOBAL_DIRECTOR:
        designer.GLOBAL_DIRECTOR = Director()


def draw(*objs):
    """
    Internally starts the game loop.

    :return: None
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.start()


def set_window_color(color):
    '''
    Changes window color to given color.
    Must call before adding any DesignerObjects.

    :param color: color to change window to
    :type color: str or List[str]

    :return: None
    '''
    check_initialized()
    designer.GLOBAL_DIRECTOR.bkgr_color = color
    designer.GLOBAL_DIRECTOR.screen.fill(color)
    designer.GLOBAL_DIRECTOR.background.fill(color)


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
