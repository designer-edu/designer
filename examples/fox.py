from designer import *
from designer import spin

background_fox = background_image('https://bit.ly/3zFlzuT')

#roof = shape('lightyellow', (100, 150), (200, 300), (0, 300))
#bottom_house = rectangle('firebrick', 0, 300, 200, 200)
#door = rectangle('black', 60, 350, 75, 150)
#door_handle = line('white',3, 70, 400, 70, 450)
#house = group(roof, bottom_house, door, door_handle)

house = above(shape('lightyellow', (0, 0), (100, 150), (-100, 150)),
              rectangle('firebrick', 100, 200))
#spin(house, 5)

#box = rectangle('firebrick', 100, 100)
#spin(box, 5)

gn_text = text("green", "Goodnight Moon", 30, 200, 100)
moon = circle('lightgray', 75, 600, 100)

draw(background_fox, house, gn_text, moon)

