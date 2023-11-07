.. _scenes:

Scene Management in Designer
============================

The Designer's scene management allows for dynamic transitions between different parts of the application.
This feature allows you to create, switch, and manage game states or screens effectively.

There are basically three kinds of transitions:

* ``change_scene``: Create a new scene and move to it, destroying the current scene.
* ``push_scene``: Create a new scene and move to it, pausing the current scene.
* ``pop_scene``: Destroy the current scene and move to the previous scene, resuming it.

Scene Transitions
-----------------

The designer package provides several functions to manage scene transitions:

.. function:: change_scene(scene_name, **kwargs)

    Switches from the current scene to a new one, indicated by ``scene_name``.
    The current scene will be destroyed and replaced with the new one.
    Note that the transition happens *at the end of the current update*. The effect is not instantenous,
    so any objects created during the rest of this update cycle will be in the old scene and not the new scene.

   :param str scene_name: The name of the scene to transition to.
   :param kwargs: Keyword arguments that should be passed to the new scene's initialization function.

.. function:: push_scene(scene_name, **kwargs)

    Pauses the current scene and places a new scene on top of the stack. The current scene will be
    paused and can be resumed later.
    Note that the transition happens *at the end of the current update*. The effect is not instantenous,
    so any objects created during the rest of this update cycle will be in the old scene and not the new scene.

   :param str scene_name: The name of the scene to be pushed onto the stack.
   :param kwargs: Keyword arguments that should be passed to the new scene's initialization function.

.. function:: pop_scene(**kwargs)

    Removes the current scene from the stack, resuming the previous one.
    Note that the transition happens *at the end of the current update*. The effect is not instantenous,
    so any objects created during the rest of this update cycle will be in the old scene and not the new scene.

   :param kwargs: Keyword arguments that should be passed to the resumed scene's handler function.

Scene Handlers
--------------

Scene handlers are functions designed to manage specific actions and events within a scene. They correspond
to regular event handlers, but have a colon specifying what scene (or scenes) they are associated with.
Events bound to a scene will only fire during those scenes.

The syntax for scene handlers is ``"event_name: scene_name"``. For example, a handler for handling mouse clicks
in the overworld scene would be ``"clicking: overworld"``. The other `event <event>`_ handlers work the same way.

The event names follow a specific pattern, denoting the scene and the event type:

- ``'starting: <scene_name>'``: When a scene is being initialized.
- ``'clicking: <scene_name>'``: When a clicking event is detected in a scene.
- ``'entering: <scene_name>'``: When a scene is being resumed or entered.

Scene Parameters
----------------

When creating or transitioning to a scene, you can provide keyword arguments that will be passed to the scene's
``starting`` or ``entering`` handlers. This allows you to pass data between scenes. You can also have shared basic objects,
but that's mutabilty and you should be afraid of it. Much better to pass around mutable data.

Don't try to pass designer objects across scenes, though! That won't work. Probably. I don't even know what it will do, to be honest.