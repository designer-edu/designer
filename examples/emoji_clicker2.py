from designer import *

def grow_emoji(picture: DesignerObject):
    growth_rate = get_emoji_growth(picture)
    change_scale(picture, growth_rate)


def get_emoji_growth(picture: DesignerObject):
    if picture.name == "dragon":
        return .1
    else:
        return .02


def shrink_emoji(picture: DesignerObject):
    if colliding_with_mouse(picture):
        change_scale(picture, -.5)


def check_emoji(picture: DesignerObject):
    if get_scale_x(picture) > 8:
        picture.name = "cross mark"
        pause()


def advance_emoji(picture: DesignerObject):
    if picture.name == "banana":
        picture.name = "dragon"
    elif picture.name == "dragon":
        picture.name = "red apple"
    elif picture.name == "red apple":
        picture.name = "green apple"
    else:
        picture.name = "banana"


def change_emoji(picture: DesignerObject, key: str):
    if key == "right":
        advance_emoji(picture)


when('updating', grow_emoji)
when('clicking', shrink_emoji)
when('updating', check_emoji)
when('typing', change_emoji)
draw(emoji("dog face"))
