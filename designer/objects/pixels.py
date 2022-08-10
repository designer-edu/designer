try:
    from collections import UserList
except:
    UserList = list


class PixelsGrid:
    def __init__(self, data=None):
        self.data = data

    def __getitem__(self, item):
        if isinstance(item, (int, float)):
            item = int(item)
            return self.data[item]
        elif isinstance(item, tuple):
            return self.data[item]

    def __setitem__(self, item, value):
        pass


def get_pixels2d(designer_object):
    if not designer_object or not designer_object._internal_image._surf:
        return []
    surface = designer_object._internal_image._surf
    pixels = [[surface.get_at((x, y))
               for x in range(surface.get_width())]
              for y in range(surface.get_height())]
    return pixels


def get_pixels(designer_object):
    if not designer_object or not designer_object._transform_image:
        return []
    surface = designer_object._transform_image
    w, h = surface.get_width(), surface.get_height()
    pixels = [surface.get_at((x, y))
              for y in range(h)
              for x in range(w)]
    return PixelsList(pixels, w, h)


class PixelsList(UserList):
    def __init__(self, data, w, h):
        super().__init__(data)
        self.width = w
        self.height = h
