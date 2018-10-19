import tornado.web
import os
import socket
import logging
import tornado.auth
import shutil
from . import utilities

from tornado.log import enable_pretty_logging
enable_pretty_logging()


args = [
	 ['husername', 
          'HydroShare username.  This is used to build an isolated userspace on the JupyterHub server', 
          'Yes',
	  'Example: TonyCastronova'],
         ['resourcetype', 
          'The type of HydroShare resource being sent to JupyterHub. Typically used when launching JupyterHub instances from HydroShare', 
          'No',
	  'Example: GenericResource'],
         ['resourceid', 
          'The unique id of the a HydroShare resource.  Typically used when launching JupyterHub instances from HydroShare', 
          'No',
	  'Example: 97add6638f7841278c73519e7192b252'],
         ['target', 
          'Target notebook to launch relative to http://[jupyteraddress]/user/[husername]/tree/.  This argument is designed to support applications that wish to provide a more customized user experience.', 
          'No',
	  'Example: notebooks/Welcome.ipynb'],
]
header = ['Function', 'Description', 'Required']


class RequestHandler(tornado.web.RequestHandler):
#    def __init_(self):
    errors = []
#        super(RequestHandler, self)

    def get_or_error(self, argname, strip=True):
        """
        This function gets a REST input argument or returns an error message if the argument is not found
        Arguments:
        argname -- the name of the argument to get
        strip -- indicates if the whitespace will be stripped from the argument
        """
        arg = self.get_argument(argname, default=None, strip=strip)
        if arg is None:
            error = 'Could not find required parameter "%s"' % argname
            self.render("index.html", header=header, args=args, error=error)
        return arg

    def get_arg_value(self, argname, isrequired, strip=True):
        arg = self.get_argument(argname, default=None, strip=strip)
        if arg is None and isrequired:
            error = 'Could not find required parameter "%s"' % argname
            self.errors.append(error)
        return arg
   
    def check_for_errors(self):
        if len(self.errors) > 0:
            self.render("index.html", header=header, args=args, error=self.errors)
            return 1
        else:
            return 0


class IndexHandler(RequestHandler, tornado.auth.OAuth2Mixin):
    def get(self):
        self.render("index.html", header=header, args=args)

class JupyterHandler(RequestHandler, tornado.auth.OAuth2Mixin):
    def get(self):

        # get arguments from the query string.
        # display an error if req args are missing.
        self.errors = []
        husername = self.get_arg_value('husername', 1)
        resourcetype = self.get_arg_value('resourcetype', 0) or ""
        resourceid = self.get_arg_value('resourceid', 0) or ""
        target = self.get_arg_value('target', 0)
        if self.check_for_errors():
            return

        # make all usernames lowercase
        username = husername.lower()
        if resourcetype != "":
            resourcetype = resourcetype.lower()

        # build userspace
        try:
            msg = '%s -> building userspace' % husername
            print(msg)
            utilities.build_userspace(username)
        except Exception as e:
            print('ERROR %s: %s' % (msg, e))

        try:
            msg = '%s -> writing .env' % husername
            print(msg)
            utilities.set_hydroshare_args(husername, resourceid, resourcetype)
        except Exception as e:
            print('ERROR %s: %s' % (msg, e), flush=True)

        # generate the redirect url
        baseurl = os.environ['JUPYTER_HUB_IP']
        port = os.environ['JUPYTER_PORT']
        
        # build the redirect url 
        if port == '443':
            proto = 'https'
            port = ''
        else:
            proto = 'http'
            port = ':'+port
        
        if target is not None:
            url = "%s://%s%s/user/%s/tree/%s" % (proto, baseurl, port, username, target)
        else:
            url = "%s://%s%s/user/%s/tree/notebooks/Welcome.ipynb" % (proto, baseurl, port, username)

        print("URL:" + url)

        # save the next url to ensure that the redirect will work
        p = os.path.join(os.environ['HYDROSHARE_REDIRECT_COOKIE_PATH'], '.redirect_%s' % username)        
        with open(p, 'w') as f:
            f.write(url)

        # redirect to the desired page
        self.redirect(url, status=303)

