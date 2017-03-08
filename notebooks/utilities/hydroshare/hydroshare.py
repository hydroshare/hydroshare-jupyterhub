from __future__ import print_function
import os, sys
import getpass
import glob
import requests
from IPython.core.display import display, HTML
from hs_restclient import HydroShare, HydroShareAuthBasic, HydroShareHTTPException
from datetime import datetime as dt
import pickle
import shutil

from . import threads
from . import resource
from . import utilities
from .compat import *


class hydroshare():
    def __init__(self, username=None, password=None, cache=True):
        self.hs = None
        self.content = {}
        
        # load the HS environment variables
        # todo: this should be set as a path variable somehow.  Possibly add JPY_TMP to Dockerfile
        self.cache = cache
        if cache:
            utilities.load_environment(os.path.join(os.environ['HOME'], '.env'))
        self.auth_path = '/home/jovyan/.auth'

        # todo: either use JPY_USR or ask them to enter their hydroshare username
        uname = username
        if uname is None:
            if 'HS_USR_NAME' in os.environ.keys():
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
            # display(HTML('<b style="color:green;">Successfully established a connection with HydroShare</b>'))
            print('Successfully established a connection with HydroShare')

        except HydroShareHTTPException as e:
            # display(HTML('<p style="color:red;"><b>Failed to establish a connection with HydroShare.  Please check that you provided the correct credentials</b><br>%s </p>' % e))
            print('Failed to establish a connection with HydroShare.\n  '
                  'Please check that you provided the correct credentials.\n  '
                  '%s' % e)

            # remove the cached authentication
            if os.path.exists(self.auth_path):
                os.remove(self.auth_path)

            return None
       
    # def _getResourceFromHydroShare(self, resourceid, destination='.', unzip=True):
    #     # download the resource
    #     pid = self.hs.getResource(resourceid, destination=destination, unzip=unzip)
    #     utilities.threadResults.put(pid)
    
    # def _createHydroShareResource(self, res_type, title, abstract, content_file,
    #                               keywords=[]):
    #
    #     resid = self.hs.createResource(res_type, title, resource_file=content_file,
    #                                    keywords=keywords, abstract=abstract)
    #     threadResults.put(resid)
    
    def _addContentToExistingResource(self, resid, content_files):

        for f in content_files:
            self.hs.addResourceFile(resid, f)
        
    def getSecureConnection(self, username=None):
        """
        Establishes a secure connection with HydroShare.

        Args:
            email: email address associated with HydroShare
        Returns:
            HydroShare connection 
        """
        if not os.path.exists(self.auth_path):
            print('\nThe hs_utils library requires a secure connection to your HydroShare account.')
            if username is None:
                username = input('Please enter your HydroShare username: ').strip()
            p = getpass.getpass('Enter the HydroShare password for user \'%s\': ' % username)
            auth = HydroShareAuthBasic(username=username, password=p)

            if self.cache:
                with open(self.auth_path, 'wb') as f:
                    pickle.dump(auth, f, protocol=2)
                
        else:
            
            with open(self.auth_path, 'rb') as f:
                auth = pickle.load(f)
            
        return auth
        

    def getResourceMetadata(self, resid):
        science_meta = self.hs.getScienceMetadata(resid)
        system_meta = self.hs.getSystemMetadata(resid)
        return resource.ResourceMetadata(system_meta, science_meta)
        
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
        resid = threads.runThreadedFunction('Creating HydroShare Resource', 'Resource Created Successfully',
                                            self.hs.createResource, res_type, title, abstract, f,
                                            keywords=keywords)
        # resid = utilities.runThreadedFunction(t, msg='Creating HydroShare Resource', success='Resource Creation Successful')

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
        
        default_dl_path = utilities.get_env_var('DATA')
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
                threads.runThreadedFunction('Downloading Resource', 'Download Finished', self.hs.getResource,
                                            resourceid, destination=dst, unzip=True)

                print('Successfully downloaded resource %s' % resourceid)

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

        utilities.display_resource_content_files(content)
        #check_for_ipynb(content_files)
        
        # update the content dictionary
        self.content.update(content)
        
    def addContentToExistingResource(self, resid, content):
        # t = threads.Thread(target=self._addContentToExistingResource, args=(resid, content))
        threads.runThreadedFunction('Adding Content to Resource', 'Successfully Added Content Files',
                                    self._addContentToExistingResource, resid, content)
    
    def loadResource(self, resourceid):
        
        resdir = utilities.find_resource_directory(resourceid)
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
        
        utilities.display_resource_content_files(content)
        
        self.content = content
