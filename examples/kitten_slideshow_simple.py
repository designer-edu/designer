from designer import *


URLS = [
    "https://placekitten.com/300/300",
    "https://placekitten.com/300/301",
    "https://placekitten.com/300/302",
    "https://placekitten.com/300/303",
]

slideshow = image(URLS[0])
sequence_animation(slideshow, 'filename', URLS, 5, loop=True)

draw(slideshow)