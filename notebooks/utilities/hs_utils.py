import os, sys
import getpass
import socket
import glob
import requests
import threading
import time
import utils
import yaml
from IPython.core.display import display, HTML
from hs_restclient import HydroShare, HydroShareAuthBasic, HydroShareHTTPException
import queue

threadResults = queue.Queue()

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

def check_for_ipynb(content_files):

    links = {}
    for f in content_files:
        if f[-5:] == 'ipynb':
            fname = os.path.basename(f)
            rel_path = os.path.relpath(f, os.environ['HOME'])
            url = '%s%s/notebooks/notebooks/%s' % (':'.join(os.environ['JPY_HUB_API_URL'].split(':')[:-1]),os.environ['JPY_BASE_URL'], rel_path)
            links[fname] = url

    if len(links) > 0:
        display(HTML('<h3>I found the following notebook(s) associated with this HydroShare resource.</h3>'))
        display(HTML('Click the link(s) below if you wish to load a different Python notebook'))
        for name, url in links.items():
            display(HTML('<a href=%s target="_blank">%s<a>' % (url, name)))

def check_for_ipynbs_by_keyword():    
    pass
            
def display_resource_content_files(content_file_dictionary):
    
    display(HTML('<h3>Found the following content when parsing the HydroShare resource:</h3>'))
    table_str = '<table>'
    table_str += '<th>Key</th><th>Value</th>'
    for k,v in content_file_dictionary.items():
        table_str += '<tr style="word-break: break-word;">'
        table_str += '<td width="20%%">%s</td><td>%s</td>' % (k,v)
        table_str += '</tr>'
    table_str += '</table>'
    display(HTML(table_str))
    display(HTML('<p>To access these variables issue the following command: <br> <code>   my_value = hs.content["key"] </code><p>'))
    
def runThreadedFunction(t, msg, success):

    # start the thread
    t.start()

    # add some padding to the message
    message = msg+' ' if msg[-1] != ' ' else msg
 
    # print message while 
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
    
    # join the thread
    print('\r' + (len(message) + 10)*' ')
    display(HTML('<b style="color:green;">%s</b>' % success))
    
    res = None
    if not threadResults.empty():
        res = threadResults.get()
      
    t.join()
    return res
            
    
class hydroshare():
    def __init__(self):
        self.hs = None
        self.content = {}
        
    def _getResourceFromHydroShare(self, resourceid, destination='.', unzip=True):
        # download the resource
        pid = self.hs.getResource(resourceid, destination=destination, unzip=unzip)
        threadResults.put(pid)
    
    def _createHydroShareResource(self, res_type, title, abstract, content_file,              
                                  keywords=[]):
        
        resid = self.hs.createResource(res_type, title, resource_file=content_file, 
                                       keywords=keywords, abstract=abstract)
        threadResults.put(resid)
    
    def _addContentToExistingResource(self, resid, content_files):
   
        for f in content_files:
            self.hs.addResourceFile(resid, f)
            
        
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
            display(HTML('<b style="color:green;">Successfully established a connection with HydroShare</b>'))
        except HydroShareHTTPException as e:
            display(HTML('<p style="color:red;"><b>Failed to establish a connection with HydroShare.  Please check that you provided the correct credentials</b><br>%s </p>' % e))
            self.hs = None


    def createHydroShareResource(self, abstract, title, keywords=[], resource_type='GenericResource', content_files=[], public=False):
        
        # query the hydroshare resource types and make sure that resource_type is valid
        restypes = {r.lower():r for r in hs.hs.getResourceTypes()}
        try:
            res_type = restypes[resource_type]
        except KeyError:
            display(HTML('<b style="color:red;">[%s] is not a valid HydroShare resource type.</p>' % resource_type))
        
        f = None if len(content_files) == 0 else content_files[0]

        # create the hs resource (1 content file allowed)
        t = threading.Thread(target=self._createHydroShareResource, args=(res_type, title, abstract, f), kwargs={'keywords':keywords})
        resid = runThreadedFunction(t, msg='Creating HydroShare Resource', success='Resource Creation Successful')

        # add the remaining content files to the hs resource
        self.addContentToExistingResource(resid, content_files[1:])
                                                                           
        
        display(HTML('Resource id: %s' % resid))
        display(HTML('<a href=%s target="_blank">%s<a>' % ('https://www.hydroshare.org/resource/%s' % resid, 'Open Resource in HydroShare')))
        
    def getResourceFromHydroShare(self, resourceid, destination='.'):
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
            t = threading.Thread(target=self._getResourceFromHydroShare, 
                                 args=(resourceid,), kwargs={'destination':dst, 'unzip':True})
            runThreadedFunction(t, msg='Downloading', success='Download Completed Successfully')
                        
            #self.hs.getResource(resourceid, destination=dst, unzip=True)
            outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
            content_files = glob.glob(os.path.join(outdir,'data/contents/*'))
        except Exception as e:
            print('<b style="color:red">Failed to retrieve resource content from HydroShare: %s</b>' % e)
            return None

        display(HTML('Downloaded content is located at: %s' % outdir))
        
        content = {}
        for f in content_files:
            fname = os.path.basename(f)
            content[fname] = f

        display_resource_content_files(content)
        check_for_ipynb(content_files)
        
        self.content = content
        
    def addContentToExistingResource(self, resid, content):
        t = threading.Thread(target=self._addContentToExistingResource, args=(resid, content))
        runThreadedFunction(t, msg='Adding Content to Resource', success='Successfully Added Content Files') 
    
    def loadResource(self, resourceid):
        
        resdir = find_resource_directory(resourceid)
        if resdir is None:
            display(HTML('<b style="color:red">Could not find any resource matching the id [%s].</b> <br> It is likely that this resource has not yet been downloaded from HydroShare.org, or it was removed from the JupyterHub server.   Please use the following command to aquire the resource content: <br><br> <code>    hs.getResourceFromHydroShare(%s)</code>.' % (resourceid, resourceid)))
            return
        
        content_files = glob.glob(os.path.join(resdir,'%s/data/contents/*' % resourceid))
        display(HTML('<p>Downloaded content is located at: %s</p>' % resdir))
        display(HTML('<p>Found %d content file(s). \n</p>' % len(content_files)))
        content = {}
        for f in content_files:
            fname = os.path.basename(f)
            content[fname] = f
        
        display_resource_content_files(content)
        check_for_ipynb(content_files)
        
        self.content = content

            
# initialize
hs = hydroshare()

