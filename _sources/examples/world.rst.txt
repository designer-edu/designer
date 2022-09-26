.. _world:

---------------
Designer Worlds
---------------

Graphics are great, but wouldn't it be cool to make stuff move and bounce and jump?
To click your mouse and collect a coin, or strike a key and make a heart wiggle?
In this guide, we'll talk about how you can use Designer to make a game, animation, or interactive
visualization.

We begin with the absolute minimum Designer program:

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_1_dictionaries.py
            :language: python

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_1_dictionaries.py
            :language: python

The first line of code imports all of Designer's commands, making them available to be used.
The second line (:code:`start()`) causes an external blank white window to appear.
You will generally always need these two lines of code for Designer to function.
The :code:`start` command works just like the :code:`draw` command, but helps us to understand that we are
"starting" a game rather than just drawing some simple objects.

The :code:`start()` command goes at the very end of all of your other code. Once you
:code:`start` your game, no other code will run: the game enters an infinite loop and continues forever.
Let's see what kind of code we can put before then.

.. image:: images/world/world_0.png
   :width: 700
   :alt: A window with nothing in it.

^^^^^^^^^
The World
^^^^^^^^^

A central concept in Designer games is the World. The state (or "model") of the World controls
what you see in the Window (or "View"). If something does not exist in the World, then it does
not exist in the Window. Technically speaking, the state of the World can be any type of data,
but by convention we make it a dataclass or a dictionary containing references to Designer Objects.

Let's make a simple World with just a box in the center of the screen.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_2_dataclasses.py
            :language: python
            :linenos:

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_2_dictionaries.py
            :language: python
            :linenos:

To properly define a World, we create a definition on line 4. We say that a World is has a :code:`box`
with a value of type :code:`DesignerObject`.
The :code:`DesignerObject` is a fundamental concept in Designer, representing the actual drawable shapes
and images on the screen.

The definition only describes the shape of the World; no actual World has been created yet.
Instead, that is the responsibility of the :code:`create_the_world` function.
This is a "nullary function" (it takes no parameters) that returns a :code:`World`.
You might also call it a "constructor" for Worlds. Every time we call that function,
we get a fresh new copy of the default, initial :code:`World`. However, we do not call that function
ourselves.

Instead, we pass the name of the function (without parentheses!) to the code:`when` function, to tell Designer
what to do when the game is starting. Formally, we are binding the :code:`"starting"` event
to our event handler function :code:`create_the_world`. Informally, we can say that now
the :code:`create_the_world` function will be called on the game's start, in order to create
the World.

Our World is quite simple: it only has a :code:`box` mapped to a :ref:`rectangle<rectangle>`.
We created the rectangle to be black and have a width of 200 and a height of 100.
Because the rectangle is stored in World that we return, it will be drawn on the screen.

.. image:: images/world/world_1.png
   :width: 700
   :alt: A window with a black rectangle in the middle.


^^^^^^^^^^^^^^^^^^
Updating the World
^^^^^^^^^^^^^^^^^^

We've created a rectangle, but it's not doing anything yet. Let's create
a function that will tell Designer how to manipulate our rectangle.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_3_dataclasses.py
            :language: python
            :emphasize-lines: 14-18,23-25
            :linenos:

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_3_dictionaries.py
            :language: python
            :emphasize-lines: 14-17,22-24
            :linenos:

The new function, :code:`spin_the_box` consumes a World and changes the value in one of its fields.
Specifically, it accesses the :code:`'box'` to get access to our previously-created rectangle,
and then increments its :code:`angle` by 1. This means to "rotate the box by one degree."

On its own, defining the :code:`spin_the_box` function does not do anything. We also cannot call
the function on our own - that would simply rotate the box by only one degree (a tiny amount), and where
would we get a World from anyway?

Instead we have to bind the :code:`"updating"` event to our :code:`spin_the_box` function using the
:ref:`when<when>` built-in function. The result almost reads like a sentence: "When the
game is updating, spin the box." This is why it is necessary to only rotate the box a single
degree: the game updates many times a second (usually 30 times, in fact), so we only have
to describe a very small, incremental change to our world.

This idea of defining functions that make small changes in the world, and then binding them with
the :ref:`when<when>` function is at the heart of Designer games. We call this "Event Handling".

.. image:: images/world/world_2.gif
   :width: 700
   :alt: A window with a black ROTATING rectangle in the middle.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Interacting with the World
^^^^^^^^^^^^^^^^^^^^^^^^^^

It's not a game if there isn't any interaction, so let's now add the ability to move the
rectangle by clicking on the screen. We'll use another event type, :code:`"clicking"`, which
provides some additional parameters.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_4_dataclasses.py
            :language: python
            :emphasize-lines: 20-25,33-34
            :linenos:

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_4_dictionaries.py
            :language: python
            :emphasize-lines: 19-23,31-32
            :linenos:

The new function :code:`move_the_box` takes in two parameters, which are carefully named :code:`x` and :code:`y`.
The names matter here, because Designer will actually look at them and expect those names!
If you chose other names, then an error message would appear. But because we chose the right names,
when we click the mouse, Designer will call the :code:`move_the_box` function, passing in not only the current world
but also the X and Y of the mouse.
These X and Y values are then assigned to the boxes :code:`x` and :code:`y` fields, updating its position on the screen.

The only other thing to do is to bind the function to the event. Again, the name matters here: a typo would
prevent the event from being bound correctly, and the function would not be called.

.. image:: images/world/world_3.gif
   :width: 700
   :alt: A window with a black ROTATING rectangle in the middle. A mouse clicks on random positions and the rectangle's jumps to that spot.

^^^^^^^^^^^^^^^^^^^^^
A Touch of Randomness
^^^^^^^^^^^^^^^^^^^^^

A game has an objective, and since our game doesn't, it's actually more of a visualization. Let's change things up so
that we have a goal: to click on the spinning box as it jumps around the screen randomly. Let's focus on making
the box jump around randomly first.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_5_dataclasses.py
            :language: python
            :emphasize-lines: 21-30,38-39
            :linenos:

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_5_dictionaries.py
            :language: python
            :emphasize-lines: 20-27,35-36
            :linenos:

We've made a number of changes to our previous function. First, it's no longer bound to the
:code:`'clicking'` event, but bound to the :code:`'updating'` event. Designer let's you bind any number of functions
to the same event, with no limitation. You can also pass in multiple functions to the same event, if you want.

The :code:`move_the_box` function has become :code:`teleport_the_box`, and it no longer consumes an :code:`x` and a
:code:`y` (since those were only available in the :code:`clicking` event). Instead, we now set the boxes
:code:`x` and :code:`y` fields to be a randomly chosen value between 0 and either the width of the window
(from :ref:`get_width<get_width>`) or the height of the window (from :ref:`get_height<get_height>`).
The :code:`randint` function is available in the built-in :code:`random` module, and produces an
integer between the two values given as parameters.

If we teleported the box every step, the box would move very, very fast. To make things a little fairer, we only
teleport the box on 1 in 10 updates. To achieve this, we guard the update with an :code:`if` statement that checks if a
randomly chosen value between 0 and 9 (including 9 itself) is equal to 0. Since this will happen about 10% of the time,
so we can anticipate this happening only about 3 times a second (since Designer games update 30 times a second by default).
Notice that we are still calling the function every update; we just don't execute the body of its :code:`if` statement every update!

.. image:: images/world/world_4.gif
   :width: 700
   :alt: A window with a black ROTATING rectangle. The rectangle is jumping around the screen quite fast.

^^^^^^^^^^^^^
Keeping Score
^^^^^^^^^^^^^

We're going to earn points by clicking on the rectangle, but how do we know if we were successful?
A simple solution is to keep score and show the user how many times they have clicked the rectangle.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_6_dataclasses.py
            :language: python
            :emphasize-lines: 5-9, 17-19, 36-41, 51-52
            :linenos:

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_6_dictionaries.py
            :language: python
            :emphasize-lines: 7-8, 17-20, 37-42, 52-53
            :linenos:

This isn't a terribly exciting update in terms of new functionality, since all that appears on the screen is the
text :code:`Score: 0`. Without a way to increase the score, we don't see very much. However, this demonstrates how we
can have state besides DesignerObjects (the :code:`"score"`, an integer) and also display text on the screen. In order to keep
the text in sync with the score, we've defined a function named :code:`track_the_score` that gets called every update. Notice
how we extract data from the World (specifically, the current :code:`"score"`) and use that to update the field of the text
object we created before. In order to prefix the score with the text :code:`"Score:"`, we had to convert the integer score to
a string representation.

.. image:: images/world/world_5.gif
   :width: 700
   :alt: A window with a teleporting, rotating, black rectangle. The words "Score: 0" are in the middle of the window.

^^^^^^^^^^^^^^^^^^^^
Responding to Clicks
^^^^^^^^^^^^^^^^^^^^

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_7_dataclasses.py
            :language: python
            :emphasize-lines: 44-50, 63-64
            :linenos:

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_7_dictionaries.py
            :language: python
            :emphasize-lines: 44-50, 62-63
            :linenos:

We haven't added much new code - mostly just a new event handler named :code:`check_box_clicked`. This function
is bound to the :code:`"clicking"` event that we saw before. However, the function uses a new feature we haven't
yet seen: the handy :ref:`colliding<colliding>` function. This function can take in either two objects, or an object
and an x/y pair. The function returns True if they overlap, or otherwise False if they do not. We use the function
here to detect if the box was clicked.

Actually clicking the box is a little tricky! For testing purposes, you might want to disable the teleportation or
decrease the probability that it will teleport on a given update. Regardless, you can see from the video below that
clicking on the rectangle gives you a point.

.. image:: images/world/world_6.gif
   :width: 700
   :alt: A window with a teleporting, rotating, black rectangle. The mouse clicks on the rectangle a few times, increasing the score displayed each time.


^^^^^^^^^^^^^^^
Ending the Game
^^^^^^^^^^^^^^^

Our game is almost complete. All that we have to do now is establish some criteria for when the game is over, and
then stop the game. For that, we'll take advantage of a custom event check and the Designer :code:`pause` function.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./world/world_8_dataclasses.py
            :language: python
            :emphasize-lines: 10, 12-16, 25-26, 58-71, 85-89
            :linenos:

    .. group-tab:: Dictionaries

        .. literalinclude:: ./world/world_8_dictionaries.py
            :language: python
            :emphasize-lines: 8-9, 12-16, 28-29, 61-74, 88-92
            :linenos:

We want the game to end after 10 seconds, so we need a little bit more state to hold a :code:`timer`. This will be
an integer that increases by one every update of the game. Therefore, we also add a :code:`advance_the_timer` function
and bind it to the :code:`"updating"` event.

The next function we created ( :code:`the_timer_runs_out`) is a custom event: in order to satisfy that purpose,
we have to define the function to be a *predicate* (i.e., a function that returns a boolean value). Designer
will call the function every update and when it is True, it will call all the subsequent functions one after the
other.

In this case, the predicate  :code:`the_timer_runs_out` checks the current value stored in the World's  :code:`timer` and
compares it to a global constant we created named  :code:`LENGTH_OF_GAME`. Rather than embedding that value in the function,
we created a constant at the top of our program. This makes it much easier for anyone wanting to extend our game
to see what that value represents, since it's a more meaningful name than just the value :code:`300` (which represents
10 seconds, for a game that runs at 30 frames per second).

We defined a third function  :code:`flash_game_over` that changes the  :code:`"message"`'s :code:`"text"` field to be a
simple game over message. This takes advantage of the fact that after the game is paused, the update event no longer triggers,
meaning that the  :code:`track_the_score` function will not overwrite our message's text. That :code:`flash_game_over`
function just has to check the current :code:`score` and determine if it has exceeded the threshold for victory that
we stored in the global constant :code:`WIN_THRESHOLD`.

Finally, the :ref:`pause<pause>` function (another Designer built-in) is used to hang the game without closing the
Window (if you wanted to do that, then you could use the :ref:`stop<stop>` function instead. Whatever was drawn last
will still be rendered, but no further events are processed.

.. image:: images/world/world_7.gif
   :width: 700
   :alt: A window with a teleporting, rotating, black rectangle. The mouse clicks on the rectangle a few times, increasing the score displayed each time, until they earn 5 points and the game ends.

^^^^^^^^^^^
Wrapping Up
^^^^^^^^^^^

So there you have a simple "click the teleporting, spinning rectangle" game. We've incorporated event handling,
collision detection, and several other Designer features all into one code file.

Try making some of these changes to the game:

1. Swap out the rectangle for an image of your choice. Make the image change whenever you click on the rectangle.
2. Instead of having the rectangle move randomly, choose a spot that is far away from the mouse.
3. Whenever the mouse clicks on the rectangle, immediately have it jump away.
4. Instead of teleporting at random intervals, have the rectangle teleport every 60 updates (hint: use the :code:`%` operator).
5. Modify the message to also show the current timer.
6. Have the rectangle spin forward and then BACKWARD. You'll need an additional field to keep track of its current direction!
7. Use the timer to wait an additional 5 seconds after the game ends, and then have everything restart by updating the world appropriately.
