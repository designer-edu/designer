.. _quickstart:

--------------------------
Designer Quick Start Guide
--------------------------
Designer is an educational interactive graphics Python library. What does that mean?

As a student, you can use Designer to learn and practice Python by creating output of pictures and
basic animations.

Let's look at some code to get us started.

Once you've installed Designer, you only need two lines of code to get started:

.. code-block:: python

    from designer import *
    draw()

These two lines of code create an external blank white window to appear. You will generally always need
these two lines of code for Designer to function. Let's fill in some code in between.

^^^^^^^^^^^^^^^^^^^^^
What are our options?
^^^^^^^^^^^^^^^^^^^^^
We can add visual elements, called DesignerObjects, to personalize our output.
A DesignerObject is any graphic representation to add to the window.

For example:

* A bright orange circle is a DesignerObject.
* An image of your favorite animal is a DesignerObject.
* A diagonal blue line is a DesignerObject.

You can use and pass around DesignerObjects as arguments to the ``draw()`` function to add the DesignerObjects
you make to the window.

What are some DesignerObjects?

==========
1. Shapes!
==========
You can make lines, circles, rectangles, ellipses, arcs, or any general polygons with at least three sides.

Let's look at the code and output for making a rectangle:

.. code-block:: python

    from designer import *

    green_rect = rectangle('green', 0, 0, 400, 600)
    draw(green_rect)

Let's unpack ``rectangle('green', 0, 0, 400, 600)``
The function, ``rectangle``, creates and returns a rectangle DesignerObject. It's arguments:

* "green", is the color the rectangle will be.
* The next two arguments, "0, 0", represent the left (0) top (0) corner of the rectangle.
* The window operates on an x, y plane, where (0, 0), is the top left of the window. Moving to the right on the window increases the x value and moving down on the window increases the y value.
* The final two arguments, "400, 300", represent the width (400 pixels) and height (600 pixels) of the rectangle to be drawn.

==========
2. Images!
==========
You can add images in two different ways:
#. The file path to an image
#. The link to an image

Let's use the link to this `frog image`_.

.. code-block:: python

    from designer import *

    frog = image('https://cdn.pixabay.com/photo/2017/08/15/15/44/frog-2644410_960_720.png', 0, 0, 200, 300)
    draw(frog)

Noticing a trend yet? The function, ``image``, creates and returns an image DesignerObject.

* The first argument of ``image`` can be a string representing a url to an image, such as in this example. Or, it can be a string of a file path to an image.

* The next two arguments, "0, 0", are again the left (0) top (0) corner of the image.

* The final two arguments, "200, 300" are the width (200 pixels) and height (300 pixels) of the image.

========
3. Text!
========
You can add any string to the window.

.. code-block:: python

    from designer import *

    hello = text('blue', "Hello World!", 40, 0, 0)
    draw(hello)

The function, ``text``, creates and returns a text DesignerObject.

* The first argument, "blue", is the color the text will be.
* The next argument, "Hello World!", is the text to add to the window.
* The next argument, "40", is the size of the text's font.
* The final two arguments, "0, 0", are the left (0), top (0), corner of the text.

==============================
4. Make a DesignerObject move!
==============================
Let's go back to our frog image code. What if we want it to glide across the window?

Easy, let's add one function call!

.. code-block:: python

   from designer import *

    frog = image('https://cdn.pixabay.com/photo/2017/08/15/15/44/frog-2644410_960_720.png', 0, 0, 200, 300)
    glide_right(frog, 10)
    draw(frog)

See that we've added the function ``glide_right``. By passing a DesignerObject, in this case our frog image,
to the function as the first parameter, we can set it to glide to the right of the window.

The second parameter, "10", is the speed of the frog gliding. The higher the speed, the quicker the DesignerObject moves.

Check out the `documentation of DesignerObjects`_ to see all that you can add to your output!

.. _frog image: https://cdn.pixabay.com/photo/2017/08/15/15/44/frog-2644410_960_720.png
.. _documentation of DesignerObjects: https://krishols.github.io/designer/students/docs.html#module-designer.DesignerObject