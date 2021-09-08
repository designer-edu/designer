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

size_of_house = input("Do you want to build a big or small house? Answer \"big\" or \"small\" ")
residents = input("Does anyone live in the house? Answer \"yes\" or \"no\" ")
if size_of_house.lower() == 'big':
    bottom_house = rectangle('firebrick', 300, 300, 400, 200)
    roof = shape('lightyellow', [(500, 150), (700, 300), (300, 300)])
    door = rectangle('black', 460, 350, 75, 150)
    door_handle = line(3, 'white', 470, 400, 470, 450)
    house = group(roof, bottom_house, door, door_handle)

elif size_of_house.lower() == 'small':
    bottom_house = rectangle('firebrick', 300, 300, 200, 200)
    roof = shape('lightyellow', [(400, 150), (500, 300), (300, 300)])
    door = rectangle('black', 360, 350, 75, 150)
    door_handle = line(3, 'white', 370, 400, 370, 450)
    house = group(roof, bottom_house, door, door_handle)
else:
    print("You did not provide a valid answer. No house will be drawn. ")

if residents == "yes":
    resident_head = circle('black', 20, 100, 370)
    resident_body = line(5, 'black', 100, 400, 100, 450)
    resident_left_leg = line(5, 'black', 100, 450, 75, 500)
    resident_right_leg = line(5, 'black', 100, 450, 125, 500)
    resident_arms = line(5, 'black', 75, 420, 125, 420)
    resident_person = group(resident_head, resident_body, resident_left_leg, resident_right_leg, resident_arms)
    draw(house, resident_person)
else:
    stake = line(20, 'white', 100, 300, 100, 500)
    sign = rectangle('white', 100, 300, 100, 70)
    for_sale_text = text("red", "for sale", 25, 100, 300)
    for_sale_sign = group(stake, sign, for_sale_text)
    draw(house, for_sale_sign)


