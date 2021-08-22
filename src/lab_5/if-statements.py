from designer import *


def handle_color(color: str):
    if color.lower() == "blue":
        color = 'lightblue'
    elif color.lower() == "orange":
        color = 'orange'
    elif color.lower() == 'green':
        color = 'lightgreen'
    else:
        print("You did not enter an appropriate color. A color will be chosen for you. ")
        color = 'purple'
    return color


def handle_number(num_str: str):
    if num_str.isnumeric():
        num = int(num_str)
    if num <= 10:
        if num % 2 == 0:
            color = 'lightblue'
        else:
            color = 'lightgreen'
    else:
        print("You did not enter a number between 0 and 10. A number will be chosen for you. ")
        color = 'lavender'
    return color

'''
back_color = input("What is your favorite color? Blue, orange, or green. ")
back_color = handle_color(back_color)
set_window_color(back_color)
'''

number = input("What is your favorite number from 0 to 10? ")
back_color = handle_number(number)
set_window_color(back_color)

draw_house = input("Do you want to build a house? ")
if draw_house.lower() == 'yes':
    roof = shape('lightyellow', [(400, 150), (500, 300), (300, 300)])
    bottom_house = rectangle('firebrick', 300, 300, 200, 200)
    door = rectangle('black', 360, 350, 75, 150)
    door_handle = line(3, 'white', 370, 400, 370, 450)
    house = group(roof, bottom_house, door, door_handle)
else:
    text('black', 'Empty lot!', 20, 350, 300)

draw()
