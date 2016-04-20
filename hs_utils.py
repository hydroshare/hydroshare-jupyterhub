import os
import getpass
import socket
from hs_restclient import HydroShare


def getSecureConnection(username):
    p = getpass.getpass('Enter you HydroShare Password: ')
    auth = HydroShareAuthBasic(username=username, password=p)
    hs = HydroShare(auth=auth)
    return hs


def getResourceContent(hs_connection, resourceid, destination='.'):
    jupyter_username = getpass.getuser()
    ip = socket.gethostbyname(socket.gethostname())
    base_dir = 'http://%s/user/%s/tree/ipynbs/content' % (ip, jupyter_username)
    dst = os.path.join(base_dir, destination)
    hs.getResourceContent(resourceid, destination=dst, unzip=True)
    return dst




