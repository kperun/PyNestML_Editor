try:
    from pynestml.frontend.pynestml_frontend import to_nest, install_nest

    pynestml_available = True
except ImportError:
    pynestml_available = False


class ModelChecker(object):

    @classmethod
    def check_model(cls, path):
        if pynestml_available:
            pass
        else:
            print('PyNestML not available, no checks performed!')
