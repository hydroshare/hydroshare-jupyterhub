from __future__ import print_function
import os, sys
import getpass
import socket
import glob
import requests
import threading
import time
from . import utils
import yaml
from IPython.core.display import display, HTML
from hs_restclient import HydroShare, HydroShareAuthBasic, HydroShareHTTPException
import xml.etree.ElementTree as et
from datetime import datetime as dt
import pickle
import shutil
import urllib

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
    input = raw_input
    urlencode = urllib.pathname2url
else:
    import queue as queue
    urlencode = urllib.parse.quote

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
    for f, p in content_files.items():
        if f[-5:] == 'ipynb':
            fname = os.path.basename(p)
            rel_path = os.path.relpath(p, os.environ['HOME'])
            url = '%s%s/notebooks/notebooks/%s' % (':'.join(os.environ['JUPYTER_HUB_IP'].split(':')[:-1]),os.environ['JPY_BASE_URL'], rel_path)
            encoded_url = urlencode(url)
            links[fname] = encoded_url
    return links
            
def display_resource_content_files(content_file_dictionary, text='Found the following content when parsing the HydroShare resource:'):
    
    # get ipynb files
    nbs = check_for_ipynb(content_file_dictionary)
    if len(nbs.keys()) > 0:
        display(HTML('<b>Found the following notebook(s) associated with this HydroShare resource.</b><br>Click the link(s) below to launch the notebook.'))
        
        for name, url in nbs.items():

            # remove notebook from content_file_dictionary
            content_file_dictionary.pop(name)

            display(HTML('<a href=%s target="_blank">%s<a>' % (url, name)))

    # print the remaining files    
    if len(content_file_dictionary.keys()) > 0:
        display(HTML('<b>Found the following file(s) associated with this HydroShare resource.</b>'))
        
        text = '<br>'.join(content_file_dictionary.keys())
        display(HTML(text))
    
    if (len(content_file_dictionary.keys()) + len(nbs.keys())) > 0:
        display(HTML('These files are stored in a dictionary called <b>hs.content</b> for your convenience.  To access a file, simply issue the following command where MY_FILE is one of the files listed above: <pre>hs.content["MY_FILE"] </pre> '))
    
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
            
    
class ResourceMetadata (object):
    def __init__(self, system_meta, science_meta):
        
        self.root = et.fromstring(science_meta)
        self.ns = {'dc': 'http://purl.org/dc/elements/1.1/', 
                      'ns2': "http://purl.org/dc/terms/",
                      'ns3':"http://hydroshare.org/terms/",
                      'ns4': 'http://www.w3.org/2001/01/rdf-schema#',
                      'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                     }
        self.parse_science_metadata()
        
        self.__dict__.update(system_meta)
        
    @property
    def url(self): return self._url
    @property
    def abstract(self): return self._abstract
    @property
    def keywords(self): return self._keywords
    
    @url.setter
    def url(self, value): self._url = value
    @abstract.setter
    def abstract(self, value): self._abstract = value
    @keywords.setter
    def keywords(self, value): self._keywords = value
        
    
    def parse_science_metadata(self):
        
        # get the resource url
        search = '{{{0}}}Description'.format(self.ns['rdf'])
        self.url = self.root.find(search).get('{{{0}}}about'.format(self.ns['rdf']))

        search = '{{{0}}}Description/{{{1}}}description/{{{0}}}Description/{{{2}}}abstract'.format(self.ns['rdf'], self.ns['dc'], self.ns['ns2'])
        self.abstract = self.root.find(search).text

        search = '{{{0}}}Description/{{{1}}}subject'.format(self.ns['rdf'], self.ns['dc'])
        kw_elems = self.root.findall(search)
        self.keywords = [kw.text for kw in kw_elems]
        
        
class hydroshare():
    def __init__(self, username=None, password=None, cache=True):
        self.hs = None
        self.content = {}
        
        # load the HS environment variables
        self.load_environment()
        
        uname = username
        if uname is None:
            uname = os.environ['HS_USR_NAME']

        if password is None:
            # get a secure connection to hydroshare
           auth = self.getSecureConnection(uname)
        else:
            print('WARNING:  THIS IS NOT A SECURE METHOD OF CONNECTING TO HYDROSHARE...AVOID TYPING CREDENTIALS AS PLAIN TEXT')
            auth = HydroShareAuthBasic(username=uname, password=password)

        try:
            self.hs = HydroShare(auth=auth)
            self.hs.getUserInfo()
            display(HTML('<b style="color:green;">Successfully established a connection with HydroShare</b>'))
     
        except HydroShareHTTPException as e:
            display(HTML('<p style="color:red;"><b>Failed to establish a connection with HydroShare.  Please check that you provided the correct credentials</b><br>%s </p>' % e))

            # remove the cached authentication
            auth_path = os.path.join(os.path.dirname(__file__), '../../../.auth')
            if os.path.exists(auth_path):
                os.remove(auth_path)

            return None
        
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
        
        auth_path = os.path.join(os.path.dirname(__file__), '../../../.auth')
        if not os.path.exists(auth_path):
            print('\nThe hs_utils library requires a secure connection to your HydroShare account.')
            p = getpass.getpass('Enter the HydroShare password for user \'%s\': ' % username)
            auth = HydroShareAuthBasic(username=username, password=p)
            
            with open(auth_path, 'wb') as f:
                pickle.dump(auth, f, protocol=2)
                
        else:
            
            with open(auth_path, 'rb') as f:
                auth = pickle.load(f)
            
        return auth
        

    def getResourceMetadata(self, resid):
        science_meta = self.hs.getScienceMetadata(resid)
        system_meta = self.hs.getSystemMetadata(resid)
        return ResourceMetadata(system_meta, science_meta)
        
    def createHydroShareResource(self, abstract, title, derivedFromId, keywords=[], resource_type='GenericResource', content_files=[], public=False):
        
        # query the hydroshare resource types and make sure that resource_type is valid
        restypes = {r.lower():r for r in self.hs.getResourceTypes()}
        try:
            res_type = restypes[resource_type]
        except KeyError:
            display(HTML('<b style="color:red;">[%s] is not a valid HydroShare resource type.</p>' % resource_type))
            return None
        
        # get the 'derived resource' metadata
        if derivedFromId is not None:
            try:
                # update the abstract and keyword metadata
                meta = self.getResourceMetadata(derivedFromId)
                abstract = meta.abstract + '\n\n[Modified in JupyterHub on %s]\n%s' % (dt.now(), abstract)
                keywords = set(keywords + meta.keywords)
                
            except:
                display(HTML('<b style="color:red;">[%s] is not a valid HydroShare resource id for setting the "derivedFrom" attribute.</p>' % derivedFromId))
                return None
        
        else:
            response = input('You have indicated that this resource is NOT derived from any existing HydroShare resource.  Are you sure that this is what you intended? [Y/n]')
            if response == 'n':
                display(HTML('<b style="color:red;">Resource creation aborted.</p>'))
                return  
        
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
        
        default_dl_path = os.environ['DATA']
        dst = os.path.abspath(os.path.join(default_dl_path, destination))
        download = True
        
        # check if the data should be overwritten
        dst_res_folder = os.path.join(dst, resourceid)
        if os.path.exists(dst_res_folder):    
            res = input('This resource already exists in your userspace.\nWould you like to overwrite this data [Y/n]? ')
            if res != 'n':
                shutil.rmtree(dst_res_folder)
            else:
                download = False
         
        # re-download the content if desired
        if download:
            try:

                # get some metadata about the resource that will be downloaded
                res_meta = self.hs.getSystemMetadata(resourceid)
                header = requests.head(res_meta['bag_url'])

                # download the resource (threaded)
                t = threading.Thread(target=self._getResourceFromHydroShare, 
                                     args=(resourceid,), kwargs={'destination':dst, 'unzip':True})
                runThreadedFunction(t, msg='Downloading', success='Download Completed Successfully')


            except Exception as e:
                display(HTML('<b style="color:red">Failed to retrieve resource content from HydroShare: %s</b>' % e))
                return None

        # load the resource content
        outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
        content_files = glob.glob(os.path.join(outdir,'data/contents/*'))
            #display(HTML('Your Content is located at: %s' % outdir))
        
        content = {}
        for f in content_files:
            fname = os.path.basename(f)
            content[fname] = f

        display_resource_content_files(content)
        #check_for_ipynb(content_files)
        
        # update the content dictionary
        self.content.update(content)
        
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
        
        self.content = content
