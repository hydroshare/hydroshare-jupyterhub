# this file contains utility functions used by the RequestHandlers

import os
import pwd
import shutil
from hs_restclient import HydroShare


def get_user_info(username):
    try:
        userinfo = pwd.getpwnam(username)
    except Exception:
        return 0
    return userinfo

# this is insecure for user execution b/c they could input any username.
def make_content_dir(username):
    contentdir = '/home/%s/ipynbs/content' % username
     
    if not os.path.exists(contentdir):
        userinfo = get_user_info(username)
        if not userinfo:
            print('Failed to create user content directory')
        os.makedirs(contentdir)
        os.chown(contentdir, userinfo.pw_uid, userinfo.pw_gid)
    return contentdir


# this is insecure for user execution b/c they could input any username.
def get_content_for_resource(username, resource_id):

    # todo: this is missing authentication
    hs = HydroShare()
    dst = make_content_dir(username)
    hs.getResource(resource_id, destination=dst, unzip=True)
    return os.path.join(dst, resource_id)

def build_userspace(username):

    userinfo = get_user_info(username)
    if not username:
        raise Exception("<b>Encountered Error: </b> User '%s' does not exist on system" % username)

    user_dir = userinfo.pw_dir

    # get the default files 
    files = collect_ipynb_files('./ipynbs')
    relpaths = [os.path.relpath(p, '.') for p in files]

    # copy files into user space and change ownership
    for i in range(0, len(files)):
        src = files[i]
        dst = os.path.join(user_dir, relpaths[i])

        # make the destination directory if it doesn't already exist
        dirpath = os.path.dirname(dst)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            os.chown(dirpath, userinfo.pw_uid, userinfo.pw_gid)

        # todo: check if file exists, so that it is not overwritten
        shutil.copyfile(src, dst)

        # modify user permissions
        os.chown(dst, userinfo.pw_uid, userinfo.pw_gid)

        # make content directory
        make_content_dir(username)

def collect_ipynb_files(dir):
    files_paths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            #if file[-5:] == 'ipynb':
            files_paths.append(os.path.join(os.path.abspath(root), file))
    return files_paths



