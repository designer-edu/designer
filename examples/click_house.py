from designer import *


def house():
    return image(
        "https://cdn.iconscout.com/icon/free/png-256/house-home-building-infrastructure-real-estate-resident-emoj"
        "-symbol-1-30743.png")


def empty_lot():
    return image(
        "https://media.istockphoto.com/vectors/pleasant-valley-vector-id165909426?k=20&m=165909426&s=612x612&w=0&h"
        "=LFYvcBqR-uKy_fGexLjgiTsB-BsJ3VoVWhGVuBlq6v8=")


def create_world():
    return {
        'house': house(),
        'available': True
    }


def change_house(world):
    print("CLICKED", world)
    world['house'].kill()
    if world['available']:
        world['house'] = empty_lot()
    else:
        world['house'] = house()
    world['available'] = not world['available']


when('starting', create_world)
when('clicking', change_house)

draw()
