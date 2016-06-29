# this file contains utility functions used by the RequestHandlers

import os
from pwd import getpwnam
import grp
import json
import shutil
from hs_restclient import HydroShare
import logging

log = logging.getLogger()



def load_envs():
    with open('../jupyterhub/env','r') as f:
        lines = f.readlines()
        for line in lines:
            vals = line.strip().split(' ')[-1].split('=')
            if len(vals) == 2:
                os.environ[vals[0]] = vals[1]

def set_hydroshare_args(username, resourceid, resourcetype):
    
    userspace_dir = os.environ['JUPYTER_USERSPACE_DIR']
    hs_env = os.path.abspath(os.path.join(userspace_dir, '%s/notebooks/utilities/env' % username.lower()))
    print('ENV_PATH ',hs_env)

    with open(hs_env, 'w') as f:
        f.write('HS_USR_NAME=%s\n' % username)
        f.write('HS_RES_ID=%s\n' % resourceid)
        f.write('HS_RES_TYPE=%s\n' % resourcetype)
    
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
    # check to see if user exists
    basepath = os.path.abspath(os.path.join(userspace_dir, '%s'%husername))
    path = os.path.abspath(os.path.join(basepath, 'notebooks'))
    if not os.path.exists(path):
        os.makedirs(path)

    file_paths = []
    print('IPYNB_DIR: ' + ipynb_dir)
    #ipynb_dir = '../jupyter-rest-endpoint/notebooks'
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

    # change file ownership so that it can be accessed inside docker container
    print('Modifying permissions for %s' % basepath)
    os.chown(basepath, uid, gid)
    for root, dirs, files in os.walk(basepath):
        for d in dirs:
            print('Modifying permissions for %s' % os.path.join(root,d))
            os.chown(os.path.join(root, d), uid, gid)
        for f in files:
            print('Modifying permissions for %s' % os.path.join(root,f))
            os.chown(os.path.join(root, f), uid, gid)


# load environment vars 
load_envs()



                
                

