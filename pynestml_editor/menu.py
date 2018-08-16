import tkFileDialog
import tkMessageBox
import sys

if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk


class MenuSetup(object):
    def __init__(self, root, text_pad):
        self.root = root
        self.textPad = text_pad
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.__add_file_menu()
        self.__add_help_menu()

    def __open_command(self):
        file_handler = tkFileDialog.askopenfile(parent=self.root, mode='rb', title='Select a file')
        if file_handler is not None:
            contents = file_handler.read()
            self.textPad.delete('1.0', tk.END)
            self.textPad.insert('1.0', contents)
            file_handler.close()
        # print(textPad.get("1.0","2.0")) returns the text as unicode

    def __save_command(self):
        file_handler = tkFileDialog.asksaveasfile(mode='w')
        if file_handler is not None:
            # slice off the last character from get, as an extra return is added
            data = self.textPad.get('1.0', tk.END + '-1c')
            file_handler.write(data)
            file_handler.close()

    def exit_command(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def __about_command(self):
        label = tkMessageBox.showinfo("PyNestML Editor", "TODO")

    def __new_command(self):
        file_path = None
        file_handler = tkFileDialog.asksaveasfile(mode='w')
        if file_handler is not None:
            # slice off the last character from get, as an extra return is added
            data = self.textPad.get('1.0', tk.END + '-1c')
            file_handler.write(data)
            file_path = file_handler.name
            file_handler.close()
        if file_path is not None:
            with open(file_path, 'r') as f:
                self.textPad.delete('1.0', tk.END)
                self.textPad.insert('1.0', f.read())

    def __add_file_menu(self):
        filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.__new_command)
        filemenu.add_command(label="Open...", command=self.__open_command)
        filemenu.add_command(label="Save", command=self.__save_command)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_command)

    def __add_help_menu(self):
        helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.__about_command)
