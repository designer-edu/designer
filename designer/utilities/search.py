from designer.objects.designer_object import DesignerObject


def _detect_objects_recursively(data):
    """ Recursively detects any references to DesignerObjects,
     and returns them as a flattened list. """
    if isinstance(data, (list, set, tuple, frozenset)):
        result = []
        for item in data:
            result.extend(_detect_objects_recursively(item))
        return result
    elif isinstance(data, dict):
        result = []
        for key, value in data.items():
            result.extend(_detect_objects_recursively(key))
            result.extend(_detect_objects_recursively(value))
        return result
    elif isinstance(data, DesignerObject):
        return [data]
    else:
        return []