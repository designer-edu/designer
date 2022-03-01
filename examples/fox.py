from designer import *

set_window_image('https://bit.ly/3zFlzuT')

# Moon and title
title = text("green", "Goodnight Moon", 30, 200, 100)
moon = grow(emoji('🌕', 600, 100), 5)

# Build the House components
bottom_house = rectangle('firebrick', 200, 200)
door = change_y(rectangle('black', 75, 150), 25)
door_handle = change_xy(rectangle('white', 3, 50), -25, 15)
roof = change_y(shape('lightyellow', 0, 0, 100, 150, -100, 150), -175)
# Group them together into a single, moveable object
house = group(roof, bottom_house, door, door_handle)
move_to_xy(house, 100, 325)

# Draw everything
draw(house, title, moon)

