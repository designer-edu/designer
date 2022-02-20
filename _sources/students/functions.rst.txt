.. _quicklist:

Designer Functions Quick List
#############################

Creating objects
----------------

====================================================================== =================================================
 :ref:`Images<image>`
====================================================================== =================================================
 `image(path)`
 `image(path, x, y)`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Built-in Emojis<emoji>`
====================================================================== =================================================
 `emoji(name)`
 `emoji(name, x, y)`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Text<text>`
====================================================================== =================================================
 `text(color, text)`
 `text(color, text, size)`
 `text(color, text, size, x, y)`
 `text(color, text, size, x, y, font_name="Arial")`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Rectangles<rectangle>`
====================================================================== =================================================
 `rectangle(color, width, height)`
 `rectangle(color, width, height, x, y)`
 `rectangle(color, width, height, x, y, border, anchor)`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Circles<circle>`
====================================================================== =================================================
 `circle(color, radius)`
 `circle(color, radius, x, y)`
 `circle(color, radius, x, y, border, anchor)`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Ellipses<ellipse>`
====================================================================== =================================================
 `ellipse(color, width, height)`
 `ellipse(color, width, height, x, y)`
 `ellipse(color, width, height, x, y, border, anchor)`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Line between two points<line>`
====================================================================== =================================================
 `line(color, start_x, start_y, end_x, end_y)`
 `line(color, start_x, start_y, end_x, end_y, thickness)`
====================================================================== =================================================

========================================================================================== =================================================
 :ref:`Arc between two points<arc>`
========================================================================================== =================================================
 `arc(color, start_angle, stop_angle, width, height)`
 `arc(color, start_angle, stop_angle, width, height, x, y)`
 `arc(color, start_angle, stop_angle, width, height, x, y, thickness=1, anchor='center')`
========================================================================================== =================================================

====================================================================== =================================================
 :ref:`Shape<shape>`
====================================================================== =================================================
 `shape(color, x1, y1, x2, y2, x3, y3, ...)`
 `shape(color, points)`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Connected Lines<lines>`
====================================================================== =================================================
 `lines(color, x1, y1, x2, y2, x3, y3, ...)`
 `lines(color, points)`
====================================================================== =================================================

====================================================================== =================================================
 :ref:`Frozen Group of Objects<group>`
====================================================================== =================================================
 `group(object1, ...)`
 `group(objects)`
====================================================================== =================================================

Moving and Positioning Objects
------------------------------

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
 `change_xy(object, x_amount, y_amount)`   Increase the object's `x` and `y` location by the two amounts
 `change_x(object, amount)`                Increase the object's `x` location by the `amount`
 `change_y(object, amount)`                Increase the object's `y` location by the `amount`
 `set_x(object, new_x)`                    Set the object's `x` coordinate to be `new_x`
 `set_y(object, new_y)`                    Set the object's `y` coordinate to be `new_y`
 `get_x(object)`                           Get the object's `x` coordinate
 `get_y(object)`                           Get the object's `y` coordinate
========================================= ==============================================================================

Rotating Objects
----------------

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

Scaling and Size of Objects
---------------------------

========================================= ===================================================================================
 Size
========================================= ===================================================================================
 `set_scale(object, scale)`               Set the object's `scale` to a float relative to `1.0`
 `change_scale(object, amount)`           Increase the object's scale by the decimal `amount`
 `grow(object, times)`                    Make the object bigger by `times`, setting its scale to that value
 `shrink(object, times)`                  Make the object smaller by `times`, setting its scale to the inverse of that value
 `grow_x(object, amount)`                 Increase the object's horizontal `scale_x` by the decimal `amount`
 `grow_y(object, amount)`                 Increase the object's vertical `scale_y` by the decimal `amount`
 `set_scale_x(object, new_scale_x)`       Set the object's horizontal `scale_x` to the `new_scale_x`
 `set_scale_y(object, new_scale_y)`       Set the object's horizontal `scale_y` to the `new_scale_y`
 `get_scale(object)`                      Get the object's `scale`
 `get_scale_x(object)`                    Get the object's horizontal `scale_x`
 `get_scale_y(object)`                    Get the object's vertical `scale_y`
 `get_width(object)`                      Get the object's horizontal width in pixels before scaling
 `get_height(object)`                     Get the object's vertical height in pixels before scaling
========================================= ===================================================================================

Visibility of Objects
---------------------

========================================= ==============================================================================
 Visibility
========================================= ==============================================================================
 `show(object)`                           Makes the object `visible`
 `hide(object)`                           Makes the object not `visible` (aka hidden)
 `set_visible(object, status)`            Sets the object to be `visible` or not based on `status`
 `get_visible(object)`                    Get whether or not the object is `visible`
========================================= ==============================================================================

Flipping Objects
----------------

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


