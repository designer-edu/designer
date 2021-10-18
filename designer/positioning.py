import pygame

from designer.objects.designer_object import DesignerObject


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
