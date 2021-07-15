from typing import Union, List

import designer
import pygame


class Director:
    def __init__(self, width=800, height=600, background_color=(255, 255, 255), fps = 50):
        """
        Initializes the Director that will control the game state.
        :param width: width of the game window in pixels
        :param height: height of the game window in pixels
        :param background_color: color to initially fill the window with
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.bkgr_color = background_color
        self.screen.fill(background_color)

        self.width = width
        self.height = height
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.bkgr_color)

        self.fps = fps
        self.running = False
        self.all_game_sprites = pygame.sprite.LayeredDirty()
        self.groups = []


    def start(self):
        """
        Starts Pygame main game loop. Checks for events and DirtySprite updates. Handles animations.
        :return:
        """
        self.running = True
        self.all_game_sprites.clear(self.screen, self.background)

        time = 0
        while self.running:
            pygame.time.Clock().tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            for gsprite in self.all_game_sprites:
                gsprite._handle_animation()
            for group in self.groups:
                group._handle_animation()
            time += 1
            self.all_game_sprites.update()
            rects = self.all_game_sprites.draw(self.screen)
            pygame.display.update(rects)

    def add(self, *images):
        """
        Adds a DirtySprite to Director's DirtySprite collection.
        :param images:
        :return:
        """
        for image in images:
            self.all_game_sprites.add(image)

    def add_group(self, *groups):
        """
        Adds group of DirtySprites to Director's group collection.
        :param groups:
        :return:
        """
        for group in groups:
            self.groups.append(group)


def check_initialized():
    """
    Checks if global state exists and creates one if it does not.
    :return:
    """
    if designer.GLOBAL_DIRECTOR is None:
        designer.GLOBAL_DIRECTOR = Director()


def draw(*images):
    """
    Internally starts the game loop.
    :param images:
    :return:
    """
    check_initialized()
    designer.GLOBAL_DIRECTOR.start()


def set_window_color(color: Union[str, List[str]]):
    '''
    Changes window color to given color.
    :param color: color to change window to
    :return: None
    '''
    check_initialized()
    designer.GLOBAL_DIRECTOR.bkgr_color = color
    designer.GLOBAL_DIRECTOR.screen.fill(color)
    designer.GLOBAL_DIRECTOR.background.fill(color)
