import difflib
import importlib
import json
import os
import re
from os import path

from designer.utilities.argument_checks import make_suggestions

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'data/colors.json'), encoding='utf-8') as f:
    colors = json.load(f)
    f.close()


def hex_to_rgb(hx, hsl=False):
    """
    Converts a HEX code into RGB or HSL.
    All credit goes to here: https://stackoverflow.com/a/62083599/1718155
    CC BY-SA 4.0

    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values.
    Raise:
        ValueError: If given value is not a valid HEX code.
    """
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i]*2, 16) / div if div else
                         int(hx[i]*2, 16) for i in (1, 2, 3))
        return tuple(int(hx[i:i+2], 16) / div if div else
                     int(hx[i:i+2], 16) for i in (1, 3, 5))
    raise ValueError(f'"{hx}" is not a valid HEX code. Should be something like "#FFB6C1".')


def _process_color(color) -> 'List[int]':
    """
    Converts either a color string (e.g., 'orange') into a color triplet (list of 3 numbers).
    If a color triplet is passed in, it is returned unmodified.

    :param color:
    :return:
    """
    if isinstance(color, str):
        if color and color[0] == '#':
            return hex_to_rgb(color)
        elif color not in colors:
            suggestions = make_suggestions(color, colors.keys(), cutoff=.3)
            if suggestions:
                raise ValueError(f"Unknown color {color!r}. Perhaps you meant one of these? {suggestions}")
            else:
                raise ValueError(f"Unknown color {color!r}. You should check the documentation!")
        return colors[color]
    if isinstance(color, int):
        raise ValueError(f"An integer ({color}) was given as the color value. The color should be a string ('red') or three numbers in a list.")
    else:
        return color
