.. _inheritance:

Extending DesignerObjects
=========================

.. note::

        You will need to upgrade Designer to at least version 0.5.0 to run this example!

This game demonstrates how to have:

* A ``DesignerObject`` that has additional extra fields using inheritance

By inheriting from a constructor for a ``DesignerObject``, you can add additional fields.
One drawback is that when calling the constructor for your new class, you must pass in the field as a keyword argument.
This just means you put the name of the field in front of the value you want to pass in.

In this example, we inherit ``MovingEmoji`` from ``Emoji`` so that we can add ``speed`` and ``direction`` fields.
Now, we can freely access ``world.dragon.speed`` the same way we could previously access ``world.dragon.x`` or
``world.dragon.height``.

.. tabs::

    .. group-tab:: Dataclasses

        .. literalinclude:: ./inheritance/inheritance_dataclass.py
            :language: python