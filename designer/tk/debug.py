import tkinter as Tkinter
import sys

from designer.objects.designer_object import DesignerObject
from designer.core.event import register, unregister
from pprint import pformat


def stringify_state(world):
    if isinstance(world, (int, str, float, bool)):
        return repr(world)
    elif isinstance(world, (list, set, frozenset, tuple)):
        return repr([stringify_state(w) for w in world])
    elif isinstance(world, (dict,)):
        return pformat({k: stringify_state(v) for k, v in world.items()}, indent=2)
    elif isinstance(world, DesignerObject):
        return repr(world)


class DebugWindow:
    def __init__(self, director):
        self.director = director
        self.root = Tkinter.Tk()
        self.main_dialog = Tkinter.Frame(self.root)

        status_str = "Status"
        self.status_line = Tkinter.Label(self.main_dialog,
                                         text=status_str,
                                         bd=1,
                                         relief=Tkinter.SUNKEN,
                                         anchor=Tkinter.W,
                                         justify='left')
        self.status_line.pack(side=Tkinter.TOP, fill=Tkinter.X, anchor='w')
        self.main_dialog.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)

        register("updating", self.update_window)

    def update_window(self):
        world = stringify_state(self.director._game_state)
        self.status_line.config(text=f"{world}")
        try:
            self.main_dialog.update()
        except Exception as e:
            print("Debug mode encountered an error with TKinter: "+str(e))

    def destroy(self):
        self.director.stop_debug_mode()
        unregister('updating', self.update_window)
