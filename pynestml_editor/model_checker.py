try:
    from pynestml.utils.model_parser import ModelParser
    from pynestml.utils.logger import Logger, LoggingLevel
    from pynestml.meta_model.ast_source_location import ASTSourceLocation
    from pynestml.symbol_table.symbol_table import SymbolTable
    from pynestml.symbols.predefined_functions import PredefinedFunctions
    from pynestml.symbols.predefined_types import PredefinedTypes
    from pynestml.symbols.predefined_units import PredefinedUnits
    from pynestml.symbols.predefined_variables import PredefinedVariables
    from pynestml.utils.logger import Logger, LoggingLevel
    from pynestml.utils.model_parser import ModelParser, set_up_parser_error_reporting, set_up_lexer_error_reporting
    from pynestml.generated.PyNestMLLexer import PyNestMLLexer
    from pynestml.generated.PyNestMLParser import PyNestMLParser
    from antlr4 import *

    # minor setup steps required
    Logger.init_logger(LoggingLevel.INFO)
    SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
    PredefinedUnits.register_units()
    PredefinedTypes.register_types()
    PredefinedVariables.register_variables()
    PredefinedFunctions.register_functions()

    pynestml_available = True
except ImportError:
    pynestml_available = False


class ModelChecker(object):

    @classmethod
    def check_model_syntax(cls, model_as_string):
        if pynestml_available:
            Logger.init_logger(LoggingLevel.NO)
            input_file = InputStream(model_as_string)
            lexer = PyNestMLLexer(input_file)
            set_up_lexer_error_reporting(lexer)
            # create a token stream
            stream = CommonTokenStream(lexer)
            stream.fill()
            # parse the file
            parser = PyNestMLParser(stream)
            set_up_parser_error_reporting(parser)
            parser.nestMLCompilationUnit()

            return str(Logger.get_json_format())
        else:
            print('PyNestML not available, no checks performed!')
            return str({})

    @classmethod
    def check_model_with_cocos(cls, model_as_string):
        if pynestml_available:
            Logger.init_logger(LoggingLevel.INFO)

            model = ModelParser.parse_model(model=model_as_string, from_string=True)
            return str(Logger.get_json_format())
        else:
            print('PyNestML not available, no checks performed!')
            return str({})

# ModelChecker().check_model('/home/kperun/Dropbox/PyNestMlAtGithub/models/aeif_cond_alpha.nestml')
