from designer import *

def house():
  pass

def empty_lot():
  pass

def create_world():
  return {
    'house': house(),
    'available': True
  }

def change_house(world):
  if world['available']:
    world['house'] = empty_lot()
  else:
    world['available'] = house()
  world['available'] = not world['available']

when('starting', create_world)
when('clicking', change_house)

draw()
