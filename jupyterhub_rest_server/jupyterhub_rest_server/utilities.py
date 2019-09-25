# this file contains utility functions used by the RequestHandlers

import os, stat
from pwd import getpwnam
import grp
import shutil
import logging

log = logging.getLogger()


def set_hydroshare_args(username, resourceid, resourcetype):

    userspace_dir = os.environ['JUPYTER_USERSPACE_DIR']
    hs_env = os.path.abspath(os.path.join(userspace_dir, '%s/notebooks/.env' % username.lower()))
    print('ENV_PATH ',hs_env)

    with open(hs_env, 'w') as f:
        f.write('HS_USR_NAME=%s\n' % username)
        f.write('HS_RES_ID=%s\n' % resourceid)
        f.write('HS_RES_TYPE=%s\n' % resourcetype)
        f.write('JUPYTER_HUB_IP=%s\n' % os.environ['JUPYTER_HUB_IP'] )

    # get the jupyter username
    user = getpwnam(os.environ['JUPYTER_USER'])
    group = grp.getgrnam('users')
    uid = user.pw_uid
    gid = group.gr_gid
    os.chown(hs_env, uid, gid)

def build_userspace(username):

    # make all usernames lowercase
    husername = username.lower()

    # get the jupyter username
    user = getpwnam(os.environ['JUPYTER_USER'])
    group = grp.getgrnam('users')
    uid = user.pw_uid
    gid = group.gr_gid

    userspace_dir = os.environ['JUPYTER_USERSPACE_DIR']
    ipynb_dir = os.environ['JUPYTER_NOTEBOOK_DIR']

    # set the path to the user's directory in the 
    # userspace mount
    basepath = os.path.abspath(os.path.join(userspace_dir,
                                            '%s' % husername))
    # define the path to the users notebooks
    path = os.path.abspath(os.path.join(basepath, 'notebooks'))

    # prepare the user's root direcory
    # make the root directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # set permissions for the root path and
    # the users notebooks path regardless of the
    # directories already exist to make sure we don't
    # run into permissions issues
    os.chown(path, uid, gid)
    os.chmod(path, 0o2770)
    os.chown(basepath, uid, gid)
    os.chmod(basepath, 0o2770)

    # collect all the paths for the files that will be
    # copied into the user's notebooks directory
    print('%s -> copying userpace files' % username, flush=True)
    file_paths = []
    for root, dirs, files in os.walk(ipynb_dir):
        for file in files:
            file_paths.append(os.path.join(os.path.abspath(root), file))

    # generate list of relative paths that will be used to copy
    # the default files into the user's notebook directory
    relpaths = [os.path.relpath(p, ipynb_dir) for p in file_paths]

    # loop through each of the file paths and add them to the
    # user's userspace directory. Make sure permissions are set
    # correctly.
    for i in range(0, len(file_paths)):
        src = file_paths[i]
        dst = os.path.join(path, relpaths[i])
        dirpath = os.path.dirname(dst)

        # only create the dir of it doesn't already exist
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        # always set the permission for folders whether or not
        # they already exist to make sure we don't run into
        # permissions issues
        os.chown(dirpath, uid, gid)
        os.chmod(dirpath, 0o2770)

        # copy the file and set permissions
        shutil.copyfile(src, dst)
        os.chown(dst, uid, gid)
        os.chmod(dst, 0o2770)
