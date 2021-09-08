import math
from designer import DesignerObject
import pygame
import designer
import random


class Animation:
    def __init__(self, speed, direction):
        self.speed = speed
        self.direction = direction

    def start(self):
        pass

    def is_finished(self):
        return False


class GlideAnimation(Animation):
    def __init__(self, speed, direction):
        """
        Initializer of animations that glide across the screen.
        Calls initializer of Animations, parent  class.

        :param speed: Pixels to move per second
        :type speed: int
        :param direction: Degrees at which to move
        :type direction: int
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

    def step(self, object):
        '''
        Handles glide for each step of the game state.

        :param object: Object to move
        :type object: DesignerObject or DesignerGroup
        :return: None
        '''
        if isinstance(object, DesignerObject):
            objects = [object]
        elif isinstance(object, designer.DesignerGroup):
            objects = [object]
        for temp_object in objects:
            if (
                    temp_object.rect.right) < designer.GLOBAL_DIRECTOR.width and temp_object.rect.x > 0 and temp_object.rect.top < designer.GLOBAL_DIRECTOR.height and temp_object.rect.y > 0:
                if not object.finished_animation:
                    temp_object.rect.x += (self.speed * self.x)
                    temp_object.rect.y += (self.speed * self.y)
                    temp_object.dirty = 1
            else:
                object.finished_animation = True


class JitterAnimation(Animation):
    def __init__(self, direction):
        self.direction = direction

    def step(self, object):
        '''
              Handles glide for each step of the game state.

                :param object: Object to move
                :type object: DesignerObject or DesignerGroup
                :return: None
                '''
        if isinstance(object, DesignerObject):
            objects = [object]
        elif isinstance(object, designer.DesignerGroup):
            objects = object.objects
            x_dir = random.randint(-self.direction, self.direction)
            y_dir = random.randint(-self.direction, self.direction)
            for object in objects:
                object.rect.x += x_dir
                object.rect.y += y_dir
                object.dirty = 1


class RotateAnimation(Animation):
    def __init__(self, speed, direction, angle_limit, pos):
        self.speed = speed
        self.angle = 1
        self.angle_limit = angle_limit
        self.pos = pos
        self.total = 0
        super().__init__(speed, direction)

    def step(self, obj):
        '''
        Handles rotation for each step of the game state.

        :param obj: Object to be moved
        :type obj: DesignerObject or DesignerGroup
        :return: None
        '''
        if isinstance(obj, DesignerObject):
            objects = [obj]
        elif isinstance(obj, designer.DesignerGroup):
            objects = obj.objects
        for obj in objects:
            if self.total < self.angle_limit:
                self.total = self.total + (self.speed * self.angle)
                obj.image = pygame.transform.rotate(obj.orig_img, self.total)
                obj.rect = obj.image.get_rect(center=obj.orig_img.get_rect(center=(obj.rect.center)).center)

                obj.dirty = 1


def glide_around(*objects, speed):
    '''
    Moves object around at random.

    :param objects: Object to move around
    :type objects: DesignerObject or DesignerGroup
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    '''
    for object in objects:
        object.add_animation(JitterAnimation(speed, 0))


def glide_right(obj, speed):
    '''
       Moves object to the right of the window.

       :param obj: Object to move
       :type obj: DesignerObject or DesignerGroup
       :param speed: Pixels to move per second
       :type speed: int
       :return: None
       '''
    obj.add_animation(GlideAnimation(speed, 0))


def glide_left(obj, speed):
    '''
           Moves object to the left of the window.

           :param obj: Object to move
           :type obj: DesignerObject
           :param speed: Pixels to move per second
           :type speed: int
           :return: None
           '''
    obj.add_animation(GlideAnimation(speed, 180))


def glide_up(obj, speed):
    '''
           Moves object up on the window.

           :param obj: Object to move
           :type obj: DesignerObject or DesignerGroup
           :param speed: Pixels to move per second
           :type speed: int
           :return: None
     '''
    obj.add_animation(GlideAnimation(speed, 90))


def glide_down(obj, speed):
    '''
            Moves object down on the window!

            :param obj: Object to move
            :type obj: DesignerObject or DesignerGroup
            :param speed: Pixels to move per second
            :type speed: int
            :return: None
         '''
    obj.add_animation((GlideAnimation(speed, 270)))


def glide_in_degrees(obj, direction, speed):
    '''
    Moves object a given number of degrees in that direction

    :param obj: Object to move
    :type obj: DesignerObject or DesignerGroup
    :param direction: Direction in degrees counterclockwise for object to move
    :type direction: int
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    '''
    obj.add_animation((GlideAnimation(speed, direction)))


def rotate(obj, angle_limit, speed):
    '''
    Rotates object in place for a given number of degrees

    :param obj: Object to move
    :type obj: DesignerObject or DesignerGroup
    :param angle_limit: Degrees to rotate object
    :type angle_limit: int
    :param speed: Pixels to move per second
    :type speed: int
    :return: None
    '''
    if isinstance(obj, DesignerObject.DesignerObject):
        obj.add_animation(RotateAnimation(speed, 0, angle_limit, obj.rect.topleft))
    if isinstance(obj, DesignerObject.DesignerGroup):
        for temp_object in obj.objects:
            temp_object.add_animation(RotateAnimation(speed, 0, angle_limit, temp_object.rect.topleft))
