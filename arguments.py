
from tornado.web import RequestHandler


def get_or_error(argname, strip=True):
    """
    This function gets a REST input argument or returns an error message if the argument is not found
    Arguments:
    argname -- the name of the argument to get
    strip -- indicates if the whitespace will be stripped from the argument
    """
    
    arg = RequestHandler.get_argument(argname, default=None, strip=strip)
    return arg

    if arg is None:
        raise Exception('Could not find parameter "%s".  Please make sure that all required parameters have been provided' % argname)
    
    return arg
    

