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
    with open('env','r') as f:
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
    user = getpwnam('castro')  # todo: change to jupyter user
    group = grp.getgrnam('users')
    uid = user.pw_uid
    gid = group.gr_gid
    os.chown(hs_env, uid, gid)

def build_userspace(username):
    

    # make all usernames lowercase
    husername = username.lower()

    # get the jupyter username
    user = getpwnam('castro')  # todo: change to jupyter user
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



#def build_user_space(username):
#    """
#    Builds the userspace on the Jupyterhub server.  This userspace is volume mounted into the Docker JupyterHub container.
#    """
#    pass
#
#def get_user_info(username):
#    try:
#        userinfo = pwd.getpwnam(username)
#    except Exception:
#        return 0
#    return userinfo
#
## this is insecure for user execution b/c they could input any username.
#def make_content_dir(username):
#    contentdir = '/home/%s/ipynbs/content' % username
#     
#    if not os.path.exists(contentdir):
#        userinfo = get_user_info(username)
#        if not userinfo:
#            print('Failed to create user content directory')
#        os.makedirs(contentdir)
#        os.chown(contentdir, userinfo.pw_uid, userinfo.pw_gid)
#    return contentdir
#
#
# this is insecure for user execution b/c they could input any username.
#def get_content_for_resource(username, resource_id):
#
#    # todo: this is missing authentication
#    hs = HydroShare()
#    dst = make_content_dir(username)
#    hs.getResource(resource_id, destination=dst, unzip=True)
#    return os.path.join(dst, resource_id)
#
#def build_userspace(username):
#
#    userinfo = get_user_info(username)
#    if not username:
#        raise Exception("<b>Encountered Error: </b> User '%s' does not exist on system" % username)
#
#    user_dir = userinfo.pw_dir
#
#    # get the default files 
#    files = collect_files('./ipynbs')
#    log.info('Collect files operation found %d files to be copied' % len(files))
#    relpaths = [os.path.relpath(p, '.') for p in files]
#    
#    newfiles = []
#    # copy files into user space and change ownership
#    for i in range(0, len(files)):
#        src = files[i]
#        dst = os.path.join(user_dir, relpaths[i])
#        newfiles.append(dst)
#
#        log.info('Copying file %s --> %s' % (src,dst))
#
#        # make the destination directory if it doesn't already exist
#        dirpath = os.path.dirname(dst)
#        if not os.path.exists(dirpath):
#            os.makedirs(dirpath)
#            os.chown(dirpath, userinfo.pw_uid, userinfo.pw_gid)
#
#        # todo: check if file exists, so that it is not overwritten
#        shutil.copyfile(src, dst)
#
#        # modify user permissions
#        os.chown(dst, userinfo.pw_uid, userinfo.pw_gid)
#
#        # make content directory
#        make_content_dir(username)
#
#    # return the file paths that were moved
#    return newfiles
#
#
#def collect_files(dir):
#    files_paths = []
#    for root, dirs, files in os.walk(dir):
#        for file in files:
#            files_paths.append(os.path.join(os.path.abspath(root), file))
#    return files_paths
#
#def insert_user_info_into_ipynb(ipynb_file, username, resource_id):
#
#    log.info('Inserting the following params into %s: %s, %s' % (ipynb_file, username, resource_id))
#
#    # load the ipynb as json
#    with open(ipynb_file) as f:
#        data = json.load(f)
#
#    # replace keywords
#    for i in range(len(data['cells'])):
#        cell = data['cells'][i]
#        for j in range(len(cell['source'])):
#            data['cells'][i]['source'][j] = data['cells'][i]['source'][j].replace('INSERT_USERNAME', "'%s'"%username)
#            data['cells'][i]['source'][j] = data['cells'][i]['source'][j].replace('INSERT_RESID', "'%s'"%resource_id)
#
#    # rewrite the file
#    with open(ipynb_file, 'w') as f:
#        json.dump(data, f)


                
                

