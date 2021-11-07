from designer import *


def create_world():
    orb = circle("black", 10)
    orb['x'] = 50
    try:
        print(orb['x scale'])
    except Exception as e:
        print(e)
    try:
        orb['flip'] = True
    except Exception as e:
        print(e)
    try:
        rectangle('hippopotamus blue', 20, 30)
    except Exception as e:
        print(e)
    try:
        circle(27, "red")
    except Exception as e:
        print(e)
    try:
        circle(5, 4)
    except Exception as e:
        print(e)
    return {
        'orb': orb,
    }

when('starting', create_world)

def update_the_world(worl):
    print(worl)

try:
    when('updated', update_the_world)
except Exception as e:
    print(e)

when('updating', update_the_world)

draw()