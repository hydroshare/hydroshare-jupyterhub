import os
from os.path import *
import sys

# Configuration file for Jupyter Hub
c = get_config()

# set container culling properties
c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': 'python3 /etc/jupyterhub/cull/cull_idle_servers.py --timeout=3600'.split(),
    }
]

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

# mount the userspace directory
c.DockerSpawner.volumes = {
   userspace: '/home/jovyan/work',
   os.environ['JUPYTER_STATIC_DIR']: '/home/jovyan/.jupyter/custom',
}

# IRODS settings 
# http://stackoverflow.com/questions/37144357/link-containers-with-the-docker-python-api
#c.DockerSpawner.extra_host_config = {
#    'privileged':True,
#    'cap_add':['SYS_ADMIN','MKNOD'],
#    'devices':['/dev/fuse'],
#    'security_opt':['apparmor:unconfined']
#}

#c.NotebookApp.extra_static_paths = ['/home/jovyan/work/notebooks/.ipython/profile_default/static']

