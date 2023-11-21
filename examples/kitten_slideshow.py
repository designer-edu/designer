from designer import *
from dataclasses import dataclass

@dataclass
class World:
    slideshow: DesignerObject

URLS = [
    "https://placekitten.com/300/300",
    "https://placekitten.com/300/301",
    "https://placekitten.com/300/302",
    "https://placekitten.com/300/303",
]

def create_world() -> World:
    """ Create the world """
    slideshow = image(URLS[0])
    sequence_animation(slideshow, 'filename', URLS, 5, loop=True)
    return World(slideshow)


when('starting', create_world)
start()