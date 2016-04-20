import tornado.web
import os
import utilities
import socket

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

        # check to see if user exists
        userinfo = utilities.get_user_info(username)
        if not userinfo:
            self.write("<b>Encountered Error: </b> User '%s' does not exist on system" % username)
            return

        # build userspace
        try:
            utilities.build_userspace(username)
        except Exception as e:
            self.write(e)
            return
       
        # generate the redirect url
        #baseurl = socket.gethostbyname(socket.gethostname())
        url = "/user/%s/notebooks/ipynbs/%s.ipynb" % (username, resourcetype)
        print(url)

        # redirect to ipynb
        self.redirect(url)



