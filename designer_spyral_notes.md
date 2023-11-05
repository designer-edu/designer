There is one global director

The director has a list of scenes
    There is a default scene automatically created
    The current scene is in the "window"
    Popping off the last scene ends the game
    There is exactly one Global Director

A Scene can have any number of DesignerObjects
    A Scene can also have Views? Not done yet tho

A DesignerObject can be one of several possible subclasses
    A DesignerObject lives in a Scene and cannot escape it

A Scene has state, DesignerObjects, and Event handlers
    Changing a scene deactivates everything not in use
    Popping/replacing a scene means the old scene is lost, including its state