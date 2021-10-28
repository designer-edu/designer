import designer
import os


def get_designer_path():
    """ Get the path of the Designer directory. """
    return os.path.dirname(designer.__file__) + '/'


def get_resource(filename: str):
    """
    Get the given resource by its filename
    """
    return os.path.join(os.path.dirname(designer.__file__), 'data', filename)
