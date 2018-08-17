class Highlighter(object):
    # create a menu & define functions for each menu item

    def __init__(self, text):
        self.text = text

    def color_text_error(self, start_line, start_column, end_line, end_column):
        self.text.tag_add("error", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        self.text.tag_config("error", background="red", foreground="black")

    def color_text_warning(self, start_line, start_column, end_line, end_column):
        self.text.tag_add("warning", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        self.text.tag_config("warning", background="yellow", foreground="black")

    def color_default(self, start_line, start_column, end_line, end_column):
        self.text.tag_add("default", "%s.%s" % (start_line, start_column), "%s.%s" % (end_line, end_column))
        self.text.tag_config("default", background="yellow", foreground="black")

    def process_report(self):
        from pynestml.utils.logger import Logger, LoggingLevel
        for (artifactName, neuron, logLevel, code, errorPosition, message) in Logger.log.values():
            if logLevel == LoggingLevel.WARNING:
                print('warning: '+ str(errorPosition))
                self.color_text_warning(errorPosition.start_line, 0,errorPosition.start_line,20)
            elif logLevel == LoggingLevel.ERROR:
                print('error')
                self.color_text_error(errorPosition.start_line, errorPosition.start_column,
                                      errorPosition.end_line, errorPosition.end_column)
