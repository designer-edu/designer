from designer.colors import _process_color
from designer.helpers import get_width, get_height
from designer.objects.designer_object import DesignerObject
from designer.core.internal_image import InternalImage


class Ellipse(DesignerObject):
    DEFAULT_BORDER_WIDTH = 1

    def __init__(self, left, top, width, height, anchor, color, border):
        '''
        Creates an ellipse Designer Object on the window.

        :param left: x coordinate of top left corner of ellipse
        :type left: int
        :param top: y coordinate of top left corner of ellipse
        :type top: int
        :param width: width of ellipse to be drawn
        :type width: int
        :param height: height of ellipse to be drawn
        :type height: int
        :param anchor: the anchor to draw the circle at
        :type anchor: str
        :param color: color of ellipse
        :type color: str or List[str]
        :param border: the width of the circle's line (0 is used for a filled circle)
        :type border: int
        '''
        super().__init__()
        color = _process_color(color)
        self.internal_image = InternalImage(size=(width, height))
        self.internal_image.draw_ellipse(color, (0, 0, width, height), border)

        left = left if left is not None else get_width() / 2 - self.rect.width / 2
        top = top if top is not None else get_height() / 2 - self.rect.height / 2

        self.pos = (left, top)
        self.anchor = anchor
        self.color = color
        self.border = border


def ellipse(color, x, y, width=None, height=None, anchor='center', border=None, filled=True):
    '''
    Function to make an ellipse.

    :param color: color of ellipse
    :type color: str or List[str]
    :return: Ellipse object created
    '''
    if width is None and height is None:
        if isinstance(x, (int, float)):
            width, height = x, y
        else:
            width, height = y
            x, y = x
    if filled is True:
        border = 0
    elif filled is False:
        border = border or Ellipse.DEFAULT_BORDER_WIDTH
    elif border is None:
        border = Ellipse.DEFAULT_BORDER_WIDTH
    return Ellipse(x, y, width, height, anchor, color, border)
