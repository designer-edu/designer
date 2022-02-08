# Example program to create a picture book
from designer import *

# Load a background image
set_background_image('https://i.imgur.com/5S2Bi4Y.png')

# Construct the house
wall = rectangle('firebrick', 200, 200, 0, 300, )
door = rectangle('black', 75, 150, 60, 350)
handle = line('white', 70, 400, 70, 450, 3)
# Can make a `shape` with an offset
# roof = shape('lightyellow',
#              [(100, 150), (200, 300), (0, 300)],
#              x=0, y=150)
# Or just use `lines`
roof = lines('lightyellow',
             [(100, 150), (200, 300), (0, 300)])

house = group(wall, door, handle, roof)

# Text and the moon
title = text('green', "Goodnight Moon", 30, 150, 50)
moon = circle('lightgray', 75, 500, 100)

# Comparable to `print`, make images appear
draw(house, title, moon)