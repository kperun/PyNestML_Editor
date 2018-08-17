import sys
from ScrolledText import *
import threading
from pynestml_editor.highlighter import Highlighter
from pynestml_editor.menu import Menu
from pynestml_editor.model_checker import ModelChecker

if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk


class EditorMain(object):

    def __init__(self):
        self.root = tk.Tk(className=" Just another Text Editor")
        self.textPad = ScrolledText(self.root, width=self.root.winfo_screenwidth(),
                                    height=self.root.winfo_screenheight())
        self.menu = Menu(root=self.root, text_pad=self.textPad, editor=self)
        self.highlighter = Highlighter(self.textPad)

        self.textPad.insert('1.0','PyNestML             \n')
        self.textPad.insert('2.0','         Model       \n')
        self.textPad.insert('3.0','               Editor\n')
        self.textPad.tag_add("l1", "%s.%s" % (1, 0), "%s.%s" % (1, len('PyNestML')))
        self.textPad.tag_add("l2", "%s.%s" % (2, 0), "%s.%s" % (2, len('         Model')))
        self.textPad.tag_add("l3", "%s.%s" % (3, 0), "%s.%s" % (3, len('               Editor')))
        self.textPad.tag_config("l1", background="white", foreground="blue")
        self.textPad.tag_config("l2", background="white", foreground="red")
        self.textPad.tag_config("l3", background="white", foreground="green")

        self.textPad.pack()
        self.root.mainloop()

    def change_button_state(self, active = True):
        if not active:
            self.menu.menu.entryconfig('Check Model', state=tk.DISABLED)
            self.menu.menu.entryconfig('Compile Model', state=tk.DISABLED)
        else:
            self.menu.menu.entryconfig('Check Model', state=tk.NORMAL)
            self.menu.menu.entryconfig('Compile Model', state=tk.NORMAL)

    def exit_editor(self, _):
        self.menu.exit_command()

    def check_model(self):
        self.change_button_state(False)
        thread = threading.Thread(target=self.check_model_in_separate_thread)
        thread.start()
        return thread  # returns immediately after the thread starts

    def check_model_in_separate_thread(self):
        ModelChecker.check_model(self.textPad.get('0.0', tk.END))
        self.report_findings()

    def report_findings(self):
        print('process complete!')
        self.highlighter.process_report()
        self.change_button_state(True)

    def bind_keys(self):
        # bind the events
        self.textPad.bind('<Control-q>', self.exit_editor)


if __name__ == '__main__':
    editor = EditorMain()

"""
chk_state = BooleanVar()

chk_state.set(True) #set check state

chk = Checkbutton(window, text='Choose', var=chk_state)

chk.grid(column=0, row=0)
"""
