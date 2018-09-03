import sys
import threading
import tkFont
from ScrolledText import *

from pynestml_editor.highlighter import Highlighter
from pynestml_editor.menu import Menu
from pynestml_editor.model_checker import ModelChecker

if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk


class EditorMain(object):

    def __init__(self):
        self.root = tk.Tk(className="PyNestML IDE")
        self.after_id = None

        self.text_frame = tk.Frame(self.root, width=self.root.winfo_screenwidth(),
                                   height=self.root.winfo_screenheight() * 0.70)
        self.text_frame.pack_propagate(False)
        self.textPad = ScrolledText(self.text_frame, height=1, width=1, undo=True)
        self.textPad.pack(side="top", fill="both", expand=True)
        self.text_frame.pack(side="top", fill="both", expand=True)

        self.line_nr_frame = tk.Frame(self.root, width=self.root.winfo_screenwidth())
        self.line_nr_frame.pack_propagate(False)
        self.line_nr = tk.Text(self.root, width=self.root.winfo_screenwidth(), height=1)
        self.line_nr.pack(side="top", fill="both", expand=True)
        self.line_nr_frame.pack(side="top", fill="both", expand=True)

        self.console_frame = tk.Frame(self.root, width=self.root.winfo_screenwidth(),
                                      height=self.root.winfo_screenheight() * 0.20)
        self.console_frame.pack_propagate(False)
        self.console = ScrolledText(self.console_frame, width=1, height=1)
        self.console.pack(side="top", fill="both", expand=True)
        self.console_frame.pack(side="top", fill="both", expand=True)

        self.menu = Menu(root=self.root, text_pad=self.textPad, editor=self)
        self.highlighter = Highlighter(self.textPad, self)

        # insert empty model
        self.textPad.insert('1.0', 'PyNestML             \n')
        self.textPad.insert('2.0', '         Model       \n')
        self.textPad.insert('3.0', '               Editor\n')
        self.textPad.tag_add("l1", "%s.%s" % (1, 0), "%s.%s" % (1, len('PyNestML')))
        self.textPad.tag_add("l2", "%s.%s" % (2, 0), "%s.%s" % (2, len('         Model')))
        self.textPad.tag_add("l3", "%s.%s" % (3, 0), "%s.%s" % (3, len('               Editor')))
        self.textPad.tag_config("l1", background="white", foreground="blue")
        self.textPad.tag_config("l2", background="white", foreground="red")
        self.textPad.tag_config("l3", background="white", foreground="green")
        self.last = self.textPad.get('0.0', tk.END)
        # insert start position of cursor
        self.console.pack(side=tk.BOTTOM)
        self.console.configure(state='disabled')
        self.line_nr.insert('1.0', 'Position: 0:0')
        self.line_nr.configure(state='disabled')
        # bind keys
        self.bind_keys()
        self.root.mainloop()

    def change_button_state(self, active = True):
        if not active:
            self.menu.modelmenu.entryconfig('Check CoCos', state=tk.DISABLED)
            self.menu.modelmenu.entryconfig('Compile Model', state=tk.DISABLED)
        else:
            self.menu.modelmenu.entryconfig('Check CoCos', state=tk.NORMAL)
            self.menu.modelmenu.entryconfig('Compile Model', state=tk.NORMAL)

    def exit_editor(self, _):
        self.menu.exit_command()

    def store_command(self, _):
        self.menu.save_command()

    def check_model(self):
        self.change_button_state(False)
        thread = threading.Thread(target=self.check_model_in_separate_thread)
        thread.start()
        return thread  # returns immediately after the thread starts

    def check_model_in_separate_thread(self):
        self.textPad.configure(state='disabled')
        ModelChecker.check_model_with_cocos(self.textPad.get('0.0', tk.END))
        self.report_findings()
        self.textPad.configure(state='normal')

    def check_syntax_in_separate_thread(self):
        ModelChecker.check_model_syntax(self.textPad.get('0.0', tk.END))
        self.report_findings()

    def check_model_syntax(self, _):
        self.update_line_number()
        # cancel the old job
        if self.after_id is not None:
            self.textPad.after_cancel(self.after_id)

        # create a new job
        self.after_id = self.textPad.after(800, self.do_check_model_syntax)

    def do_check_model_syntax(self):
        if self.textPad.get('0.0', tk.END) != self.last:
            if self.last is None or "".join(self.textPad.get('0.0', tk.END).split()) != "".join(self.last.split()):
                thread = threading.Thread(target=self.check_syntax_in_separate_thread)
                thread.start()
                self.last = self.textPad.get('0.0', tk.END)
                return thread  # returns immediately after the thread starts

    def update_line_number(self):
        self.line_nr.configure(state='normal')
        self.line_nr.delete('1.0', tk.END)
        pos = self.textPad.index(tk.INSERT).split('.')
        self.line_nr.insert('1.0', 'Position: %s:%s' % (pos[0], pos[1]))
        self.line_nr.configure(state='disabled')

    def report_findings(self):
        # print('process complete!')
        self.highlighter.process_report()
        self.change_button_state(True)

    def bind_keys(self):
        # bind the events
        self.textPad.bind('<Control-q>', self.exit_editor)
        self.textPad.bind('<KeyRelease>', self.check_model_syntax)
        self.textPad.bind('<Control-s>', self.store_command)

    def clear_console(self):
        self.console.delete('1.0', tk.END)

    def report(self, text):
        if self.menu.show_syntax_errors_var.get() == 1:
            self.console.configure(state='normal')
            self.console.insert(tk.END, text + '\n')
            self.console.configure(state='disabled')

    def inc_font_size(self):
        f = tkFont.Font(self.textPad, self.textPad.cget('font'))
        self.textPad.configure(font=("Courier", f.configure()['size'] + 1))

    def dec_font_size(self):
        f = tkFont.Font(self.textPad, self.textPad.cget('font'))
        if not f.configure()['size'] - 1 < 4:
            self.textPad.configure(font=("Courier", f.configure()['size'] - 1))


if __name__ == '__main__':
    editor = EditorMain()

"""
chk_state = BooleanVar()

chk_state.set(True) #set check state

chk = Checkbutton(window, text='Choose', var=chk_state)

chk.grid(column=0, row=0)
"""
