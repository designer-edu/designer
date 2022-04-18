import tkinter as Tkinter
from tkinter import font
from designer.core.event import register, unregister
from pprint import pformat

class DebugWindow:
    def __init__(self, director):
        self.director = director
        self.root = Tkinter.Tk()
        self.root.title("Debug Designer")
        self.main_dialog = Tkinter.Frame(self.root)

        status_str = "Status"
        self.status_line = Tkinter.Label(self.main_dialog,
                                         text=status_str,
                                         bd=1,
                                         relief=Tkinter.SUNKEN,
                                         anchor=Tkinter.W,
                                         justify='left',
                                         font=font.nametofont("TkFixedFont"))
        self.status_line.pack(side=Tkinter.TOP, fill=Tkinter.X, anchor='w')
        self.main_dialog.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)

        register("updating", self.update_window)

    def update_window(self):
        world = pformat(self.director._game_state, indent=2)
        self.status_line.config(text=f"{world}")
        try:
            self.main_dialog.update()
        except Exception as e:
            print("Debug mode encountered an error with TKinter: "+str(e))

    def destroy(self):
        self.director.stop_debug_mode()
        unregister('updating', self.update_window)
        self.root.destroy()
