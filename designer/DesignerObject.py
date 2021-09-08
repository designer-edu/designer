import os
import shutil
import sys
from typing import Tuple, List

import requests

import pygame
import designer
import math

from designer.colors import _process_color


class DesignerObject(pygame.sprite.DirtySprite):
    def __init__(self):
        '''
        Creates a DesignerObject, a visual component of Designer output.
        '''
        designer.check_initialized()
        super().__init__()
        self.animations = []
        self.orig_img = None
        self.finished_animation = False

    def add(self):
        '''
        Adds self to the global state's object collection.
        :return: None
        '''
        designer.GLOBAL_DIRECTOR.add(self)
        self.orig_img = self.image.copy()

    def add_animation(self, animation):
        """
        Adds an animation to self's animations collection.

        :param animation: animation to be added
        :type animation: designer.Animation

        :return: None

        """
        self.animations.append(animation)

    def _handle_animation(self):
        '''
        Processes all animations in self's animation collection. Is continuously called in main game loop for each
        Designer Object.
        '''
        for animation in self.animations:
            animation.step(self)


class Circle(DesignerObject):
    def __init__(self, center, size, color):
        '''
        Creates a circle object on the window.

        :param center: x, y coordinates of center of circle
        :type center: Tuple[int]
        :param size: radius of circle
        :type size: int
        :param color: color of circle
        :type color: str or List[str]

        '''
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


class Ellipse(DesignerObject):
    def __init__(self, color, left, top, width, height):
        '''
        Creates an ellipse Designer Object on the window.

        :param color: color of ellipse
        :type color: str or List[str]
        :param left: x coordinate of top left corner of ellipse
        :type left: int
        :param top: y coordinate of top left corner of ellipse
        :type top: int
        :param width: width of ellipse to be drawn
        :type width: int
        :param height: height of ellipse to be drawn
        :type height: int
        '''
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((2 * width, 2 * height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.ellipse(self.image, color, (0, 0, width, height))

        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top

        super().add()


def ellipse(color, args):
    '''
    Function to make ellipse.

    :param color: color of ellipse
    :type color: str or List[str]
    :param args: left top corner of ellipse and width and height of ellipse
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Ellipse object created
    '''
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Ellipse(color, left, top, width, height)


class Arc(DesignerObject):
    def __init__(self, color, start_angle, stop_angle, thickness, left, top, width, height):
        """
        Creates an Arc Designer Object on window.

        :param color: color to draw arc
        :type color: str or List[str]
        :param start_angle: angle to start drawing arc at
        :type start_angle: int
        :param stop_angle: angle to stop drawing arc at
        :type stop_angle: int
        :param thickness: thickness of arc in pixels
        :type thickness: int
        :param left: x coordinate of top left corner of arc
        :type left: int
        :param top: y coordinate of top left corner of arc
        :type top: int
        :param width: width of arc to be drawn
        :type width: int
        :param height: height of arc to be drawn
        :type height: int
        """
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((width * 2, height * 2), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.arc(self.image, color, (0, 0, width, height), start_angle, stop_angle, width=thickness)

        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top

        super().add()


def arc(color, start_angle, stop_angle, thickness, args):
    """
    Function to make arc.

    :param color: color to draw arc
    :type color: str or List[str]
    :param start_angle: angle to start drawing arc at
    :type start_angle: int
    :param stop_angle: angle to stop drawing arc at
    :type stop_angle: int
    :param thickness: thickness of arc in pixels
    :type thickness: int
    :param args: left top corner of arc and width and height of arc
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Arc object created
    """
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Arc(color, start_angle, stop_angle, thickness, left, top, width, height)


class Line(DesignerObject):
    def __init__(self, start, end, thickness, color):
        """
        Creates Line Designer Object on window.

        :param start: starting coordinates of line
        :type start: Tuple[int]
        :param end: ending coordinates of line
        :type end: Tuple[int]
        :param thickness: thickness of line in pixels
        :type thickness: int
        :param color: color of line
        :type color: str or List[str]
        """

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

        # calculate differences between x and y coordinates of line
        x = abs(start[0] - end[0])
        y = abs(start[1] - end[1])

        width = right - left
        height = bottom - top

        new_start = (x1 - left), (y1 - top)
        new_end = (x2 - left), (y2 - top)

        # create a surface of the width and height of the line
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.line(self.image, color, new_start, new_end, thickness)
        self.rect = pygame.Rect(left, top, width, height)

        # set top left corner of rect to minimum of x and y points of line (this should guarantee top left coordinates)
        self.rect.left = left
        self.rect.top = top
        super().add()


class Rectangle(DesignerObject):
    def __init__(self, left, top, width, height, color):
        """
        Creates Rectangle Designer Object on window.

        :param left: x position of top left corner of rectangle
        :type left: int
        :param top: y position of top left corner of rectangle
        :type top: int
        :param width: width of rectangle in pixels
        :type width: int
        :param height: height of rectangle in pixels
        :type height: int
        :param color: color of rectangle
        :type color: str or List[str]
        """
        super().__init__()
        self.dirty = 1
        color = _process_color(color)

        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.rect(self.image, color, (0, 0, width, height))



        self.color = color
        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)

        super().add()


def rectangle(color, *args):
    '''
    Function to create a rectangle.

    :param color: color of rectangle
    :type color: str or List[str]
    :param args: left top corner of image and width and height of rectangle
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Rectangle object
    '''
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Rectangle(left, top, width, height, color)


class Text(DesignerObject):
    def __init__(self, left, top, text_color, text, text_size):
        """
        Creates Text Designer Object on window

        :param left: x coordinate of top left corner of text box
        :type left: int
        :param top: y coordinate of top left corner of text box
        :type top: int
        :param text_color: color of text
        :type text_color: str or List[str]
        :param text: text to be written on window
        :type text: str
        :param text_size: font size of text
        :type text_size: int
        """
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


class Shape(DesignerObject):
    def __init__(self, points, left, top, width, height, color):

        super().__init__()
        self.dirty = 1
        color = _process_color(color)


        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.polygon(self.image, color, points)

        self.rect = self.image.get_rect()
        self.rect.topleft = (left, top)


        super().add()


def shape(color, points: List[Tuple]):
    designer.check_initialized()
    max_x = 0
    max_y = 0
    new_points = []
    min_x = designer.GLOBAL_DIRECTOR.width
    min_y = designer.GLOBAL_DIRECTOR.height
    for pt in points:
        if pt[0] < min_x:
            min_x = pt[0]
        if pt[0] > max_x:
            max_x = pt[0]
        if pt[1] < min_y:
            min_y = pt[1]
        if pt[1] > max_y:
            max_y = pt[1]
        x = designer.GLOBAL_DIRECTOR.width - pt[0]
        y = designer.GLOBAL_DIRECTOR.height - pt[1]
        new_points.append((x, y))
    width = max_x - min_x
    height = max_y - min_y
    new_points = [(x - min_x, y - min_y) for x, y in points]
    return Shape(new_points, min_x, min_y, width, height, color)


class Image(DesignerObject):
    def __init__(self, path, left, top, width, height):
        """
        Creates Image Designer Object on window

        :param path: either url or local file path to image to load on screen
        :type path: str
        :param left: x position of top left corner of image
        :type left: int
        :param top: y position of top left corner of image
        :type top: int
        :param width: width of image in pixels
        :type width: int
        :param height: height of image in pixels
        :type height: int
        """
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
                    print('Image Couldn\'t be retrieved')
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = left, top
        self.rect.width = width

        super().add()


def circle(color, radius, *args):
    '''
    Function to create a circle. 

    :param color: color of circle
    :param radius: int, radius of circle in pixels
    :param args: center of circle in x, y either as separate ints or as a tuple of ints
    :return: Circle object
    '''
    if len(args) >= 2:
        x, y = args[0], args[1]
    else:
        x, y = args[0]
    return Circle((x, y), radius, color)


def line(thickness, color, *args):
    '''
    Function to create a line.

    :param thickness: thickness of line in pixels
    :type thickness: int
    :param color: color of line
    :type color: str or List[str]
    :param args: start and end coordinates of line
    :type args: two tuples (start x, start y), (end x, end y) or four ints start x, start y, end x, end y

    :return: Line object created
    '''
    if len(args) > 2:
        start = args[0], args[1]
        end = args[2], args[3]
    else:
        start = args[0]
        end = args[1]
    return Line(start, end, thickness, color)


def text(text_color, text, text_size, *args):
    if len(args) >= 2:
        left, top = args[0], args[1]
    else:
        left, top = args[0]
    return Text(left, top, text_color, text, text_size)


def image(path, *args):
    '''
    Function to create an image.

    :param path: local file path or url of image to upload
    :type path: str
    :param args: left top corner of image and width and height of image
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Image object
    '''
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    else:
        left, top = args[0]
        width, height = args[1]
    return Image(path, left, top, width, height)


class above(DesignerObject):
    def __init__(self, top, bottom):
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


class DesignerGroup(DesignerObject):
    '''
    class consisting of group of DesignerObjects together to allow collective functionality
    '''

    def __init__(self, *objects):
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

    def add_animation(self, animation):
        """
         Adds an animation to self's animations collection.

        :param animation: animation to be added
        :type animation: designer.Animation

        :return: None

        """
        self.animations.append(animation)

    def _handle_animation(self):
        '''
        Processes all animations in self's animation collection. Is continuously called in main game loop for each
        Designer Group.

        :return: None
        '''
        for animation in self.animations:
            if not self.finished_animation and self.animations:
                animation.step(self)

    def _calc_total_object(self):
        """
        Groups individual objects into one image.

        :return: None
        """
        x, y = self.objects[0].rect.topleft
        max_x, max_y = self.objects[0].rect.bottomright
        for object in self.objects:
            # calculates most topleft position of all objects
            temp_x, temp_y = (object.rect.topleft)
            if (temp_x < x):
                x = temp_x
            if (temp_y < y):
                y = temp_y
            temp_w, temp_h = object.rect.bottomright
            # calculates greatest width and height of all objects
            if (temp_w > max_x):
                max_x = temp_w
            if (temp_h > max_y):
                max_y = temp_h
        width = max_x - x
        height = max_y - y
        image = pygame.surface.Surface((width, height)).convert_alpha()
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


def group(*objects):
    '''
    Function to group multiple objects together.

    :param objects: collection of objects to be grouped together for collective functionality
    :type objects: at least one DesignerObject
    :return: Created Designer Group object
    '''
    return DesignerGroup(*objects)
