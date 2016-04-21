import os
import getpass
import socket
from hs_restclient import HydroShare, HydroShareAuthBasic


def getSecureConnection(username):
    """
    Establishes a secure connection with HydroShare.

    Args:
        username: HydroShare username
    Returns:
        HydroShare connection 
    """
    
    p = getpass.getpass('Enter you HydroShare Password: ')
    auth = HydroShareAuthBasic(username=username, password=p)
    hs = HydroShare(auth=auth)
    return hs


def getResourceContent(hs_connection, resourceid, destination='.'):
    """
    Downloads the content of HydroShare resource to the JupyterHub userspace

    Args:
        hs_connection: secure connection to hydroshare, HydroShare.HydroShare() object
        resourceid: id of the HydroShare resource to query
        destination: path relative to /user/[username]/notebooks/ipynbs/content

    """
    
    jupyter_username = getpass.getuser()
    ip = socket.gethostbyname(socket.gethostname())
    base_dir = 'http://%s/user/%s/tree/ipynbs/content' % (ip, jupyter_username)
    dst = os.path.join(base_dir, destination)
    hs_connection.getResource(resourceid, destination=dst, unzip=True)
    return dst




