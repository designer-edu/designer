import pygame
import designer


class DesignerObject(pygame.sprite.DirtySprite):
    def __init__(self):
        '''
        Creates a DesignerObject, a visual component of Designer output.
        '''
        designer.check_initialized()
        super().__init__()
        self.animations = []
        self._original_image = None
        self.finished_animation = False
        self.angle = 0
        self.scale = 1

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'angle' and self._original_image:
            self.image = pygame.transform.rotate(self._original_image, self.angle)
            self.rect = self.image.get_rect(center=self._original_image.get_rect(center=(self.rect.center)).center)
            self.dirty = 1
        elif name == 'scale' and self._original_image:
            self._rescale(int(self.width*self.scale), int(self.height*self.scale))
            self.dirty = 1

    def __getattr__(self, item):
        if item in ('width',):
            return self.rect.width
        elif item in ('height',):
            return self.rect.height
        else:
            return super().__getattr__(item)

    def __getitem__(self, item):
        if item in ('x', 'X', 'left'):
            return self.rect.x
        elif item in ('y', 'Y', 'top'):
            return self.rect.y
        elif item in ('width',):
            return self.rect.width
        elif item in ('height',):
            return self.rect.height
        elif item in ('angle', 'rotation', 'rotate'):
            return self.angle
        elif item in ('scale',):
            return self.scale
        else:
            return self.__getattribute__(item)

    def __setitem__(self, key, value):
        if key in ('x', 'X', 'left'):
            self.rect.x = value
            self.dirty = 1
        elif key in ('y', 'Y', 'top'):
            self.rect.y = value
            self.dirty = 1
        elif key in ('angle', 'rotation', 'rotate'):
            self.angle = value
        elif key in ('scale',):
            self.scale = value
        else:
            self.__setattr__(key, value)

    def add(self):
        '''
        Adds self to the global state's object collection.
        :return: None
        '''
        designer.GLOBAL_DIRECTOR.add(self)
        self._original_image = self.image.copy()

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

    def _rescale(self, new_width, new_height):
        self.rect.width = new_width
        self.rect.height = new_height