import requests
import pygame

import sys
import os
import shutil

from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage
from designer.utilities.vector import Vec2D
from designer.utilities.surfaces import DesignerSurface

class Image(DesignerObject):
    def __init__(self, path, left, top, width, height, anchor):
        """
        Creates Image Designer Object on window

        :param path: either url or local file path to image to load on screen
        :type path: str
        :param left: x position of top left corner of image
        :type left: int
        :param top: y position of top left corner of image
        :type top: int
        :param width: width of image in pixels
        :type width: int
        :param height: height of image in pixels
        :type height: int
        """
        super().__init__()

        try:
            path_strs = path.split('/')
            self.internal_image = InternalImage(os.path.join(*path_strs))
        except FileNotFoundError as err:
            try:
                r = requests.get(path, stream=True)

                # Check if the image was retrieved successfully
                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True

                    # Open a local file with wb ( write binary ) permission.
                    with open('temp', 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    # TODO: Do this without a temp file
                    self.internal_image = InternalImage('temp')
                else:
                    print('Image Couldn\'t be retrieved')
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

        #width = width if width is not None else self.image.get_width()
        #height = height if height is not None else self.image.get_height()
        left = left if left is not None else get_width()/2
        top = top if top is not None else get_height()/2
        # get_width()/2, get_height()/2
        self.pos = (left, top)
        self.anchor = anchor


def image(path, *args, anchor='center'):
    """
    Function to create an image.

    :param path: local file path or url of image to upload
    :type path: str
    :param args: left top corner of image and width and height of image
    :type args: two Tuples (left, top), (width, height) or four ints left, top, width, height
    :return: Image object
    """
    if len(args) > 2:
        left, top = args[0], args[1]
        width, height = args[2], args[3]
    elif len(args) == 1:
        left, top = args[0]
        width, height = args[1]
    else:
        left, top = None, None
        width, height = None, None
    return Image(path, left, top, width, height, anchor)