from designer import *


def spin(w, d, event):
    #print(event)
    w['box']['angle'] += 1


when('updating', spin)
start({"box": rectangle("orange", 30, 30)})
