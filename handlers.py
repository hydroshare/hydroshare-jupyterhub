import tornado.web
import os
import utilities
import socket
import logging

log = logging.getLogger()

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

class JupyterHandler(RequestHandler):
    def get(self):
        username = self.get_or_error('username')
        resourcetype = self.get_or_error('resourcetype')
        resourceid = self.get_or_error('resourceid')
        
        log.info('Jupyter Handler RECEIVED: %s, %s, %s ' % (username, resourcetype, resourceid))
        
        if not (username and resourcetype and resourceid): return

        # check to see if user exists
        userinfo = utilities.get_user_info(username)
        if not userinfo:
            self.write("<b>Encountered Error: </b> User '%s' does not exist on system" % username)
            return
        print('User exists: %s'%username)

        # build userspace
        try:
            # construct the userspace 
            fpaths = utilities.build_userspace(username)
            log.info('Userspace created')

            # loop through resourcetype notebooks and insert customization
            resource_specific_files = [f for f in fpaths if (resourcetype in f and f[-5:] == 'ipynb')]
            for r in resource_specific_files:
                utilities.insert_user_info_into_ipynb(r, username, resourceid)
                log.info('Finished customizing ipynb %s using the following params: %s, %s' % (r, username, resourceid))
        except Exception as e:
            self.write(e)
            return

        # generate the redirect url
        baseurl = socket.gethostbyname(socket.gethostname())
        url = "http://%s/user/%s/notebooks/ipynbs/%s.ipynb" % (baseurl, username, resourcetype)
        print(url)

        # redirect to ipynb
        # Need to use OAuth, see http://www.tornadoweb.org/en/branch2.3/auth.html
        self.redirect(url, status=303)



