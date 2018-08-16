import sys
from pynestml_editor.menu import MenuSetup
from pynestml_editor.model_checker import ModelChecker
from ScrolledText import *

if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk


def check_model(text):
    print(text)

def exit_editor(_):
    menu.exit_command()

def bind_keys():
    # bind the events
    # textPad.bind('<KeyRelease>', check_model)
    # textPad.bind('<Enter>', check_model)
    textPad.bind('<Control-q>', exit_editor)


if __name__ == '__main__':
    root = tk.Tk(className=" Just another Text Editor")
    textPad = ScrolledText(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    menu = MenuSetup(root, textPad)
    textPad.pack()
    textPad.grid()
    ModelChecker.check_model(path='')
    # ----------
    textPad.insert(tk.INSERT, "Test " * 10)
    #---------
    root.mainloop()

"""
chk_state = BooleanVar()

chk_state.set(True) #set check state

chk = Checkbutton(window, text='Choose', var=chk_state)

chk.grid(column=0, row=0)
"""