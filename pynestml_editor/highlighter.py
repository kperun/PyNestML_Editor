class Highlighter(object):
    # create a menu & define functions for each menu item

    def color_text_error(self, text, start_line, start_column, end_line, end_column):
        text.tag_add("error", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        text.tag_config("error", background="red", foreground="black")

    def color_text_warning(self, text, start_line, start_column, end_line, end_column):
        text.tag_add("warning", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        text.tag_config("warning", background="yellow", foreground="black")

    def color_default(self, text, start_line, start_column, end_line, end_column):
        text.tag_add("default", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        text.tag_config("default", background="yellow", foreground="black")
