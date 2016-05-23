import os
import getpass
import socket
import glob
from hs_restclient import HydroShare, HydroShareAuthBasic, HydroShareHTTPException

class hydroshare():
    def __init__(self):
        self.hs = None

    def getSecureConnection(self, email):
        """
        Establishes a secure connection with HydroShare.

        Args:
            email: email address associated with HydroShare
        Returns:
            HydroShare connection 
        """

        p = getpass.getpass('Enter you HydroShare Password: ')
        auth = HydroShareAuthBasic(username=email, password=p)
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
            self.hs.getResource(resourceid, destination=dst, unzip=True)
            outdir = os.path.join(dst, '%s/%s' % (resourceid, resourceid))
            content_files = glob.glob(os.path.join(outdir,'data/contents/*'))
        except Exception as e:
            print('Encountered an error when retrieving resource content from HydroShare: %s' % e)
            return None
        
        print('Download successful.\nContent is located at: %s' % outdir)
        print('\nFound the following content files: ')
        content = {}
        for f in content_files:
            fname = os.path.basename(f)
            content[fname] = f
            print('\n[%s]: %s' % (fname,f))
            
        return content




