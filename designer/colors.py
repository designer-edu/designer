import importlib
import json
import os
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'data/colors.json'), encoding='utf-8') as f:
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
