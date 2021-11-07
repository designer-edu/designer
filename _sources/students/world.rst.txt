.. _world:

---------------
Designer Worlds
---------------

Graphics are great, but wouldn't it be cool to make stuff move and bounce and jump?
To click your mouse and collect a coin, or strike a key and make a heart wiggle?
In this guide, we'll talk about how you can use Designer to make a game, animation, or interactive
visualization.

We begin with the absolute minimum Designer program:

.. code-block:: python

    from designer import *

    start()

The first line of code imports all of Designer's commands, making them available to be used.
The second line (:code:`start()`) causes an external blank white window to appear.
You will generally always need these two lines of code for Designer to function.
The :code:`start` command works just like the `draw` command, but helps us to understand that we are
"starting" a game rather than just drawing some simple objects.

The :code:`start()` command goes at the very end of all of your other code. Once you
:code:`start` your game, no other code will run: the game enters an infinite loop and continues forever.
Let's see what kind of code we can put before then.

.. image:: images/world_0.png
   :width: 700
   :alt: A window with nothing in it.

^^^^^^^^^
The World
^^^^^^^^^

A central concept in Designer games is the World. The state (or "model") of the World controls
what you see in the Window (or "View"). If something does not exist in the World, then it does
not exist in the Window. Technically speaking, the state of the World can be any type of data,
but by convention we make it a dictionary containing references to Designer Objects.

Let's make a simple World with just a box in the center of the screen.

.. code-block:: python

    from designer import *

    # Define the shape of the World
    World = { "box": DesignerObject }

    # Create a function that creates new worlds
    def create_the_world() -> World:
        # Actually create an initial World instance
        return {
            # The world has a 20x30 black rectangle in it
            "box": rectangle("black", 200, 100)
        }

    # This tells Designer to call our `create_the_world` function
    # when the game starts, in order to setup our initial World.
    when("starting", create_the_world)

    start()

To properly define a World, we create a definition on line 4 using the typed dictionary
syntax. We say that a World is any dictionary that has a key named :code:`"box"` and a value
that maps to a value of type :code:`DesignerObject`. The :code:`DesignerObject` is a fundamental
concept in Designer, representing the actual drawable shapes and images on the screen.

Line 4 only describes the shape of the World; no actual World has been created yet.
Instead, that is the responsibility of the :code:`create_the_world` function.
This is a "nullary function" (it takes no parameters) that returns a World.
You might also call it a "constructor" for Worlds. Every time we call that function,
we get a fresh new copy of the default, initial World. However, we do not call that function
ourselves.

Instead, line 16 uses the name of the function (without parentheses!) to tell Designer
what to do when the game is starting. Formally, we are binding the :code:`"starting"` event
to our event handler function :code:`create_the_world`. Informally, we can say that now
the :code:`create_the_world` function will be called on the game's start, in order to create
the World.

Our World is quite simple: a dictionary with the key `"box"` mapped to a :ref:`rectangle<rectangle>`.
We created the rectangle to be black and have a width of 200 and a height of 100.
Because the rectangle is stored in the dictionary that we return, it will be drawn in the world.

.. image:: images/world_1.png
   :width: 700
   :alt: A window with a black rectangle in the middle.


^^^^^^^^^^^^^^^^^^
Updating the World
^^^^^^^^^^^^^^^^^^

We've created a rectangle, but it's not doing anything yet. Let's create
a function that will tell Designer how to manipulate our rectangle.

.. code-block:: python
    :emphasize-lines: 14-17,22-24

    from designer import *

    # Define the shape of the World
    World = { "box": DesignerObject }

    # Create a function that creates new worlds
    def create_the_world() -> World:
        # Actually create an initial World instance
        return {
            # The world has a 20x30 black rectangle in it
            "box": rectangle("black", 200, 100)
        }

    # Define a function that spins the box
    def spin_the_box(world: World):
        # Increase the boxes angle by one degree
        world['box']['angle'] += 1

    # This tells Designer to call our `create_the_world` function
    # when the game starts, in order to setup our initial World.
    when("starting", create_the_world)
    # Tell Designer to call our spin_the_box function every update.
    # There are usually 30 updates per second!
    when("updating", spin_the_box)

    start()

The new function, `spin_the_box` consumes a World and changes the value in one of its fields.
Specifically, it accesses the `'box'` key to get access to our previously-created rectangle,
and then increments its `angle` key's value by 1. This means to "rotate the box by one degree."

On its own, defining the `spin_the_box` function does not do anything. We also cannot call
the function on our own - that would simply rotate the box by only one degree, and where
would we get a World from anyway?

Instead we have to bind the `"updating"` event to our `spin_the_box` function using the
:ref:`when<when>` built-in function. The result almost reads like a sentence: "When the
game is updating, spin the box." This is why it is necessary to only rotate the box a single
degree: the game updates many times a second (usually 30 times, in fact), so we only have
to describe a very small, incremental change to our world.

This idea of defining functions that make small changes in the world, and then binding them with
the :ref:`when<when>` function is at the heart of Designer games. We call this "Event Handling".

.. image:: images/world_2.gif
   :width: 700
   :alt: A window with a black ROTATING rectangle in the middle.

^^^^^^^^^^^^^^^^^^^^^^^^^^
Interacting with the World
^^^^^^^^^^^^^^^^^^^^^^^^^^

It's not a game if there isn't any interaction, so let's now add the ability to move the
rectangle by clicking on the screen. We'll use another event type, `"clicking"`, which
provides some additional parameters.

.. code-block:: python
    :emphasize-lines: 19-23,31-32

    from designer import *

    # Define the shape of the World
    World = { "box": DesignerObject }

    # Create a function that creates new worlds
    def create_the_world() -> World:
        # Actually create an initial World instance
        return {
            # The world has a 20x30 black rectangle in it
            "box": rectangle("black", 200, 100)
        }

    # Define a function that spins the box
    def spin_the_box(world: World):
        # Increase the boxes angle by one degree
        world['box']['angle'] += 1

    # Move the box to the given position
    def move_the_box(world: World, x: int, y: int):
        # Adjust the X and Y positions of the box
        world['box']['x'] = x
        world['box']['y'] = y

    # This tells Designer to call our `create_the_world` function
    # when the game starts, in order to setup our initial World.
    when("starting", create_the_world)
    # Tell Designer to call our spin_the_box function every update.
    # There are usually 30 updates per second!
    when("updating", spin_the_box)
    # Tell Designer to call our move_the_box function every click.
    when("clicking", move_the_box)

    start()

The new function `move_the_box` takes in two parameters, which are carefully named `x` and `y`.
The names matter here, because Designer will actually look at them and expect those names!
If you chose other names, then an error message would appear. But because we chose the right names,
when we click the mouse, Designer will call the `move_the_box` function, passing in not only the current world
but also the X and Y of the mouse.
These X and Y values are then assigned to the boxes X and Y fields, updating its position on the screen.

The only other thing to do is to bind the function to the event. Again, the name matters here: a typo would
prevent the event from being bound correctly, and the function would not be called.

.. image:: images/world_3.gif
   :width: 700
   :alt: A window with a black ROTATING rectangle in the middle. A mouse clicks on random positions and the rectangle's jumps to that spot.

^^^^^^^^^^^^^^^^^^^^^
A Touch of Randomness
^^^^^^^^^^^^^^^^^^^^^

A game has an objective, and since our game doesn't, it's actually more of a visualization. Let's change things up so
that we have a goal: to click on the spinning box as it jumps around the screen randomly. Let's focus on making
the box jump around randomly first.

.. code-block:: python
    :emphasize-lines: 20-27,35-36

    from designer import *
    import random

    # Define the shape of the World
    World = { "box": DesignerObject }

    # Create a function that creates new worlds
    def create_the_world() -> World:
        # Actually create an initial World instance
        return {
            # The world has a 20x30 black rectangle in it
            "box": rectangle("black", 200, 100)
        }

    # Define a function that spins the box
    def spin_the_box(world: World):
        # Increase the boxes angle by one degree
        world['box']['angle'] += 1

    # Move the box to a random position
    def teleport_the_box(world: World):
        # Have a 1 in 10 chance of jumping around
        if random.randint(0, 9) == 0:
            # Set x/y to be random coordinates within the bounds of the
            # window, given by get_width() and get_height()
            world['box']['x'] = random.randint(0, get_width())
            world['box']['y'] = random.randint(0, get_height())

    # This tells Designer to call our `create_the_world` function
    # when the game starts, in order to setup our initial World.
    when("starting", create_the_world)
    # Tell Designer to call our spin_the_box function every update.
    # There are usually 30 updates per second!
    when("updating", spin_the_box)
    # Tell Designer to call teleport_the_box every update.
    when("updating", teleport_the_box)

    start()

We've made a number of changes to our previous function. First, it's no longer bound to the
`'clicking'` event, but bound to the `'updating'` event. Designer let's you bind any number of functions
to the same event, with no limitation. You can also pass in multiple functions to the same event, if you want.

The `move_the_box` function has become `teleport_the_box`, and it no longer consumes an `x` and a `y` (since those
were only available in the `clicking` event). Instead, we now set the boxes `x` and `y` fields to be a randomly chosen
value between 0 and either the width of the window (from :ref:`get_width<get_width>`) or the height of the window (from
:ref:`get_height<get_height>`). The `randint` function is available in the built-in `random` module, and produces an
integer between the two values given as parameters.

If we teleported the box every step, the box would move very, very fast. To make things a little fairer, we only
teleport the box on 1 in 10 updates. To achieve this, we guard the update with an `if` statement that checks if a
randomly chosen value between 0 and 9 (including 9 itself) is equal to 0. Since this will happen about 10% of the time,
so we can anticipate this happening only about 3 times a second. Notice that we are still calling the function every
update; we just don't execute the body of its `if` statement every update!

.. image:: images/world_4.gif
   :width: 700
   :alt: A window with a black ROTATING rectangle. The rectangle is jumping around the screen quite fast.

^^^^^^^^^^^^^
Keeping Score
^^^^^^^^^^^^^

We're going to earn points by clicking on the rectangle, but how do we know if we were successful?
A simple solution is to keep score and show the user how many times they have clicked the rectangle.

.. code-block:: python
    :emphasize-lines: 7-8, 37-42, 52-53

    from designer import *
    import random

    # Define the shape of the World
    World = {
        "box": DesignerObject,
        "message": DesignerObject,
        "score": int,
    }

    # Create a function that creates new worlds
    def create_the_world() -> World:
        # Actually create an initial World instance
        return {
            # The world has a 20x30 black rectangle in it
            "box": rectangle("black", 200, 100),
            # The message to show the user
            "message": text("black", "Score:"),
            # The player's current score
            "score": 0
        }

    # Define a function that spins the box
    def spin_the_box(world: World):
        # Increase the boxes angle by one degree
        world['box']['angle'] += 1

    # Move the box to a random position
    def teleport_the_box(world: World):
        # Have a 1 in 10 chance of jumping around
        if random.randint(0, 9) == 0:
            # Set x/y to be random coordinates within the bounds of the
            # window, given by get_width() and get_height()
            world['box']['x'] = random.randint(0, get_width())
            world['box']['y'] = random.randint(0, get_height())

    # Keep the message in sync with the current score
    def track_the_score(world: World):
        # Get the current score
        score = world['score']
        # Update the message's text based on the score
        world['message']['text'] = "Score: " + str(score)

    # This tells Designer to call our `create_the_world` function
    # when the game starts, in order to setup our initial World.
    when("starting", create_the_world)
    # Tell Designer to call our spin_the_box function every update.
    # There are usually 30 updates per second!
    when("updating", spin_the_box)
    # Tell Designer to call teleport_the_box every update.
    when("updating", teleport_the_box)
    # Tell Designer to call track_the_score every update.
    when("updating", track_the_score)

    start()

This isn't a terribly exciting update in terms of new functionality, since all that appears on the screen is the
text `"Score: 0"`. Without a way to increase the score, we don't see very much. However, this demonstrates how we
can have state besides DesignerObjects (the `"score"`, an integer) and also display text on the screen. In order to keep
the text in sync with the score, we've defined a function named `track_the_score` that gets called every update. Notice
how we extract data from the World (specifically, the current `"score"`) and use that to update the field of the text
object we created before. In order to prefix the score with the text `"Score:"`, we had to convert the integer score to
a string representation.

.. image:: images/world_5.gif
   :width: 700
   :alt: A window with a teleporting, rotating, black rectangle. The words "Score: 0" are in the middle of the window.

^^^^^^^^^^^^^^^^^^^^
Responding to Clicks
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :emphasize-lines: 44-50, 62-63

    from designer import *
    import random

    # Define the shape of the World
    World = {
        "box": DesignerObject,
        "message": DesignerObject,
        "score": int,
    }

    # Create a function that creates new worlds
    def create_the_world() -> World:
        # Actually create an initial World instance
        return {
            # The world has a 20x30 black rectangle in it
            "box": rectangle("black", 200, 100),
            # The message to show the user
            "message": text("black", "Score:"),
            # The player's current score
            "score": 0
        }

    # Define a function that spins the box
    def spin_the_box(world: World):
        # Increase the boxes angle by one degree
        world['box']['angle'] += 1

    # Move the box to a random position
    def teleport_the_box(world: World):
        # Have a 1 in 10 chance of jumping around
        if random.randint(0, 9) == 0:
            # Set x/y to be random coordinates within the bounds of the
            # window, given by get_width() and get_height()
            world['box']['x'] = random.randint(0, get_width())
            world['box']['y'] = random.randint(0, get_height())

    # Keep the message in sync with the current score
    def track_the_score(world: World):
        # Get the current score
        score = world['score']
        # Update the message's text based on the score
        world['message']['text'] = "Score: " + str(score)

    # Check if the box has been clicked and increase the score
    def check_box_clicked(world: World, x: int, y: int):
        # Use the Designer function colliding to check if two objects or
        # an object and a point are colliding.
        if colliding(world['box'], x, y):
            # Update the score on a successful click
            world['score'] += 1

    # This tells Designer to call our `create_the_world` function
    # when the game starts, in order to setup our initial World.
    when("starting", create_the_world)
    # Tell Designer to call our spin_the_box function every update.
    # There are usually 30 updates per second!
    when("updating", spin_the_box)
    # Tell Designer to call teleport_the_box every update.
    when("updating", teleport_the_box)
    # Tell Designer to call track_the_score every update.
    when("updating", track_the_score)
    # Tell Designer to call check_box_clicked when the mouse is clicked
    when('clicking', check_box_clicked)

    start()

We haven't added much new code - mostly just a new event handler named `check_box_clicked`. This function
is bound to the `"clicking"` event that we saw before. However, the function uses a new feature we haven't
yet seen: the handy :ref:`colliding<colliding>` function. This function can take in either two objects, or an object
and an x/y pair. The function returns True if they overlap, or otherwise False if they do not. We use the function
here to detect if the box was clicked.

Actually clicking the box is a little tricky! For testing purposes, you might want to disable the teleportation or
decrease the probability that it will teleport on a given update. Regardless, you can see from the video below that
clicking on the rectangle gives you a point.

.. image:: images/world_6.gif
   :width: 700
   :alt: A window with a teleporting, rotating, black rectangle. The mouse clicks on the rectangle a few times, increasing the score displayed each time.


^^^^^^^^^^^^^^^
Ending the Game
^^^^^^^^^^^^^^^

Our game is almost complete. All that we have to do now is establish some criteria for when the game is over, and
then stop the game. For that, we'll take advantage of a custom event check and the Designer `pause` function.

.. code-block:: python
    :emphasize-lines: 11-12, 55-61, 75-77

    from designer import *
    import random

    # Define the shape of the World
    World = {
        "box": DesignerObject,
        "message": DesignerObject,
        "score": int,
    }

    # The score you need to win the game
    WIN_THRESHOLD = 5

    # Create a function that creates new worlds
    def create_the_world() -> World:
        # Actually create an initial World instance
        return {
            # The world has a 20x30 black rectangle in it
            "box": rectangle("black", 200, 100),
            # The message to show the user
            "message": text("black", "Score:"),
            # The player's current score
            "score": 0
        }

    # Define a function that spins the box
    def spin_the_box(world: World):
        # Increase the boxes angle by one degree
        world['box']['angle'] += 1

    # Move the box to a random position
    def teleport_the_box(world: World):
        # Have a 1 in 10 chance of jumping around
        if random.randint(0, 9) == 0:
            # Set x/y to be random coordinates within the bounds of the
            # window, given by get_width() and get_height()
            world['box']['x'] = random.randint(0, get_width())
            world['box']['y'] = random.randint(0, get_height())

    # Keep the message in sync with the current score
    def track_the_score(world: World):
        # Get the current score
        score = world['score']
        # Update the message's text based on the score
        world['message']['text'] = "Score: " + str(score)

    # Check if the box has been clicked and increase the score
    def check_box_clicked(world: World, x: int, y: int):
        # Use the Designer function colliding to check if two objects or
        # an object and a point are colliding.
        if colliding(world['box'], x, y):
            # Update the score on a successful click
            world['score'] += 1

    # Check if the score is above the threshold
    def the_score_is_high_enough(world: World):
        return world['score'] >= WIN_THRESHOLD

    # Flash a game over message
    def flash_game_over(world: World):
        world['message']['text'] = "Game over, you won!"

    # This tells Designer to call our `create_the_world` function
    # when the game starts, in order to setup our initial World.
    when("starting", create_the_world)
    # Tell Designer to call our spin_the_box function every update.
    # There are usually 30 updates per second!
    when("updating", spin_the_box)
    # Tell Designer to call teleport_the_box every update.
    when("updating", teleport_the_box)
    # Tell Designer to call track_the_score every update.
    when("updating", track_the_score)
    # Tell Designer to call check_box_clicked when the mouse is clicked
    when('clicking', check_box_clicked)
    # Tell Designer to check if the game is over, then flash our message
    # and pause on that screen
    when(the_score_is_high_enough, flash_game_over, pause)

    start()

The first function we created (`the_score_is_high_enough`) is a custom event: in order to satisfy that purpose,
we have to define the function to be a *predicate* (i.e., a function that reutrns a boolean value). Designer
will call the function every update and when it is True, it will call all the subsequent functions one after the
other.

In this case, the predicate `the_score_is_high_enough` checks the current value stored in the World's `score` and
compares it to a global constant we created named `WIN_THRESHOLD`. Rather than embedding that value in the function,
we created a constant at the top of our program. This makes it much easier for anyone wanting to extend our game
to see what that value represents, since it's a more meaningful name than just the value 5.

We defined a second function `flash_game_over` that changes the `"message"`'s `"text"` field to be a friendly game
over message. This takes advantage of the fact that after the game is paused, the Update event no longer triggers,
meaning that the `track_the_score` function will not overwrite our message's text.

Finally, the :ref:`pause<pause>` function (another Designer built-in) is used to hang the game without closing the
Window (if you wanted to do that, then you could use the :ref:`stop<stop>` function instead. Whatever was drawn last
will still be rendered, but no further events are detected.

.. image:: images/world_7.gif
   :width: 700
   :alt: A window with a teleporting, rotating, black rectangle. The mouse clicks on the rectangle a few times, increasing the score displayed each time, until they earn 5 points and the game ends.

^^^^^^^^^^^
Wrapping Up
^^^^^^^^^^^

So there you have a simple "click the teleporting, spinning rectangle" game. We've incorporated event handling,
collision detection, and several other Designer features all into one code file.

Try making some of these changes to the game:

* Swap out the rectangle for an image of your choice.
* Instead of having the rectangle move randomly, choose a spot that is far away from the mouse.
* Whenever the mouse clicks on the rectangle, immediately have it jump away.
* Create a timer field that increments every update; instead of teleporting at random intevals, have the rectangle teleport every 60 updates.
* Modify the message to also show the current timer.
* Have the rectangle spin forward and then BACKWARD. You'll need an additional field to keep track of its current direction!
