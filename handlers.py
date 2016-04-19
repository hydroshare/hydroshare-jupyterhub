import tornado.web

class RequestHandler(tornado.web.RequestHandler):
    def __init_(self):
        super(RequestHandler, self)

    def get_or_error(self, argname, strip=True):
        """
        This function gets a REST input argument or returns an error message if the argument is not found
        Arguments:
        argname -- the name of the argument to get
        strip -- indicates if the whitespace will be stripped from the argument
        """
        arg = self.get_argument(argname, default=None, strip=strip)
        if arg is None:
            self.write('<b>Encountered Error: </b> Could not find parameter "%s". <br> ' % argname)
            return 0
        return arg

class MainHandler(RequestHandler):
    def get(self):

        name = self.get_or_error('name')
        if not name: return 

        self.write('Hello %s'%name)


class JupyterHandler(RequestHandler):
    def get(self):
        username = self.get_or_error('username')
        resourcetype = self.get_or_error('resourcetype')
        resourceid = self.get_or_error('resourceid')
        if not (username and resourcetype and resourceid): return
        
        self.redirect("http://129.123.51.34/user/tony/notebooks/demos.ipynb")



