import os
import io
from urllib.request import urlopen, Request
import pygame


class MusicModule:
    _USER_AGENT = "Designer Game Library for Python"

    def __init__(self):
        self._filename = None
        self._volume = 1.0
        # pygame.mixer.music.set_endevent
        # Use this to get events about music!

    def _load_song(self):
        try:
            path_strs = self._filename.split('/')
            fixed_paths = os.path.join(*path_strs)
            if os.path.exists(fixed_paths):
                pygame.mixer.music.load(self._filename)
            else:
                raise FileNotFoundError(fixed_paths)
        except FileNotFoundError as err:
            try:
                req = Request(self._filename, headers={'User-Agent': self._USER_AGENT})
                with urlopen(req) as opened_song:
                    song_str = opened_song.read()
                    song_file = io.BytesIO(song_str)
                    pygame.mixer.music.load(song_file)
            except:
                if self._filename.startswith('https://') or self._filename.startswith('http://'):
                    raise ValueError(f"Unexpected error while playing url: {self._filename!r}")
                raise ValueError(f"Unexpected error while playing song from filename: {self._filename!r}")

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self._load_song()
        self.play()

    @property
    def playing(self):
        return pygame.mixer.music.get_busy()

    @property
    def volume(self):
        return pygame.mixer.music.get_volume()

    @volume.setter
    def volume(self, value):
        pygame.mixer.music.set_volume(value)

    def play(self, loop=True):
        pygame.mixer.music.play(loops=loop)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def rewind(self):
        pygame.mixer.music.rewind()

    def set_time_position(self, time):
        pygame.mixer.music.set_pos(time)

    def get_time_position(self):
        return pygame.mixer.music.get_pos()