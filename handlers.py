import tornado.web
import shutil
import pwd
import os
import grp

ipynb_dir = './ipynbs'

def get_ipynb_files(dir):
    files_paths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            #if file[-5:] == 'ipynb':
            files_paths.append(os.path.join(os.path.abspath(root), file))
    return files_paths

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
        try:
            userinfo = pwd.getpwnam(username)
        except Exception:
            self.write("<b>Encountered Error: </b> User '%s' does not exist on system" % username)
            return

        # save the user's info
        user_dir = userinfo.pw_dir
        uid = userinfo.pw_uid
        gid = userinfo.pw_gid


        # move files into user space
        files = get_ipynb_files(ipynb_dir)
        for file in files:
            self.write('<b>Found file: </b> %s <br>'%file)

        relpaths = [os.path.relpath(p, '.') for p in files]
        
        for i in range(0, len(files)):
            src = files[i]
            dst = os.path.join(user_dir, relpaths[i])
          
            # make the destination directory if it doesn't already exist
            dirpath = os.path.dirname(dst) 
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
                os.chown(dirpath, uid, gid)

            # todo: check if file exists, so that it is not overwritten
            shutil.copyfile(src, dst)

            # modify user permissions
            os.chown(dst, uid, gid)


            self.write('<b>Copied: %s --> %s<br>' % (src, dst))

        url = "http://129.123.51.34/user/%s/notebooks/ipynbs/%s.ipynb" % (username, resourcetype)
        self.redirect(url)



