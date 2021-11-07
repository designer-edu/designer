import difflib
from designer.utilities.vector import Vec2D


def is_iterable_of_points(value):
    try:
        len(value)
        return all(is_point(v) for v in value)
    except:
        return False


def is_non_empty(value):
    try:
        value[0]
        return True
    except:
        return False

def at_least_three(value):
    try:
        return len(value) >= 3
    except:
        return False

def is_non_empty_iterable_of_points(value):
    return is_iterable_of_points(value) and is_non_empty(value)


def is_point(value):
    if isinstance(value, dict):
        return 'x' in value and 'y' in value and are_numbers(value['x'], value['y'])
    elif isinstance(value, (tuple, list)):
        return len(value) == 2 and are_numbers(value[0], value[1])
    elif isinstance(value, Vec2D):
        return True
    else:
        return hasattr(value, 'x') and hasattr(value, 'y') and are_numbers(value.x, value.y)


def are_numbers(*values):
    return all(isinstance(v, (int, float)) for v in values)


def make_suggestions(value, known_values, cutoff=.6):
    return ", ".join(map(repr, difflib.get_close_matches(value, known_values, cutoff=cutoff)))
