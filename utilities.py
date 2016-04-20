# this file contains utility functions used by the RequestHandlers

import os
import pwd
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




