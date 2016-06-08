import os, sys
import getpass
import socket
import glob
import requests
import threading
import time
import utils
import yaml
from hs_restclient import HydroShare, HydroShareAuthBasic, HydroShareHTTPException

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total

def find_resource_directory(resid):
   
    basedir = os.environ['HOME']
   
    # loop over all the files in userspace
    for dirpath, dirnames, filenames in os.walk(basedir):
        for dirname in [d for d in dirnames]:
            if dirname == resid:
                return os.path.join(dirpath, dirname)
    return None

class hydroshare():
    def __init__(self):
        self.hs = None
        
    def load_environment(self):
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'env')
        with open(env_path, 'r') as f:
            lines = f.readlines()
            print('Adding the following system variables:')
            for line in lines:
                k,v = line.strip().split('=')
                os.environ[k] = v
                print('   %s = %s' % (k, v))
            print('\nThese can be accessed using the following command: ')
            print('   os.environ[key]')
            print('\n   (e.g.)\n   os.environ["HS_USR_NAME"]  => %s' % os.environ['HS_USR_NAME'])

    def getSecureConnection(self, username):
        """
        Establishes a secure connection with HydroShare.

        Args:
            email: email address associated with HydroShare
        Returns:
            HydroShare connection 
        """

        p = getpass.getpass('Enter you HydroShare Password: ')
        auth = HydroShareAuthBasic(username=username, password=p)
        self.hs = HydroShare(auth=auth)
        
        try:
            self.hs.getUserInfo()
            print('Successfully established a connection with HydroShare')
        except HydroShareHTTPException as e:
            print(e)
            self.hs = None

   
    def getResourceContent(self,resourceid, destination='.'):
        """
        Downloads the content of HydroShare resource to the JupyterHub userspace

        Args:
            resourceid: id of the HydroShare resource to query
            destination: path relative to /user/[username]/notebooks/data

        """

        try:
            default_dl_path = os.environ['DATA']
            dst = os.path.abspath(os.path.join(default_dl_path, destination))
            
            # get some metadata about the resource that will be downloaded
            res_meta = self.hs.getSystemMetadata(resourceid)
            header = requests.head(res_meta['bag_url'])

            # download the resource (threaded)
            t = threading.Thread(target=self.hs.getResource, args=(resourceid,), kwargs={'destination':dst, 'unzip':True})
            t.start()
            
            message = 'Downloading '
            dl_file_path = os.path.join(dst, os.path.basename(header.headers['Location']))
            max_msg_len = 25
            msg_len = max_msg_len
            while(t.isAlive()):
                time.sleep(.25)    
                if msg_len == max_msg_len:
                    msg_len = 0
                    sys.stdout.write('\r' + ' '*(len(message) + 11))
                    sys.stdout.write('\r')
                    print(message, end='') 
                print('.',end='')
                msg_len += 1
            print('\rDownload Completed Successfully                         ')
            t.join()
            
            #self.hs.getResource(resourceid, destination=dst, unzip=True)
            outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
            content_files = glob.glob(os.path.join(outdir,'data/contents/*'))
        except Exception as e:
            print('Encountered an error when retrieving resource content from HydroShare: %s' % e)
            return None
        
        print(20*'-')
        print('Downloaded content is located at: %s' % outdir)
        print('\nFound the following content files: ')
        content = {}
        for f in content_files:
            fname = os.path.basename(f)
            content[fname] = f
            print('\n[%s]: %s' % (fname,f))
        return content

    def getDownloadedResource(self, resourceid):
        
        resdir = find_resource_directory(resourceid)
        if resdir is None:
            print('Could not find any resource matching the id: %s. If this HydroShare resource has not been downloaded yet, use the getResourceContent function')
            return
        
        content_files = glob.glob(os.path.join(resdir,'%s/data/contents/*' % resourceid))
        print('\nDownloaded content is located at: %s' % resdir)
        print('These data are placed in a dictionary for easy access.')
        print('Found %d content file(s). \n' % len(content_files))
        content = {}
        for f in content_files:
            fname = os.path.basename(f)
            content[fname] = f
        # use yaml for pretty printing
        print(yaml.dump(content, default_flow_style=False))
        return content

            
# initialize
hs = hydroshare()

