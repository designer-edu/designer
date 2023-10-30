.. _arrows:

Arrows
======

This game demonstrates how to have objects that:

    * Respond to ``'typing'`` and ``'done typing'`` events to "keep moving" until a key is released (even when multiple keys are pressed)
    * Moving objects in sync


The major trick is to have a field (e.g., ``active``) that gets set to ``True`` during the ``'typing'`` event
and set to ``False`` during the ``'done typing'`` event. Then, in a ``updating`` event, you can check if the field
is ``True`` and move the object accordingly.

For handling left and right keys, you need two boolean fields. For all four direction keys, you would need four boolean fields.
An alternative solution is to use a string field that gets set to ``'left'``, ``'right'``, ``'up'``, or ``'down'`` during the ``'typing'`` event,
and then set to ``'none'`` during the ``'done typing'`` event. Then, in the ``updating`` event, you can check the value of the field
and move the object accordingly.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./arrows/arrows_dataclasses.py
            :language: python

    .. group-tab:: Dictionaries

        .. literalinclude:: ./arrows/arrows_dictionaries.py
            :language: python