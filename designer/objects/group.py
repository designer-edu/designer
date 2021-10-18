import pygame
import designer
import math

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject


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
        # self._original_image = self.image
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
        image.fill((0, 0, 0, 0))
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