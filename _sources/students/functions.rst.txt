Designer Object Function Quick List
###################################

========================================= ==============================================================================
  Position
========================================= ==============================================================================
 `move_forward(object, amount)`            Move `amount` in object's current `angle`, updating the `x` and `y`
 `move_forward(object, amount, angle)`     Move `amount` in `angle` degrees, updating the `x` and `y`
 `move_backward(object, amount)`           Move `amount` away from object's current `angle`, updating the `x` and `y`
 `move_backward(object, amount, angle)`    Move `amount` away from `angle` degrees, updating the `x` and `y`
 `move_to_xy(object, x, y)`                Set the object's `x` and `y` to the given pixel locations
 `move_to(object, other_object)`           Set the first object's `x` and `y` to the other object's location
 `move_to_mouse(object)`                   Set the object's `x` and `y` to the current mouse position
 `change_x(object, amount)`                Increase the object's `x` location by the `amount`
 `change_y(object, amount)`                Increase the object's `y` location by the `amount`
 `set_x(object, new_x)`                    Set the object's `x` coordinate to be `new_x`
 `set_y(object, new_y)`                    Set the object's `y` coordinate to be `new_y`
 `get_x(object)`                           Get the object's `x` coordinate
 `get_y(object)`                           Get the object's `y` coordinate
========================================= ==============================================================================

========================================= ==============================================================================
 Angle
========================================= ==============================================================================
 `turn_right(object, amount)`              Decrease the object's current `angle` by `amount` degrees
 `turn_left(object, amount)`               Increase the object's current `angle` by `amount` degrees
 `point_in_direction(object, angle)`       Set the object's rotation to the given `angle`
 `point_towards(object, other_object)`     Change the first object's `angle` to be oriented towards the other object's position
 `point_towards_mouse(object)`             Change the first object's `angle` to be oriented towards the location of the mouse cursor
 `get_angle(object)`                       Get the object's `angle` in degrees that it is oriented towards
========================================= ==============================================================================

========================================= ==============================================================================
 Size
========================================= ==============================================================================
 `set_scale(object, scale)`               Set the object's `scale` to a float relative to `1.0`
 `grow(object, amount)`                   Increase the object's `scale` by the decimal `amount`
 `shrink(object, amount)`                 Decrease the object's `scale` by the decimal `amount`
 `grow_x(object, amount)`                 Increase the object's horizontal `scale_x` by the decimal `amount`
 `grow_y(object, amount)`                 Increase the object's vertical `scale_y` by the decimal `amount`
 `set_scale_x(object, new_scale_x)`       Set the object's horizontal `scale_x` to the `new_scale_x`
 `set_scale_y(object, new_scale_y)`       Set the object's horizontal `scale_y` to the `new_scale_y`
 `get_scale(object)`                      Get the object's `scale`
 `get_scale_x(object)`                    Get the object's horizontal `scale_x`
 `get_scale_y(object)`                    Get the object's vertical `scale_y`
========================================= ==============================================================================

========================================= ==============================================================================
 Visibility
========================================= ==============================================================================
 `show(object)`                           Makes the object `visible`
 `hide(object)`                           Makes the object not `visible` (aka hidden)
 `set_visible(object, status)`            Sets the object to be `visible` or not based on `status`
 `get_visible(object)`                    Get whether or not the object is `visible`
========================================= ==============================================================================

========================================= ==============================================================================
 Flipping
========================================= ==============================================================================
 `flip_x(object)`                         Inverts whether the object is flipped horizontally
 `flip_y(object)`                         Inverts whether the object is flipped vertically
 `set_flip_x(object, new_flip_x)`         Sets the object to be flipped horizontally based on `new_flip_x`
 `set_flip_y(object, new_flip_y)`         Sets the object to be flipped vertically based on `new_flip_y`
 `get_flip_x(object)`                     Get whether or not the object is flipped horizontally
 `get_flip_y(object)`                     Get whether or not the object is flipped vertically
========================================= ==============================================================================



Full Function Reference
-----------------------

.. _move_forward:

.. py:function:: move_forward(object, amount)
                 move_forward(object, amount, angle)

    Move the given `object` forward by `amount`, either in its current rotation
    `angle` attribute or the given `angle`. This changes the `x` and `y` attribute
    of the Designer Object, in addition to returning the value.

    .. code-block:: python

        from designer import *
        # Black rectangle of size 100x100
        # Defaults to angle=0 (pointing to the right)
        box = rectangle("black", 100, 100)

        # Move the box to the right 50 pixels
        move_forward(box, 50)

        # Move the box upwards 20 pixels
        move_forward(box, 20, 90)

        # Move the box down and left, both 10 pixels, by chaining
        move_forward(move_forward(box, 10, 270), 10, 180)

    :param object: A Designer Object
    :type object: DesignerObject
    :param amount: The number of pixels to move
    :type amount: int
    :param angle: The direction (in degrees) to move in; defaults to the object's current `angle` attribute (which defaults to 0).
    :type angle: int

    :return: The Designer Object that was passed in.
    :rtype: DesignerObject