from designer import *


@updating
def chase_mouse(picture: DesignerObject):
    point_towards_mouse(picture)


def grow_emoji(picture: DesignerObject):
    grow(picture, get_scale(picture)+.01)


def shrink_if_clicked(picture: DesignerObject):
    if colliding_with_mouse(picture):
        set_scale(picture, get_scale(picture)/2)


when('clicking', shrink_if_clicked)
when('updating', grow_emoji)
start(emoji('➡'))
