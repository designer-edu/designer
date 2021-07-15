import math
from designer import GamesSprite
import pygame
import designer
import random
from typing import Tuple, Union


class Animation:
    def __init__(self, speed: int, direction: str):
        self.speed = speed
        self.direction = direction

    def start(self):
        pass

    def is_finished(self):
        return False


class GlideAnimation(Animation):
    def __init__(self, speed: int, direction: int):
        """
        Initializer of animations that glide across the screen.
        Calls initializer of Animations, parent  class.
        :param speed: int at which to move in pixels per frame
        :param direction: int in degrees at which to move
        """
        direction = math.radians(direction)
        self.x = math.cos(direction)
        self.y = math.sin(direction + math.pi)

        # handle moving by at least one pixel if value is less than one but not accounting for when value is genuinely 0
        if 0.01 < self.x < 1:
            self.x = math.ceil(self.x)
        if 0.01 < self.y < 1:
            self.y = math.ceil(self.y)
        super().__init__(speed, direction)

    def step(self, sprite: designer.GamesSprite):
        '''
        handles glide for each step of the game state
        :param sprite: GamesSprite to move
        :return:
        '''
        if isinstance(sprite, designer.GamesSprite):
            sprites = [sprite]
        elif isinstance(sprite, designer.GamesGroup):
            sprites = [sprite]
        for temp_sprite in sprites:
            if (
                    temp_sprite.rect.right) < designer.GLOBAL_DIRECTOR.width and temp_sprite.rect.x > 0 and temp_sprite.rect.top < designer.GLOBAL_DIRECTOR.height and temp_sprite.rect.y > 0:
                if not sprite.finished_animation:
                    temp_sprite.rect.x += (self.speed * self.x)
                    temp_sprite.rect.y += (self.speed * self.y)
                    temp_sprite.dirty = 1
            else:
                sprite.finished_animation = True


class JitterAnimation(Animation):
    def __init__(self, direction: int):
        self.direction = direction

    def step(self, sprite: designer.GamesSprite):
        if isinstance(sprite, designer.GamesSprite):
            sprites = [sprite]
        elif isinstance(sprite, designer.GamesGroup):
            sprites = sprite.sprites
            x_dir = random.randint(-self.direction, self.direction)
            y_dir = random.randint(-self.direction, self.direction)
            for sprite in sprites:
                sprite.rect.x += x_dir
                sprite.rect.y += y_dir
                sprite.dirty = 1


class RotateAnimation(Animation):
    def __init__(self, speed: int, direction: int, angle_limit: int, pos: Tuple):
        self.speed = speed
        self.angle = 1
        self.angle_limit = angle_limit
        self.pos = pos
        self.total = 0
        super().__init__(speed, direction)

    def step(self, sprite: designer.GamesSprite):
        '''
        handles rotation per step of the game state
        :param sprite: GamesSprite to be moved
        :return:
        '''
        if isinstance(sprite, designer.GamesSprite):
            sprites = [sprite]
        elif isinstance(sprite, designer.GamesGroup):
            sprites = sprite.sprites
        for sprite in sprites:
            if self.total < self.angle_limit:
                self.total = self.total + (self.speed * self.angle)
                sprite.image = pygame.transform.rotate(sprite.orig_img, self.total)
                sprite.rect = sprite.image.get_rect(center=sprite.orig_img.get_rect(center=(sprite.rect.center)).center)

                # self.angle += (self.speed * self.angle)
                sprite.dirty = 1


def glide_around(*sprites: designer.GamesSprite, speed: int):
    '''
    Moves sprite(s) around at random.
    :param sprites: collection of at least one GamesSprite to move around
    :param speed: int representing pixels to move per second
    :return:
    '''
    for sprite in sprites:
        sprite.add_animation(JitterAnimation(speed, 0))


def glide_right(sprite: designer.GamesSprite, speed: int):
    '''
       Moves sprite(s) to the right of the window.
       :param sprites: collection of at least one GamesSprite to move
       :param speed: int representing pixels to move per second
       :return:
       '''
    sprite.add_animation(GlideAnimation(speed, 0))


def glide_left(sprite: designer.GamesSprite, speed: int):
    '''
           Moves sprite(s) to the left of the window.
           :param sprites: collection of at least one GamesSprite to move
           :param speed: int representing pixels to move per second
           :return:
           '''
    sprite.add_animation(GlideAnimation(speed, 180))


def glide_up(sprite: designer.GamesSprite, speed: int):
    '''
           Moves sprite(s) up on the window.
           :param sprites: collection of at least one GamesSprite to move
           :param speed: int representing pixels to move per second
           :return:
     '''
    sprite.add_animation(GlideAnimation(speed, 90))


def glide_down(sprite: designer.GamesSprite, speed: int):
    '''
            Moves sprite(s) down on the window.
            :param sprites: collection of at least one GamesSprite to move
            :param speed: int representing pixels to move per second
            :return:
         '''
    sprite.add_animation((GlideAnimation(speed, 270)))


def glide_in_degrees(sprite: designer.GamesSprite, direction: int, speed: int):
    '''
    Moves sprite(s) a given number of degrees in a specific direction
    :param sprite: collection of at least one GamesSprite to move
    :param direction: direction in degrees counterclockwise for sprite to move
    :param speed: int representing pixels to move per second
    :return:
    '''
    sprite.add_animation((GlideAnimation(speed, direction)))


def rotate(sprite: GamesSprite, angle_limit: int, speed: int):
    '''
    Rotates sprite(s) in place for a given number of degrees
    :param sprite: collection of at least one GameSprite to move
    :param angle_limit: int in degrees to rotate sprite
    :param speed: int representing pixels to move per second
    :return:
    '''
    if isinstance(sprite, GamesSprite.GamesSprite):
        sprite.add_animation(RotateAnimation(speed, 0, angle_limit, sprite.rect.topleft))
    if isinstance(sprite, GamesSprite.GamesGroup):
        for temp_sprite in sprite.sprites:
            temp_sprite.add_animation(RotateAnimation(speed, 0, angle_limit, temp_sprite.rect.topleft))
