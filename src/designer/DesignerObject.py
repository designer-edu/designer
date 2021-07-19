import os
import shutil
import sys
from typing import Union, Tuple, List

import requests

from designer import Animation
import pygame
import designer
import random
import math

from designer.colors import _process_color


class GamesObject(pygame.sprite.DirtySprite):
    def __init__(self):
        designer.check_initialized()
        super().__init__()
        self.animations = []
        self.orig_img = None
        self.finished_animation = False

    def add(self):
        '''
        adds a object to the global state's object collection
        :return:
        '''
        designer.GLOBAL_DIRECTOR.add(self)
        self.orig_img = self.image.copy()

    def add_animation(self, animation: Animation):
        """
        Adds an animation to GamesObject's animations collection.
        :param animation: designer.Animation to be added
        :return:
        """
        self.animations.append(animation)

    def _handle_animation(self):
        for animation in self.animations:
            animation.step(self)


class Circle(GamesObject):
    def __init__(self, center: Tuple[int], size: int, color):
        super().__init__()
        self.dirty = 1
        color = _process_color(color)
        self.image = pygame.surface.Surface((2 * size, 2 * size), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(self.image, color, (size, size), size)

        self.center = center
        self.size = size
        self.color = color

        self.rect = self.image.get_rect(center=center)

        super().add()


class Ellipse(GamesObject):
    def __init__(self, left, top, width, height, color):
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((2 * width, 2 * height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.ellipse(self.image, color, (0, 0, width, height))

        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top

        super().add()


def make_ellipse(color, args):
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Ellipse(left, top, width, height, color)


class Arc(GamesObject):
    def __init__(self, color, start_angle, stop_angle, thickness, left, top, width, height):
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((width * 2, height * 2), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.arc(self.image, color, (0, 0, width, height), start_angle, stop_angle, width=thickness)

        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top

        super().add()


def make_arc(color, start_angle, stop_angle, thickness, args):
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Arc(color, start_angle, stop_angle, thickness, left, top, width, height)


class Line(GamesObject):
    def __init__(self, start, end, thickness, color):
        super().__init__()
        color = _process_color(color)
        self.dirty = 1

        (x1, y1), (x2, y2) = start, end
        # Need to flip y-axis
        angle = math.atan2(-(y2 - y1), x2 - x1) % 2 * math.pi
        p1x, p1y = x1 + math.cos(angle + math.pi / 2) * thickness, y1 + math.sin(angle + math.pi / 2) * thickness
        p2x, p2y = x1 + math.cos(angle - math.pi / 2) * thickness, y1 - math.sin(angle + math.pi / 2) * thickness
        p3x, p3y = x2 + math.cos(angle + math.pi / 2) * thickness, y2 + math.sin(angle + math.pi / 2) * thickness
        p4x, p4y = x2 + math.cos(angle - math.pi / 2) * thickness, y2 - math.sin(angle + math.pi / 2) * thickness
        left = min(p1x, p2x, p3x, p4x)
        right = max(p1x, p2x, p3x, p4x)
        top = min(p1y, p2y, p3y, p4y)
        bottom = max(p1y, p2y, p3y, p4y)

        # print(color, start, end, left, top, right, bottom, right - left, bottom - top)

        # calculate differences between x and y coordinates of line
        x = abs(start[0] - end[0])
        y = abs(start[1] - end[1])

        # catch if straight line (x or y is 0) and adjust width to be thickness of line
        if x != 0:
            width = x
        else:
            width = thickness
        if y != 0:
            height = y
        else:
            height = thickness

        width = right - left
        height = bottom - top

        new_start = (x1 - left), (y1 - top)
        new_end = (x2 - left), (y2 - top)

        # create a surface of the width and height of the line
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.line(self.image, color, new_start, new_end, thickness)
        self.rect = pygame.Rect(left, top, width, height)

        # set top left corner of rect to minimum of x and y points of line (this should guarantee top left coordinates)
        # self.rect.left = min(start[0], end[0])
        # self.rect.top = min(start[1], end[1])
        # print(self.image)
        # print(self.rect)
        self.rect.left = left
        self.rect.top = top
        super().add()


class Rectangle(GamesObject):
    def __init__(self, left: int, top: int, width: int, height: int, color):
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.rect(self.image, color, [left, top, width, height])

        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)

        super().add()


class Text(GamesObject):
    def __init__(self, left: int, top: int, text_color, text: str, text_size: int):
        super().__init__()
        self.dirty = 1
        text_color = _process_color(text_color)

        # is there a way to load text quicker?
        font = pygame.font.SysFont('Arial', text_size)

        #  self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        self.image = font.render(text, True, text_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)

        super().add()


class Image(GamesObject):
    def __init__(self, path: str, left: int, top: int, width: int, height: int):
        super().__init__()
        self.dirty = 1
        try:
            path_strs = path.split('/')
            self.image = pygame.image.load(os.path.join(*path_strs)).convert_alpha()
        except FileNotFoundError as err:
            try:
                r = requests.get(path, stream=True)

                # Check if the image was retrieved successfully
                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True

                    # Open a local file with wb ( write binary ) permission.
                    with open('temp', 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    self.image = pygame.image.load('temp').convert_alpha()
                else:
                    print('Image Couldn\'t be retreived')
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = left, top
        self.rect.width = width

        super().add()


def circle(radius: int, color: Union[str, List['str']], *args):
    '''
    Creates a circle with conditions specified by parameters.
    :param radius: int, radius of circle in pixels
    :param color: color of circle
    :param args: center of circle in x, y either as separate ints or as a tuple of ints
    :return: Circle object
    '''
    if len(args) >= 2:
        x, y = args[0], args[1]
    else:
        x, y = args[0]
    return Circle((x, y), radius, color)


def line(thickness: int, color: Union[str, List['str']], *args):
    '''
    Creates a line with conditions specified by parameters.
    :param thickness: thickness of line in pixels
    :param color: color of circle
    :param args: x and y position of start and end coordinates, either as 4 separate ints or 2 tuples
    :return:
    '''
    if len(args) > 2:
        start = args[0], args[1]
        end = args[2], args[3]
    else:
        start = args[0]
        end = args[1]
    return Line(start, end, thickness, color)


def make_text(text_color, text: str, text_size: int, *args):
    if len(args) >= 2:
        left, top = args[0], args[1]
    else:
        left, top = args[0]
    return Text(left, top, text_color, text, text_size)


def image(path: str, *args):
    '''
    Creates a Object image from file path and other parameters given
    :param path: local file path of image to upload
    :param args: in this order: left (x), top (y) coordinates, width, height of image as ints or 2 tuples
    :return: Image object
    '''
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Image(path, left, top, width, height)


class above(GamesObject):
    def __init__(self, top: GamesObject, bottom: GamesObject):
        super().__init__()
        self.dirty = 1

        x = top.rect.x
        y = top.rect.y
        width = max(top.rect.width, bottom.rect.width)
        height = top.rect.height + bottom.rect.height

        self.image = pygame.surface.Surface((width, height))
        self.image.blit(top.image, (0, 0))
        self.image.blit(bottom.image, (0, top.rect.height))

        self.rect = self.image.get_rect(center=(x, y))

        super().add()


class GamesGroup(GamesObject):
    '''
    class consisting of group of GamesObjects together to allow collective functionality
    '''

    def __init__(self, *objects: Union[GamesObject, List[GamesObject]]):
        super().__init__()
        designer.check_initialized()
        self.objects = objects
        # list of queued animation
        self.animations = []
        # flag to continue animation
        self.finished_animation = False
        self.dirty = 1
        designer.GLOBAL_DIRECTOR.add_group(self)
        self._calc_total_object()
        # self.orig_img = self.image
        super().add()

    def add_animation(self, animation: Animation):
        self.animations.append(animation)

    def _handle_animation(self):
        for animation in self.animations:
            if not self.finished_animation and self.animations:
                animation.step(self)

    def _calc_total_object(self):
        """
        Groups individual objects into one image.
        :return:
        """
        x, y = self.objects[0].rect.topleft
        w = 0
        h = 0
        for object in self.objects:
            # calculates most topleft position of all objects
            temp_x, temp_y = (object.rect.topleft)
            if (temp_x < x):
                x = temp_x
            if (temp_y < y):
                y = temp_y
            temp_w, temp_h = object.image.get_size()
            # calculates greatest width and height of all objects
            if (temp_w > w):
                w = temp_w
            if (temp_h > h):
                h = temp_h
        image = pygame.surface.Surface((w, h)).convert_alpha()
        for object in self.objects:
            # remove individual objects from collection and draw objects onto one surface
            designer.GLOBAL_DIRECTOR.all_game_objects.remove(object)
            tempx, tempy = object.rect.topleft
            tempx = tempx - x
            tempy = tempy - y
            image.blit(object.image, (tempx, tempy))
        # orient rect
        rect = image.get_rect()
        rect.x = x
        rect.y = y
        self.image = image
        self.rect = rect
        self.dirty = 1


def group(*objects: Union[GamesObject, List[GamesObject]]):
    '''
    Function to group multiple objects together.
    :param objects: collection of objects to be grouped together for collective functionality
    :return: group
    '''
    return GamesGroup(*objects)
