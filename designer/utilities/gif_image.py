"""GIFImage by Matthew Roe"""

from PIL import Image
import pygame
from pygame.locals import *

import time

from designer.utilities.animation import Animation
from designer.utilities.easings import Iterate


class GifImage(Animation):
    def __init__(self, filename):
        self.filename = filename
        self.duration = .1
        self.total_duration = 0
        self.image = Image.open(filename)
        self.frames = []
        self.get_frames()

        # Handle per-frame durations
        print(len(self.frames))
        super().__init__('image', Iterate(self.frames), self.total_duration, True, None, True)

    def get_rect(self):
        return pygame.rect.Rect((0,0), self.image.size)

    def get_frames(self):
        image = self.image

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell()+1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    self.duration = image.info["duration"]
                except:
                    self.duration = 100

                self.duration *= .001 *10#convert to milliseconds!
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i+3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                data = image.convert("RGBA").tobytes()
                pi = pygame.image.fromstring(data, image.size, "RGBA")#image.mode)
                #pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self.frames:
                        pi2.blit(i[0], (0,0))
                #pi2.fill((255, 255, 0))
                pi2.blit(pi, (0, 0))
                #pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

                #self.frames.append([pi2, self.duration])
                self.total_duration += self.duration
                self.frames.append(pi2)
                image.seek(image.tell()+1)
        except EOFError:
            pass


    def get_height(self):
        return self.image.size[1]

    def get_width(self):
        return self.image.size[0]

    def get_size(self):
        return self.image.size

    def length(self):
        return len(self.frames)
