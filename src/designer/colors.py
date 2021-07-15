import json
import os

basepath = os.path.dirname(__file__)
f = open(os.path.join(basepath,'colors.json'))
colors = json.load(f)
f.close()

def _process_color(color) -> 'List[int]':
    """
    Converts either a color string (e.g., 'orange') into a color triplet (list of 3 numbers).
    If a color triplet is passed in, it is returned unmodified.

    :param color:
    :return:
    """
    if isinstance(color, str):
        return colors[color]
    else:
        return color