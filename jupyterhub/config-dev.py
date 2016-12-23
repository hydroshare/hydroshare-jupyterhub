import os
from os.path import *
import sys

# load environment variables
os.environ['HYDROSHARE_USE_WHITELIST'] = '0'
os.environ['HYDROSHARE_REDIRECT_COOKIE_PATH'] = '/usr/local/etc'
os.environ['JUPYTER_NOTEBOOK_DIR'] = '/home/hydro/hydroshare-jupyterhub/notebooks'
os.environ['JUPYTER_USERSPACE_DIR'] = '/home/hydro/userspace'
os.environ['JUPYTER_HUB_IP']='192.168.56.101'
os.environ['DOCKER_SPAWNER_IP']='192.168.56.101'
os.environ['JUPYTER_PORT']='8000'
os.environ['JUPYTER_LOG']='./jupyterhub.log'
os.environ['JUPYTER_USER']='hydro'
os.environ['JUPYTER_REST_PORT']='8080'
os.environ['JUPYTER_REST_IP']='192.168.56.101'

# get the project root
root = abspath(dirname(__file__))

# append the dockerspawner submodule to the path
sys.path.append(abspath(join(root, '../dockerspawner/dockerspawner')))

# append the oauthenticator submodule to the path
sys.path.append(abspath(join(root, '../oauthenticator/oauthenticator')))

# append the parent dir
sys.path.append(abspath(join(root, '../')))

# Configuration file for Jupyter Hub
c = get_config()

c.JupyterHub.api_tokens = {"6b2ee57055123b95be0df3a3c3609e09886e419b7f032db219dc8235de93ed44":"jupyter"}

try:
    # spawn with Docker
    c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
    c.JupyterHub.confirm_no_ssl = True
    c.JupyterHub.port = int(os.environ['JUPYTER_PORT'])
    c.DockerSpawner.hub_ip_connect = os.environ['DOCKER_SPAWNER_IP']
    c.JupyterHub.hub_ip = os.environ['DOCKER_SPAWNER_IP']
    c.JupyterHub.extra_log_file = os.environ['JUPYTER_LOG']
    userspace = os.path.join(os.environ['JUPYTER_USERSPACE_DIR'], '{username}')
except Exception as e:
    print('Error setting JupyterHub settings from environment variables.\n',
          'Please make sure that the following environment variables are set properly in ./env:\n',
          '  JUPYTER_PORT\n',
          '  JUPYTER_IP\n',
          '  JUPYTER_LOG\n'
          '  JUPYTER_USERSPACE_DIR\n\n',
          '%s' % e)
    sys.exit(1)

# TURN OFF OAUTH WHEN DEVELOPING LOCALLY
# OAuth with HydroShare
#c.JupyterHub.authenticator_class = 'oauthenticator.HydroShareOAuthenticator'
#c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# notebook_path = abspath(join(dirname(__file__), '../notebooks'))
static = abspath(join(dirname(__file__), '../static/custom'))

# mount the unittest directory
tests = abspath(join(dirname(__file__), '../tests'))

c.DockerSpawner.volumes = {
    userspace: '/home/jovyan/work',
    static: '/home/jovyan/work/notebooks/.jupyter/custom',
    tests: '/home/jovyan/libs/tests',
}

# http://stackoverflow.com/questions/37144357/link-containers-with-the-docker-python-api
c.DockerSpawner.extra_host_config = {
    'privileged':True,
    'cap_add':['SYS_ADMIN','MKNOD'],
    'devices':['/dev/fuse'],
    'security_opt':['apparmor:unconfined']
}

# ADD AUTHENTICATED USER THAT MATCHES VIRTUALBOX USER
c.Authenticator.whitelist = {'jupyter'}


