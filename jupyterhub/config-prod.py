import os
from os.path import *
import sys

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

# OAuth with HydroShare
c.JupyterHub.authenticator_class = 'oauthenticator.HydroShareOAuthenticator'
c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

static = abspath(join(dirname(__file__), '../static/custom'))

# mount the userspace directory
c.DockerSpawner.volumes = {
   userspace: '/home/jovyan/work',
   static: '/home/jovyan/work/notebooks/.jupyter/custom',
}

# http://stackoverflow.com/questions/37144357/link-containers-with-the-docker-python-api
c.DockerSpawner.extra_host_config = {
    'privileged':True,
    'cap_add':['SYS_ADMIN','MKNOD'],
    'devices':['/dev/fuse'],
    'security_opt':['apparmor:unconfined']
}

#c.NotebookApp.extra_static_paths = ['/home/jovyan/work/notebooks/.ipython/profile_default/static']


