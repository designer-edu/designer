from designer import *

background_fox = image('https://bit.ly/3zFlzuT', 0, 0, 800, 600)

roof = shape('lightyellow', [(100, 150), (200, 300), (0, 300)])
bottom_house = rectangle('firebrick', 0, 300, 200, 200)
door = rectangle('black', 60, 350, 75, 150)
door_handle = line('white',3, 70, 400, 70, 450)
house = group(roof, bottom_house, door, door_handle)

gn_text = text('green', "Goodnight Moon", 30, 50, 50)
moon = circle('lightgray', 75, 500, 100)

draw(background_fox, house, gn_text, moon)

