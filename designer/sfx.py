import pygame
import io
import os
from urllib.request import urlopen, Request


class SfxModule:
    _USER_AGENT = "Designer Game Library for Python"

    def __init__(self):
        pass

    def play(self, path, volume=1.0):
        sfx = self._load_sfx(path)
        sfx.set_volume(volume)
        sfx.play()
        return sfx

    def _load_sfx(self, filename):
        try:
            path_strs = filename.split('/')
            fixed_paths = os.path.join(*path_strs)
            if os.path.exists(fixed_paths):
                return pygame.mixer.Sound(fixed_paths)
            else:
                raise FileNotFoundError(fixed_paths)
        except FileNotFoundError as err:
            try:
                req = Request(filename, headers={'User-Agent': self._USER_AGENT})
                with urlopen(req) as opened_sfx:
                    sfx_str = opened_sfx.read()
                    sfx_file = io.BytesIO(sfx_str)
                    return pygame.mixer.Sound(sfx_file)
            except:
                if filename.startswith('https://') or filename.startswith('http://'):
                    raise ValueError(f"Unexpected error while playing url: {filename!r}")
                raise ValueError(f"Unexpected error while playing sound from filename: {filename!r}")

