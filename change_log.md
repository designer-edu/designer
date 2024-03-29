Change Log
==========

# Version 0.6.6

* Fixed it so that flipping a negatively scaled emoji will not crash the game.

# Version 0.6.5

* Added `resume` function to match `pause`

# Version 0.6.4

* Fixed bugs with animations' default values
* Fixed bugs with layer's weakref handling of set_window_layers

# Version 0.6.3

* Contributed by @codeBodger: allow custom fonts with font files

# Version 0.6.2

* Fixed bug with destroying designer objects leaving behind its render event (and therefore leaving it on the screen!)

# Version 0.6.1

* Fix error in designer object layers caused by the scene rewrite

# Version 0.6.0

* Allow simple layer values like 'top' and 'bottom' instead of requiring colon offsets
* `change_scene`, `push_scene`, and `pop_scene` now work!
* Use weakrefs for scenes and objects to avoid memory leaks
* Transition from "window" terminology back to "scenes"

# Version 0.5.0

* Allow inheritance for fields
* Created `would_collide` function

# Version 0.4.2

* The `restart` function was added to reset the game back to whatever the `starting` event sets up.

# Version 0.4.1

* Change sphinx theme to `cloud`
* Start porting some of the doc pages to have both dataclass and dictionary versions (arrows, worlds)
* Track version `__init__.py` so it is properly output in built docs
* Fix small bug in scaling surfaces' import

# Version 0.4.0

* Added in `beside` function, `get_text`, and `set_text` function
* New logo! Made with OpenAI's Dalle2 :)

# Version 0.3.9

* Fix bug with textbox width not updating
* Text input box example

# Version 0.3.8

* "Run Once" mode for director, activated by `draw` command in some environments (e.g., blockpy)
* Dataclass support, new example created
* First stab at pixel manipulation code (get_pixels function, creating images from pixels)
* Debug mode for dataclasses, pretty printing current state

# Version 0.3.7

* Fix bug with updating layer field
* Expose set_window_layers and get_window_layers
* Allow :top and :bottom layer modifiers
* Fix up layering system a little to actually work!
* Fix object destruction throwing errors when they had event handlers

# Version 0.3.6

* Fixed SVGs for macs (including previous cropping issue) for scale, rotate, and flip!

# Version 0.3.5

* The fix from 0.3.4 was too crude - there was a bug! Should hopefully be fixed.

# Version 0.3.4

* Crude fix for debug mode on Macs by preloading a Tkinter window

# Version 0.3.3

* Partial fix for rotating emojis on Mac (were partially cut off)

# Version 0.3.2

* Bug fix for debug window module not being included in release

# Version 0.3.1

* Bug fix for set_x/set_y to return the object and not the new position
* New feature: "Debug Window", renders current world as a pretty-printed string

# Version 0.3.0

* Minor bug fix (okay I left a `print` statement in, I'm sorry)

# Version 0.2.9

* Support missing event attributes when converting pygame events
* Allow more advanced Pygame versions than 2.0.1

# Version 0.2.8

* Fix scaling of emojis on Mac *again*, this time to handle repeated scaling moving the image

# Version 0.2.7

* Export `change_scale` correctly
* Expose `get_emoji_name` and `set_emoji_name` to avoid attributes
* Reorganized documentation
* Added Emoji Clicker tutorial

# Version 0.2.6

* Alias `set_background_image` to `set_window_image` for consistent vocabulary usage!
* Export `set_visible` correctly

# Version 0.2.5

* Fixed rotation for ellipses

# Version 0.2.4

* Fix cropping issue for `emoji` on mac due to SVG viewBox
* Remove unnecessary `print`
* Moved dev dependencies to `requirements_dev.txt`

# Version 0.2.3

* Layering now respects creation order within a layer
* Ignore capitalization for emojis

# Version 0.2.2

* Bugfix for turn_right and turn_left, added in a few missing functions
* Bugfix for point_towards functions, math was incorrect
* Added `emoji_clicker` example
* Fixed `group` to respect offsets
* Added `get_window_width`/`get_window_height`; make `get_width`/`get_height` work for windows AND objects

# Version 0.2.1

* Bugfix release with missing emoji datafiles

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