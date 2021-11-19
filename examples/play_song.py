from designer import *

play_music('awesomeness-mrpoly.ogg', loop=True)

def click():
    if is_music_playing():
        pause_music()
    else:
        continue_music()

when('clicking', click)

start()