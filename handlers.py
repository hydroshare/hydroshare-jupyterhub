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
            self.write('<h1>ERROR</h1>')
            self.write('Could not find parameter "%s".  Please make sure that all required parameters have been provided' % argname)
            raise self.finish()
        return arg

class MainHandler(RequestHandler):
    def get(self):

        name = self.get_or_error('name', strip=True)
        self.write('Hello %s'%name)


class JupyterHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument('notebook', default=None, strip=True)
        resourcetype = self.get_argument('notebook', default=None, strip=True)
        resourceid = self.get_argument('notebook', default=None, strip=True)
        if notebook is None:
            self.write('missing parameter: "notebook"')
            return
        self.redirect("http://129.123.51.34/user/tony/notebooks/demos.ipynb")
        #self.write('Redirect to notebook %s'%notebook)



