# this file contains utility functions used by the RequestHandlers

import os
import pwd
import json
import shutil
from hs_restclient import HydroShare
import logging

log = logging.getLogger()

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
    files = collect_files('./ipynbs')
    log.info('Collect files operation found %d files to be copied' % len(files))
    relpaths = [os.path.relpath(p, '.') for p in files]
    
    newfiles = []
    # copy files into user space and change ownership
    for i in range(0, len(files)):
        src = files[i]
        dst = os.path.join(user_dir, relpaths[i])
        newfiles.append(dst)

        log.info('Copying file %s --> %s' % (src,dst))

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

    # return the file paths that were moved
    return newfiles


def collect_files(dir):
    files_paths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            files_paths.append(os.path.join(os.path.abspath(root), file))
    return files_paths

def insert_user_info_into_ipynb(ipynb_file, username, resource_id):

    log.info('Inserting the following params into %s: %s, %s' % (ipynb_file, username, resource_id))

    # load the ipynb as json
    with open(ipynb_file) as f:
        data = json.load(f)

    # replace keywords
    for i in range(len(data['cells'])):
        cell = data['cells'][i]
        for j in range(len(cell['source'])):
            data['cells'][i]['source'][j] = data['cells'][i]['source'][j].replace('INSERT_USERNAME', username)
            data['cells'][i]['source'][j] = data['cells'][i]['source'][j].replace('INSERT_RESID', resource_id)

    # rewrite the file
    with open(ipynb_file, 'w') as f:
        json.dump(data, f)


                
                

