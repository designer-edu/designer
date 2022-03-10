.. _emoji_clicker:

-------------
Emoji Clicker
-------------

In 2013, the web-based "Cookie Clicker" game took the world by storm. The game was exceedingly simple: players clicked
on a giant cookie in order to earn points. Although the game had a lot of other bells and whistles, the simplicity
of the core concept was a major selling point.

You are going to make your own Cookie Clicker type of game, called "Emoji Clicker". Instead of earning points,
your game will feature an emoji slowly growing bigger and bigger until it gets too big. However, you can also click
the emoji to make the emoji get smaller.

In order to make this game, we'll need to learn about Designer's Events, along with knowing how to define functions
and write `if` statements.

===================
1. Drawing an Emoji
===================

We need to start by just drawing the emoji on the screen. We can use what we learned before to
call the ``emoji`` function, passing in a string value; then we pass the result of the ``emoji`` function into
the ``draw`` function. When you run this code, a window should appear with an emoji in the middle.

.. code-block:: python

    from designer import *

    draw(emoji("dog face"))

**Problem 1:** Change the string value so that a different emoji is drawn. You can find
emojis `here <https://emojis.wiki/>`_; you can use either the formal name of the
emoji (e.g., ``"dog face"``) or the emoji itself (``"🐶"``).

====================
2. Growing the Emoji
====================

On its own, we have not made a very exciting game. Nothing happens when we run it!
Let's change that by *binding* a *function* to an *event*. Specifically, we are going to make
the emoji grow (increase scale) every *update* of the game. Let's look at the new code, and
then we'll explain what we are seeing.

.. code-block:: python
    :emphasize-lines: 3-6

    from designer import *

    def grow_picture(picture: DesignerObject):
        change_scale(picture, .5)

    when("updating", grow_picture)
    draw(emoji("dog face"))

The new function ``grow_picture`` consumes a ``picture`` and then calls the ``change_scale`` function
using it and the value ``.5``. The function does not return anything; instead, it just makes a
*tiny little* change to the ``picture`` it was given.

On its own, defining the ``grow_picture`` function does not do anything. We also cannot call the
function on our own - that would simply make the emoji a tiny bit bigger, and what argument
would we use for ``picture`` anyway? We can't just make a new ``emoji("dog face")`` each time, or it won't keep growing.

Instead we have to bind the ``"updating"`` event to our ``grow_picture`` function using
the ``when`` built-in function. The result almost reads like a sentence: "When the game is updating,
grow the picture." This is why it is necessary to only grow the picture a tiny amount:
the game updates many times a second (usually 30 times, in fact), so we only have to describe a very
small, incremental change to our world.

Notice that the ``when`` function takes a string representing the event (``"updating"``) and
the *name* of a function (``grow_picture``). Critically, we are NOT calling the
function ``grow_picture`` on that line - we don't ever call the function ourselves!
Instead, we are handing the function to Designer and politely asking Designer to call it on our behalf,
every update of the game. In return, Designer provides us the same ``picture`` that we originally passed as an argument
to ``draw``.
This idea of defining functions that make small changes in the world, and
then binding them with the ``when`` function is at the heart of Designer games. We call this "Event Handling".

**Problem 2:** Change the second argument of ``change_scale`` to be a much smaller decimal, so that the picture
does not grow as fast.

========================
3. Picture Grows Too Big
========================

When the emoji gets too big, the game should stop. We need to add some logic to the game to check the current *scale*
of the ``picture``; when the horizontal scale gets too big, we will ``pause`` the game. Since this could happen at any
update, we will add another ``when("updating", ...)`` to our program, this time binding a function ``check_picture``.

.. code-block:: python
    :emphasize-lines: 6-8, 11

    from designer import *

    def grow_picture(picture: DesignerObject):
        change_scale(picture, .5)

    def check_picture(picture: DesignerObject):
        if get_scale_x(picture) > 8:
            pause()

    when("updating", grow_picture)
    when("updating", check_picture)
    draw(emoji("dog face"))

The ``check_picture`` function uses the ``get_scale_x`` function to check the current horizontal scale of the ``picture``. If
the scale has exceeded 8 (aka is now 8 times bigger than the original size), we ``pause`` the game. We ``pause`` instead of
``stop`` so that the window stays open afterwards (``stop`` will completely end the game).

Why do we check the horizontal scale specifically, instead of the vertical? It doesn't actually matter - since we are
using ``change_scale``, both the horizontal and vertical scales will be change at the same time, and we could check either
one.

**Problem 3:** Add a new line to the ``if`` statement's body to change the ``picture`` using the ``set_emoji_name`` function.
The ``set_emoji_name(object, new_name)`` function consumes a Designer Object (i.e., ``picture``) and a string value
representing the new emoji name to use. You are free to use whatever emoji you want, such as a Cross Mark or an
Explosion or a Frowny Face. Remember, ``if`` statements can have multiple lines of code in their body, but each
line INSIDE the body is indented the same amount!

======================
4. Shrinking the Emoji
======================

It's not really a game if all you can do is watch the Emoji get bigger and bigger until you lose. Next we'll add
some interactivity. Specifically, when the user clicks on the emoji, the picture should get a little bit smaller.
Making the picture smaller can be done by passing a negative value to the ``change_scale`` function. But to make the
emoji shrink only when we click the mouse instead of every update, we need to bind the ``"clicking"`` event to our new
``shrink_picture`` function.

.. code-block:: python
    :emphasize-lines: 10-11, 15

    from designer import *

    def grow_picture(picture: DesignerObject):
        change_scale(picture, .5)

    def check_picture(picture: DesignerObject):
        if get_scale_x(picture) > 8:
            pause()

    def shrink_picture(picture: DesignerObject):
        change_scale(picture, -.5)

    when("updating", grow_picture)
    when("updating", check_picture)
    when("clicking", shrink_picture)
    draw(emoji("dog face"))

The event ``"clicking"`` only activates when the user clicks the mouse button anywhere on the screen. Once again,
Designer will provide us with the current ``picture``, so we can use that as the argument to ``change_scale`` along with
the negative value. However, we actually want the emoji to shrink only IF the player clicks on the Emoji (as opposed
to anywhere else on the screen).

**Problem 4:** Use the ``colliding_with_mouse`` and ``if`` statement to make the ``picture`` shrink ONLY if the
user actually clicks on the emoji. The ``colliding_with_mouse(object)`` function consumes a Designer Object, and produces
a boolean indicating whether or not the mouse is currently on top of the given object. Hint: you will *not* need
any ``==`` operators because the ``colliding_with_mouse`` function already returns a boolean.

=====================
5. Changing the Emoji
=====================

At this point, our game is technically playable and could be shown to other people. But we have some cute features
to add before that. The first new feature is the ability to switch what emoji is currently active. When the player
presses the right arrow on their keyboard, the emoji's picture should cycle through a few different images. Using
``when``, we can bind a ``"typing"`` event to our new ``change_picture`` function. However, that function will be a little
more complicated since it will depend on another new function ``next_picture``. Let us look at the new code.

.. code-block:: python
    :emphasize-lines: 13-23, 28

    from designer import *

    def grow_picture(picture: DesignerObject):
        change_scale(picture, .5)

    def check_picture(picture: DesignerObject):
        if get_scale_x(picture) > 8:
            pause()

    def shrink_picture(picture: DesignerObject):
        change_scale(picture, -.5)

    def change_picture(picture: DesignerObject, key: str):
        if key == "right":
            next_picture(picture)

    def next_picture(picture: DesignerObject):
        if get_emoji_name(picture) == "___":
            set_emoji_name(picture, "___")
        elif get_emoji_name(picture) == "___":
            set_emoji_name(picture, "___")
        else:
            set_emoji_name(picture, "___")

    when("updating", grow_picture)
    when("updating", check_picture)
    when("clicking", shrink_picture)
    when("typing", change_picture)
    draw(emoji("dog face"))

The ``change_picture`` function is unusual compared to the other Event Handling functions, since in addition to the
``picture`` parameter there is also a ``key`` parameter. The ``key`` is a string value representing what keyboard key the user
pressed. The ``"right"``, ``"left"``, ``"up"``, and ``"down"`` keys are often very useful for making games, but there are many
other options. In our ``change_picture`` function, we check if the user typed the ``"right"`` arrow key; if so, then we
call our ``next_picture`` function passing in our ``picture`` as the argument.

The ``next_picture`` function consumes the current ``picture`` and uses a chain of ``if``, ``elif``, and ``else`` statements
to update the emoji based on the current emoji's name. Remember, these conditional statements are "mutually exclusive"
to each other - the first one that is triggered (has a ``True`` condition) means the rest are skipped. We've left
the string values to compare against the current ``picture`` name AND the string values to use as the argument for
``set_emoji_name`` to be blanks (``"___"``), since the choice of which emojis to use is up to you.

**Problem 5.a**: Fill in the blanks of the ``next_picture`` function so that the Emoji advances through three
different pictures. You can choose which pictures to use. Let's think carefully about an example of the logic:
Let us say that if the current picture is ``"Dog Face"``, then the next picture should be ``"Cat Face"``. Then the ``if``
statement should ask whether the current picture is ``"Dog Face"`` and if so then its body should call ``set_emoji_name``
with ``"Cat Face"``. Then the ``elif`` checks if the current emoji is ``"Cat Face"``, and if so changes it to something else.
The final ``else`` condition should always set the Emoji back to the original one (in this case ``"Dog Face"``).

Once you have the logic figured out, you should be able to press the right arrow key to cycle through all the emojis
you've selected. But what if we want to also cycle backwards?

**Problem 5.b**: Define a new function ``previous_picture`` that performs the inverse of the ``next_picture`` function.
Like the other function, the ``previous_picture`` function should consume a ``picture`` and produce nothing, instead
calling the ``set_emoji_name`` function. The logic should be reversed. Call the ``previous_picture`` function correctly
inside of the ``change_picture`` function IF the player types the ``"left"`` arrow key.

=======================
6. Varying Growth Rates
=======================

We are almost done, we just have one more feature to add. Since we have different emojis, we will make them
grow at different rates, essentially having different difficulty levels.

**Problem 6**: Define a new function named ``get_growth_rate`` that consumes a ``picture`` and produces a
float value indicating how much that emoji should grow in one step. Then, call that function in your existing
``grow_picture`` function so that the ``picture`` grows at the varying rate instead of the constant rate.

===============
7. Going Beyond
===============

At this point, you have achieved all of the features you need for your game! Show it to someone else and see what
they think! Here are some other ways to extend the game.

* If you're not happy with your game having no way to win, you are free to add another condition to
  ``check_picture`` that determines if the Emoji has shrunk down small enough, and then end the game the same way.
* Change the background image (``set_window_image(path)``) and window size (``set_window_size(width, height)``)
  to be something more thematically appropriate to your game.
* Look up the ``randint`` function, which allows you to make random integers. Use this function to have the emoji
  move around the screen at random times and to random positions.

