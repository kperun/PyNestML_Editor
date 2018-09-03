import sys

from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_functions import PredefinedFunctions
import re

if sys.version_info < (3, 0):
    import Tkinter as tk
else:
    import tkinter as tk


class Highlighter(object):
    # create a menu & define functions for each menu item

    def __init__(self, text, editor):
        self.text = text
        self.editor = editor
        self.pat = re.compile("[0-9.]+|[a-zA-Z_]+")

    def color_comment(self, sl, sc, el, ec):
        name = "comment%s.%s.%s.%s." % (sl, sc, el, ec)
        self.text.tag_add(name, "%s.%s" % (sl, sc), "%s.%s" % (el, ec))
        self.text.tag_config(name, background="white", foreground="grey", selectbackground="#ededed")

    def color_type(self, sl, sc, el, ec):
        name = "comment%s.%s.%s.%s." % (sl, sc, el, ec)
        self.text.tag_add(name, "%s.%s" % (sl, sc), "%s.%s" % (el, ec))
        self.text.tag_config(name, background="white", foreground="green", selectbackground="#ededed")

    def color_text_error(self, start_line, start_column, end_line, end_column):
        self.text.tag_add("error", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        self.text.tag_config("error", background="#f44277", foreground="black")

    def color_text_warning(self, start_line, start_column, end_line, end_column):
        self.text.tag_add("warning", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        self.text.tag_config("warning", background="#fbff3f", foreground="black")

    def color_default(self, start_line, start_column, end_line, end_column):
        self.text.tag_add("default", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        self.text.tag_config("default", background="white", foreground="black")

    def process_report(self):
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)
        self.color_components()
        self.editor.clear_console()
        counter = 1
        for (artifact_name, neuron, log_level, code, error_position, message) in Logger.log.values():
            self.editor.report('[%s]%s@%s: %s' % (counter, log_level.name,
                                                  error_position if error_position is not None else 'GLOBAL',
                                                  message))
            counter += 1
            if error_position is None:  # this is only a general information, thus no reporting
                continue

            if self.__check_if_point(error_position):
                offset = self.__get_complete_word_len(error_position)
            else:
                offset = 0

            if log_level == LoggingLevel.WARNING:
                self.color_text_warning(error_position.start_line, error_position.start_column,
                                        error_position.end_line, error_position.end_column + offset)
            elif log_level == LoggingLevel.ERROR:
                # print(error_position)
                self.color_text_error(error_position.start_line, error_position.start_column,
                                      error_position.end_line, error_position.end_column + offset)

    def __check_if_point(self, error_position):
        return error_position.start_line == error_position.end_line and \
               error_position.start_column == error_position.end_column

    def __get_complete_word_len(self, error_position):
        complete_text_as_lines = self.text.get('1.0', tk.END + '-1c').splitlines()
        ret = ''
        if error_position.start_line - 1 > len(complete_text_as_lines):
            return 0
        for c in complete_text_as_lines[error_position.start_line - 1][error_position.start_column:]:
            if c != ' ':
                ret += c
            else:
                break
        return len(ret)

    def color_components(self):
        complete_text_as_lines = self.text.get('1.0', tk.END + '-1c').splitlines()
        active = False
        for number, line in enumerate(complete_text_as_lines):
            last_start_index = -1
            if '#' in line:
                s_l = number + 1
                s_c = line.index('#')
                e_l = s_l
                e_c = len(line)
                self.color_comment(s_l, s_c, e_l, e_c)
            if '/*' in line and '*/' in line:
                s_l = number + 1
                s_c = line.index('/*')
                e_l = s_l
                e_c = line.index('*/') + 2
                self.color_comment(s_l, s_c, e_l, e_c)
            elif '/*' in line:
                active = True
                s_l = number + 1
                s_c = line.index('/*')
                e_l = s_l
                e_c = len(line)
                self.color_comment(s_l, s_c, e_l, e_c)
            elif '*/' in line:
                active = False
                s_l = number + 1
                s_c = 0
                e_l = s_l
                e_c = line.index('*/') + 2
                self.color_comment(s_l, s_c, e_l, e_c)
            elif active:
                s_l = number + 1
                s_c = 0
                e_l = s_l
                e_c = len(line)
                self.color_comment(s_l, s_c, e_l, e_c)
            for index, word in enumerate(self.pat.findall(line)):
                s_l = number + 1
                s_c = line.find(word)#todo
                e_l = s_l
                e_c = s_c + len(word)
                if self.editor.textPad.tag_names('%s.%s' % (s_l, s_c)):
                    continue

                if word in PredefinedTypes.get_types():
                    last_start_index = s_c
                    print(word + '@' + str(s_l) + '_' + str(s_c) + ' in ' + str(self.pat.findall(line)))
                    self.color_type(s_l, s_c, e_l, e_c)
