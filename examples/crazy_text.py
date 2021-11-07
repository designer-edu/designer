from designer import *

def write_text():
    return {
        'text': text('blue', "Hello World!", 40),
        'vibing': True
    }

def spin_text(world):
    world['text']['angle'] += .1

def vibe_text(world):
    if world['vibing']:
        if world['text']['text_size'] < 7:
            world['vibing'] = False
        else:
            world['text']['text_size'] -= 1
    else:
        if world['text']['text_size'] > 80:
            world['vibing'] = True
        else:
            world['text']['text_size'] += 1

when('starting', write_text)
when('updating', spin_text)
when('updating', vibe_text)
draw()
