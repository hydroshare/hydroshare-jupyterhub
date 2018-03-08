import os
from os.path import *
import sys
from oauthenticator.hydroshare import HydroShareOAuthenticator
from dockerspawner.dockerspawner import DockerSpawner

# Configuration file for Jupyter Hub
c = get_config()

# set container culling properties
#c.JupyterHub.services = [
#    {
#        'name': 'cull-idle',
#        'admin': True,
#        'command': 'python3 /etc/jupyterhub/cull/cull_idle_servers.py --timeout=3600'.split(),
#    }
#]

#ssl_dir = '/etc/ssl/certs/cuahsi.org'
jbase = os.environ['JUPYTER_BASE']
c.JupyterHub.cookie_secret_file = os.path.join(jbase, 'cookie_secret')
c.JupyterHub.db_url = os.path.join(jbase, 'jupyterhub.sqlite')

# spawn with Docker
c.JupyterHub.spawner_class = DockerSpawner
#c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK']

c.DockerSpawner.image = os.environ['DOCKER_IMAGE_NAME']
c.DockerSpawner.notebook_dir = '/home/jovyan/work'

c.JupyterHub.confirm_no_ssl = True
if int(os.environ['SSL_ENABLED']):
    # https on :443
    c.JupyterHub.confirm_no_ssl = False
    c.JupyterHub.port = 443
    c.JupyterHub.ssl_key = os.environ['SSL_KEY']
    c.JupyterHub.ssl_cert = os.environ['SSL_CERT']


c.JupyterHub.port = int(os.environ['JUPYTER_PORT'])
c.DockerSpawner.remove_containers = True
c.JupyterHub.hub_ip = '0.0.0.0'


#userspace = os.path.join(os.environ['HOST_USERSPACE_DIR'], '{username}')
userspace = os.path.join(os.environ['JUPYTER_USERSPACE_DIR'], '{username}')

# OAuth with HydroShare
c.JupyterHub.authenticator_class = HydroShareOAuthenticator
c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

#mount the userspace directory
c.DockerSpawner.volumes = {
   userspace: '/home/jovyan/work',
   os.environ['JUPYTER_STATIC_DIR']: '/home/jovyan/.jupyter/custom',
#   os.environ['PYTHON_LIBS']: '/home/jovyan/libs/python',
}

#mount the userspace directory
c.DockerSpawner.read_only_volumes = {
   os.environ['PYTHON_LIBS']: '/home/jovyan/libs/python',
   os.environ['SAMPLE_DATA']: '/home/jovyan/sample_data',
}

## SSL
##c.NotebookApp.certfile = u'/volume/hydro-develop/cert.pem'
##c.NotebookApp.keyfile = u'/volume/hydro-develop/key.pem'
#
#
# Spawner configuration/settings
# http://stackoverflow.com/questions/37144357/link-containers-with-the-docker-python-api
#c.DockerSpawner.extra_host_config = {
#    'privileged':True,
#    'devices':['/dev/fuse'],
#    'cap_add':['SYS_ADMIN','MKNOD', 'SYS_PTRACE'],
#    'cap_add':['SYS_PTRACE'],
#    'security_opt':['apparmor:unconfined'],
#    'mem_limit':'16g'
#}

#c.NotebookApp.extra_static_paths = ['/home/jovyan/work/notebooks/.ipython/profile_default/static']
