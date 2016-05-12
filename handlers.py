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
        husername = husername.lower()
 
        # check to see if user exists
        path = os.path.abspath(os.path.join('/home/castro/userspace', '%s/notebooks'%husername))
        if not os.path.exists(path):
            os.makedirs(path)
            #os.chown
            #os.chmod(path, 777)
        file_paths = []
        ipynb_dir = './notebooks'
        for root, dirs, files in os.walk(ipynb_dir):
            for file in files:
                file_paths.append(os.path.join(os.path.abspath(root), file))
        relpaths = [os.path.relpath(p, ipynb_dir) for p in file_paths]
        for i in range(0, len(file_paths)):
            src = file_paths[i]
            dst = os.path.join(path, relpaths[i])
            dirpath = os.path.dirname(dst)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            print('copying: %s -> %s' %(src,dst))
            shutil.copyfile(src, dst)
            #    os.chmod(dst, 0o777)

#        # build userspace
#        try:
#            # construct the userspace 
#            fpaths = utilities.build_userspace(username)
#            log.info('Userspace created')
#
#            # loop through resourcetype notebooks and insert customization
#            resource_specific_files = [f for f in fpaths if (resourcetype in f and f[-5:] == 'ipynb')]
#            for r in resource_specific_files:
#                utilities.insert_user_info_into_ipynb(r, husername, resourceid)
#        except Exception as e:
#            self.write(e)
#            return

        # generate the redirect url
        baseurl = socket.gethostbyname(socket.gethostname())
        url = "http://%s/user/%s/tree/notebooks/examples/%s.ipynb" % (baseurl,husername, resourcetype)
        print('Redirecting to url: %s' % url)

        # redirect to ipynb
        # Need to use OAuth, see http://www.tornadoweb.org/en/branch2.3/auth.html
        #self.log.info('oauth2_request url')
        #res = yield self.oauth2_request(
        #    url,
        #)

        self.redirect(url, status=303)

