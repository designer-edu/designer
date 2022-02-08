Change Log
==========

# Version 0.2.0

* Removed all use of `weakref` for compatibility with BlockPy
* Added `emoji` function
* Added `pen` function
* Created all the Movement functions to manipulate attributes with functions

# Version 0.1.7

* Add in `lines` to replace old `shape` behavior
* Allow keyboard keys to be hashable
* Fix `shape` to work correctly
* Fix bug in handling image rotation

# Version 0.1.6

* Fix bug in __neg__ of Vec2D

# Version 0.1.5

* Fix issue where static blits were not being finalized in a timely fashion

# Version 0.1.4

* Fix bug in events for scrolling/touch
* Add in `disable_keyboard_repeating` and `enable_keyboard_repeating`

# Version 0.1.3

* Added support for `background_music` and `play_sound`
* Added support for `get_mouse_x` and `get_mouse_y`

# Version 0.1.2

* Fix `image` not keeping its size up-to-date
* Fix `image` not loading filename attribute changes correctly
* Remove memory leak from initial game state

# Version 0.1.1

* Event handlers now accept positionally-specified arguments instead of requiring a specific name
* The `event` parameter for handlers provides a dictionary-like object with all the event keys

# Version 0.1.0

* Initial release of core game dev functionality