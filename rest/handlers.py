import tornado.web
import os
import utilities
import socket
import logging
import tornado.auth
import shutil

from tornado.log import enable_pretty_logging
enable_pretty_logging()

#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

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

class JupyterHandler(RequestHandler, tornado.auth.OAuth2Mixin):
    #@tornado.web.authenticated
    #@tornado.gen.coroutine
    def get(self):
#        username = self.get_or_error('jusername')
        resourcetype = self.get_or_error('resourcetype')
        resourceid = self.get_or_error('resourceid')
        husername = self.get_or_error('husername')

        print('Jupyter Handler RECEIVED: %s, %s, %s' % (husername, resourcetype, resourceid))
        
        if not (resourcetype and resourceid and husername): return

        # make all usernames lowercase
        username = husername.lower()
        resourcetype = resourcetype.lower()
	
        # build userspace
        utilities.build_userspace(username)
        utilities.set_hydroshare_args(husername, resourceid, resourcetype)
 
        # generate the redirect url
        baseurl = socket.gethostbyname(socket.gethostname())
        url = "http://%s/user/%s/tree/notebooks/examples/%s.ipynb" % (baseurl,username, resourcetype)
        print('Redirecting to url: %s' % url)

        self.redirect(url, status=303)

