import weakref
from typing import Optional

import pygame
import time
import operator
import inspect
import sys

import designer
from itertools import chain

from designer.core.event import COMMON_EVENT_NAME_LOOKUP, get_positional_event_parameters
from designer.core.internal_image import InternalImage
from designer.utilities.layer_tree import _LayerTree
from collections import defaultdict
from weakref import ref as _wref, WeakSet, WeakKeyDictionary, WeakMethod
from designer.utilities.weak_method import WeakMethodBound, DeadFunctionError
from designer.core.clock import GameClock


def _has_value(obj, collect):
    for item in collect:
        if obj is item:
            return True
        elif isinstance(item, dict) and obj in item.values():
            return True
        elif isinstance(item, tuple) and obj in item:
            return True
    return False


class Window:
    """
    Creates a new Window. When a window is not active, no events will be processed
    for it. Windows are the basic units that are executed by Designer for your game,
    and can be subclassed and filled in with code which is relevant to your
    game. The :class:`Director <designer.core.designer.Director>`, is a manager for Windows,
    which maintains a stack and actually executes their code. There is always at least
    one default window, unless the game has ended.

    :param size: The `size` of the window internally (or "virtually"). This is
                 the coordinate space that you place Sprites in, but it does
                 not have to match up 1:1 to the window (which could be scaled).
    :type size: width, height
    :param int max_ups: Maximum updates to process per second. By default,
                        `max_ups` is pulled from the director.
    :param int max_fps: Maximum frames to draw per second. By default,
                        `max_fps` is pulled from the director.
    """

    def __init__(self, size=None, max_ups=None, max_fps=None):
        time_source = time.time
        self.clock = GameClock(
            time_source=time_source,
            max_fps=max_fps or designer.GLOBAL_DIRECTOR.fps,
            max_ups=max_ups or designer.GLOBAL_DIRECTOR.fps)
        self.clock.use_wait = True

        self._handlers = defaultdict(lambda: [])
        self._namespaces = set()
        self._event_source = designer.core.event.LiveEventHandler()
        self._handling_events = False
        self._events = []
        self._pending = []
        self._debug = True

        self._scale = designer.utilities.vector.Vec2D(1.0, 1.0)  # None
        self._surface = pygame.display.get_surface()
        display_size = self._surface.get_size()
        if size is not None:
            self.size = size
        else:
            self.size = display_size
        self._background: Optional[InternalImage] = None
        self._background_image = InternalImage(size=display_size)
        self._background_image.fill(designer.GLOBAL_DIRECTOR._window_color)
        self._background_version = 0
        self._surface.blit(self._background_image._surf, (0, 0))

        self._blits = []
        self._dirty_rects = []
        self._clear_this_frame = []
        self._clear_next_frame = []
        self._soft_clear = []
        self._static_blits = WeakKeyDictionary()
        self._invalidating_views = {}
        self._collision_boxes = WeakKeyDictionary()
        self._rect = self._surface.get_rect()

        self._layers = []
        self._child_views = []
        self._layer_tree = _LayerTree(self)
        self._objects = WeakSet()

        # View interface
        self._window = _wref(self)
        self._views = []

        self._events_activated = False

    def _register_default_events(self):
        if not self._events_activated:
            designer.core.event.register('director.window.enter', self.redraw)
            designer.core.event.register('director.update', self._handle_events)
            designer.core.event.register('system.focus_change', self.redraw)
            designer.core.event.register('system.video_resize', self.redraw)
            designer.core.event.register('system.video_expose', self.redraw)
            designer.core.event.register('designer.internal.view.changed', self._invalidate_views)
            self._events_activated = True

    # Event Handling
    def _queue_event(self, event_name, event=None):
        """
        Internal method to add a new `event` to be handled by this window.

        :param str event_name: The name of the event to queue
        :param event: Metadata about this event.
        :type event: :class:`Event <designer.core.event.Event>`
        """
        if self._handling_events:
            self._pending.append((event_name, event))
        else:
            self._events.append((event_name, event))

    def _reg_internal(self, namespace, handlers, args,
                      kwargs, priority, dynamic):
        """
        Convenience method for registering a new event; other variations
        exist to keep the signature convenient and easy.
        """
        if namespace.endswith(".*"):
            namespace = namespace[:-2]
        self._namespaces.add(namespace)
        for handler in handlers:
            self._handlers[namespace].append((handler, args, kwargs,
                                              priority, dynamic))
        self._handlers[namespace].sort(key=operator.itemgetter(3))

    def _get_namespaces(self, namespace):
        """
        Internal method for returning all the registered namespaces that are in
        the given namespace.
        """
        return [n for n in self._namespaces if (namespace == n or
                                                n.rsplit(".", 1)[0].startswith(namespace) or
                                                namespace.rsplit(".", 1)[0].startswith(n))]

    def _send_event_to_handler(self, event, event_type, handler: callable, args,
                               kwargs, priority, dynamic):
        """
        Internal method to dispatch events to their handlers.
        """
        def _get_arg_val(arg, default=inspect.Parameter.empty, index=None):
            if arg == 'event':
                return event
            elif hasattr(event, arg):
                return getattr(event, arg)
            else:
                #print("MISSING?", event, arg, default, fillval, type, dir(event))
                if default != inspect.Parameter.empty:
                    return default
                positional_parameters = get_positional_event_parameters(event_type, event)
                if index < len(positional_parameters):
                    return getattr(event, positional_parameters[index])
                friendly_event_name = COMMON_EVENT_NAME_LOOKUP.get(event_type, event_type)
                suggestions = ", ".join(map(repr, [k for k in dir(event) if not k.startswith("__")]))
                raise TypeError(f"Your event handler function expected a parameter named {arg!r}, but "
                                f"the event {friendly_event_name!r} does not provide an argument with that name. "
                                f"The parameters allowed for this event are: {suggestions}")

        if dynamic is True:
            original_handler = handler
            handler = self
            for piece in original_handler.split("."):
                handler = getattr(handler, piece, None)
                if handler is None:
                    return
        if handler is sys.exit and args is None and kwargs is None:
            # Dirty hack to deal with python builtins
            args = []
            kwargs = {}
        elif args is None and kwargs is None:
            # Autodetect the arguments
            try:
                funct = handler.func
            except AttributeError as e:
                funct = handler
            try:
                signature = inspect.signature(funct)
            except Exception as e:
                raise Exception(("Unfortunate Python Problem! "
                                 f"{handler} isn't supported by Python's "
                                 "inspect module! Oops."))
            # TODO: Handle all parameters elegantly
            h_args = [p.name for p in signature.parameters.values()]
            h_defaults = [p.default for p in signature.parameters.values()] or tuple()
            if len(h_args) > 0 and 'self' == h_args[0]:
                h_args.pop(0)
            d = len(h_args) - len(h_defaults)
            if d > 0:
                h_defaults = [inspect.Parameter.empty] * d + list(*h_defaults)
            args = [_get_arg_val(arg, default, index) for index, (arg, default)
                    in enumerate(zip(h_args, h_defaults))]
            kwargs = {}
        elif args is None:
            args = []
            kwargs = dict([(arg, _get_arg_val(arg)) for arg in kwargs])
        else:
            args = [_get_arg_val(arg) for arg in args]
            kwargs = {}
        if handler is not None:
            return handler(*args, **kwargs)

    def _handle_event(self, event_type, event=None, collect_results=False):
        """
        For a given event, send the event information to all registered handlers
        """
        handlers = chain.from_iterable(self._handlers[namespace]
                                       for namespace
                                       in self._get_namespaces(event_type))
        result = [] if collect_results else None
        for handler_info in handlers:
            try:
                new_result = self._send_event_to_handler(event, event_type, *handler_info)
            except DeadFunctionError:
                new_result = None
            if new_result is not None:
                if collect_results:
                    result.append(new_result)
                else:
                    result = new_result
            if result is False:
                return result
        return result

    def _handle_events(self):
        """
        Run through all the events and handle them.
        """
        self._handling_events = True
        do = True
        while do or len(self._pending) > 0:
            do = False
            for (type, event) in self._events:
                self._handle_event(type, event)
            self._events = self._pending
            self._pending = []

    def _unregister_object_events(self, object):
        for name, handlers in self._handlers.items():
            self._handlers[name] = [h for h in handlers
                                    if (not isinstance(h[0], WeakMethod)
                                        or h[0].weak_object_ref() is not object)]
            if not self._handlers[name]:
                del self._handlers[name]

    def _unregister(self, event_namespace, handler):
        """
        Unregisters a registered handler for that namespace. Dynamic handler
        strings are supported as well. For more information, see
        `Event Namespaces`_.

        :param str event_namespace: An event namespace
        :param handler: The handler to unregister.
        :type handler: a function or string.
        """
        if event_namespace.endswith(".*"):
            event_namespace = event_namespace[:-2]
        self._handlers[event_namespace] = [h for h
                                           in self._handlers[event_namespace]
                                           if ((not isinstance(h[0], WeakMethod) and handler != h[0])
                                               or (isinstance(h[0], WeakMethod)
                                                   and ((h[0].func is not handler.__func__)
                                                        or (h[0].weak_object_ref() is not handler.__self__))))]
        if not self._handlers[event_namespace]:
            del self._handlers[event_namespace]

    def _clear_namespace(self, namespace):
        """
        Clears all handlers from namespaces that are at least as specific as the
        provided `namespace`. For more information, see `Event Namespaces`_.

        :param str namespace: The complete namespace.
        """
        if namespace.endswith(".*"):
            namespace = namespace[:-2]
        ns = [n for n in self._namespaces if n.startswith(namespace)]
        for namespace in ns:
            del self._handlers[namespace]

    def _clear_all_events(self):
        """
        Completely clear all registered events for this window. This is a very
        dangerous function, and should almost never be used.
        """
        self._handlers.clear()

    def _get_event_source(self):
        """
        The event source can be used to control event playback. Although
        normally events are given through the operating system, you can enforce
        events being played from a file; there is also a mechanism for recording
        events to a file.
        """
        return self._event_source

    def _set_event_source(self, source):
        self._event_source = source

    # Rendering
    @property
    def size(self):
        """
        Read-only property that returns a :class:`Vec2D <designer.utilities.vector.Vec2D>` of the
        width and height of the Window's size.  This is the coordinate space that
        you place Sprites in, but it does not have to match up 1:1 to the window
        (which could be scaled). This property can only be set once.
        """
        return self._size

    @size.setter
    def size(self, value):
        # This can only be called once.
        rsize = self._surface.get_size()
        self._size = value
        self._scale = (rsize[0] / value[0],
                       rsize[1] / value[1])

    @property
    def width(self):
        """
        The width of this window. Read-only number.
        """
        return self.size[0]

    @property
    def height(self):
        """
        The height of this window. Read-only number.
        """
        return self.size[1]

    @property
    def rect(self):
        """
        Returns a :class:`Rect <spyral.Rect>` representing the position (0, 0)
        and size of this Window.
        """
        return designer.utilities.rect.Rect((0, 0), self.size)

    @property
    def window(self):
        """
        Returns this window. Read-only.
        """
        return self._window()

    @property
    def parent(self):
        """
        Returns this window. Read-only.
        """
        return self._window()

    @property
    def background(self):
        """
        The background of this window. The given :class:`InternalImage <designer.core.internal_image.InternalImage>`
        must be the same size as the Window. A background will be handled
        intelligently by Spyral; it knows to only redraw portions of it rather
        than the whole thing, unlike a Sprite.
        """
        return self._background_image

    @background.setter
    def background(self, image: InternalImage):
        if self.size != image.size:
            image.scale(self.size)
        self._background_image = image
        self._background_version = image._version
        surface = image._surf
        size = self._surface.get_size()
        self._background = pygame.transform.smoothscale(surface, size)
        self._clear_this_frame.append(self._background.get_rect())


    def _register_object(self, object):
        """
        Internal method to add this object to the window
        """
        self._objects.add(object)
        # Add the view and its parents to the invalidating_views for the object
        parent_view = object._parent()
        while parent_view != self:
            if parent_view not in self._invalidating_views:
                self._invalidating_views[parent_view] = set()
            self._invalidating_views[parent_view].add(object)
            parent_view = parent_view.parent

    def _unregister_object(self, object):
        """
        Internal method to remove this object from the window
        """
        if object in self._objects:
            self._objects.remove(object)
        if object in self._collision_boxes:
            del self._collision_boxes[object]
        for view in self._invalidating_views.keys():
            self._invalidating_views[view].discard(object)
        self._unregister_object_events(object)

    def _destroy_view(self, view):
        """
        Remove all references to the view from within this Window.
        """
        if view in self._invalidating_views:
            del self._invalidating_views[view]
        if view in self._collision_boxes:
            del self._collision_boxes[view]
        self._layer_tree.remove_view(view)

    def _blit(self, blit):
        """
        Apply any scaling associated with the Window to the Blit, then finalize
        it. Note that Window's don't apply cropping.
        """
        blit.apply_scale(self._scale)
        blit.finalize()
        self._blits.append(blit)

    def _static_blit(self, key, blit):
        """
        Identifies that this object will be statically blit from now, and
        applies scaling and finalization to the blit.
        """
        blit.apply_scale(self._scale)
        blit.finalize()
        self._static_blits[key] = blit
        #weakref.finalize(key, self._remove_static_blit, key)
        #weakref.finalize(key, print, "YOU KILLED", key)
        self._clear_this_frame.append(blit.rect)

    def _invalidate_views(self, view):
        """
        Expire any objects that belong to the view being invalidated.
        """
        if view in self._invalidating_views:
            for object in self._invalidating_views[view]:
                object._expire_static()

    def _remove_static_blit(self, key):
        """
        Removes this object from the static blit list
        """
        try:
            x = self._static_blits.pop(key)
            self._clear_this_frame.append(x.rect)
        except:
            pass

    def _draw(self):
        """
        Internal method that is called by the
        :class:`Director <designer.core.director.Director>` at the end of every .render() call
        to do the actual drawing.
        """

        # This function sits in a potential hot loop
        # For that reason, some . lookups are optimized away
        screen = self._surface

        # First we test if the background has been updated
        if self._background_version != self._background_image._version:
            self.background = self._background_image

        # Let's finish up any rendering from the previous frame
        # First, we put the background over all blits
        x = self._background.get_rect()
        for i in self._clear_this_frame + self._soft_clear:
            i = x.clip(i)
            b = self._background.subsurface(i)
            screen.blit(b, i)

        # Now, we need to blit layers, while simultaneously re-blitting
        # any static blits which were obscured
        static_blits = len(self._static_blits)
        dynamic_blits = len(self._blits)
        blits = list(self._static_blits.values()) + self._blits
        blits.sort(key=operator.attrgetter('layer'))

        # Clear this is a list of things which need to be cleared
        # on this frame and marked dirty on the next
        clear_this = self._clear_this_frame
        # Clear next is a list which will become clear_this on the next
        # draw cycle. We use this for non-static blits to say to clear
        # That spot on the next frame
        clear_next = self._clear_next_frame
        # Soft clear is a list of things which need to be cleared on
        # this frame, but unlike clear_this, they won't be cleared
        # on future frames. We use soft_clear to make things static
        # as they are drawn and then no longer cleared
        soft_clear = self._soft_clear
        self._soft_clear = []
        screen_rect = screen.get_rect()
        drawn_static = 0

        blit_flags_available = pygame.version.vernum < (1, 8)

        for blit in blits:
            blit_rect = blit.rect
            blit_flags = blit.flags if blit_flags_available else 0
            # If a blit is entirely off screen, we can ignore it altogether
            if not screen_rect.contains(blit_rect) and not screen_rect.colliderect(blit_rect):
                continue
            # If this is a static blit...
            if blit.static:
                skip_soft_clear = False
                for rect in clear_this:
                    if blit_rect.colliderect(rect):
                        # One of the rects (needing to be cleared this frame and marked dirty on the next)
                        # is colliding with the current static blit's rect
                        # so we blit this static blit onto the screen and then add this static blit to the
                        # _soft_clear for next time
                        screen.blit(blit.surface, blit_rect, None, blit_flags)
                        skip_soft_clear = True
                        clear_this.append(blit_rect)
                        self._soft_clear.append(blit_rect)
                        drawn_static += 1
                        break
                if skip_soft_clear:
                    continue
                for rect in soft_clear:
                    if blit_rect.colliderect(rect):
                        screen.blit(blit.surface, blit_rect, None, blit_flags)
                        soft_clear.append(blit.rect)
                        drawn_static += 1
                        break
            else:
                if screen_rect.contains(blit_rect):
                    r = screen.blit(blit.surface, blit_rect, None, blit_flags)
                    clear_next.append(r)
                elif screen_rect.colliderect(blit_rect):
                    # Todo: See if this is ever called. Shouldn't be.
                    x = blit.rect.clip(screen_rect)
                    y = x.move(-blit_rect.left, -blit_rect.top)
                    b = blit.surface.subsurface(y)
                    r = screen.blit(blit.surface, blit_rect, None, blit_flags)
                    clear_next.append(r)

        if designer.GLOBAL_DIRECTOR.window_title is None:
            pygame.display.set_caption("%d / %d static, %d dynamic. %d ups, %d fps" %
                                      (drawn_static, static_blits,
                                       dynamic_blits, self.clock.ups,
                                       self.clock.fps))
        # Do the display update
        pygame.display.update(self._clear_next_frame + self._clear_this_frame)
        # Get ready for the next call
        self._clear_this_frame = self._clear_next_frame
        self._clear_next_frame = []
        self._blits = []

    def redraw(self):
        """
        Force the entire visible window to be completely redrawn.
        """
        self._clear_this_frame.append(pygame.Rect(self._rect))

    def _get_layer_position(self, view, layer):
        """
        For the given view and layer, calculate its position in the depth order.
        """
        return self._layer_tree.get_layer_position(view, layer)

    def _set_view_layer(self, view, layer):
        """
        Set the layer that the view is on within layer tree.
        """
        self._layer_tree.set_view_layer(view, layer)

    def _set_view_layers(self, view, layers):
        """
        Set the view's layers within the layer tree.
        """
        self._layer_tree.set_view_layers(view, layers)

    def _add_view(self, view):
        """
        Register the given view within this window.
        """
        self._layer_tree.add_view(view)

    @property
    def layers(self):
        """
        A list of strings representing the layers that are available for this
        window. The first layer is at the bottom, and the last is at the top.

        Note that the layers can only be set once.
        """
        return self._layers

    @layers.setter
    def layers(self, value):
        """
        Potential caveat: If you change layers after blitting, previous blits
        may be wrong for a frame, static ones wrong until they expire
        """
        if self._layers == []:
            self._layer_tree.set_view_layers(self, value)
            self._layers = value
        elif self._layers == value:
            pass
        else:
            raise Exception("You can only define the layers for a window once.")

    def _add_child(self, entity):
        """
        Add this child to the Window; since only Views care about their children,
        this function does nothing.
        """
        pass

    def _remove_child(self, entity):
        """
        Remove this child to the Window; since only Views care about their
        children, this function does nothing.
        """
        pass

    def _warp_collision_box(self, box):
        """
        Finalize the collision box. Don't apply scaling, because that's only
        for external rendering purposes.
        """
        box.finalize()
        return box

    def _set_collision_box(self, entity, box):
        """
        Registers the given entity (a View or Sprite) with the given
        CollisionBox.
        """
        self._collision_boxes[entity] = box

    def collide_objects(self, first, second):
        """
        Returns whether the first object is colliding with the second.

        :param first: A object or view
        :type first: :class:`DesignerObject <designer.objects.designer_object.DesignerObject>` or a
                     :class:`View <spyral.View>`
        :param second: Another object or view
        :type second: :class:`DesignerObject <designer.objects.designer_object.DesignerObject>` or a
                      :class:`View <spyral.View>`
        :returns: A ``bool``
        """
        if first not in self._collision_boxes or second not in self._collision_boxes:
            return False
        first_box = self._collision_boxes[first]
        second_box = self._collision_boxes[second]
        return first_box.collide_rect(second_box)

    def collide_point(self, obj, *args):
        """
        Returns whether the object is colliding with the point.

        :param obj: A DesignerObject
        :type obj: :class:`DesignerObject <designer.objects.designer_object.DesignerObject>`
        :param point: A point
        :type point: :class:`Vec2D <spyral.Vec2D>`
        :returns: A ``bool``
        """
        point = args
        if len(args) == 2:
            point = (args[0], args[1])
        elif len(args) != 1:
            raise ValueError(f"Incorrect number of arguments to collide_point: Expected x and y, got {args}")
        if obj not in self._collision_boxes:
            return False
        object_box = self._collision_boxes[obj]
        return object_box.collide_point(point)

    def collide_rect(self, obj, rect):
        """
        Returns whether the object is colliding with the rect.

        :param obj: A DesignerObject
        :type obj: :class:`DesignerObject <designer.objects.designer_object.DesignerObject>`
        :param rect: A rect
        :type rect: :class:`Rect <spyral.Rect>`
        :returns: A ``bool``
        """
        if obj not in self._collision_boxes:
            return False
        object_box = self._collision_boxes[obj]
        return object_box.collide_rect(rect)
