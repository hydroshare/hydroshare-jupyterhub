import os
from os.path import *

# Configuration file for Jupyter Hub
c = get_config()

try:
    # spawn with Docker
    c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
    c.JupyterHub.confirm_no_ssl = True
    c.JupyterHub.port = int(os.environ['JUPYTER_PORT'])
    c.DockerSpawner.hub_ip_connect = os.environ['DOCKER_SPAWNER_IP']
    c.JupyterHub.hub_ip = os.environ['JUPYTER_HUB_IP']
    c.JupyterHub.extra_log_file = os.environ['JUPYTER_LOG']
    userspace = os.path.join(os.environ['JUPYTER_USERSPACE_DIR'], '{username}')
except Exception as e:
    print('Error setting JupyterHub settings from environment variables.  Please make sure that the following environment variables are set properly in ./env:\n  JUPYER_PORT\n  JUPYTER_IP\n  JUPYTER_LOG\n  JUPYTER_USERSPACE_DIR\n\n%s' % e)

# OAuth with HydroShare
c.JupyterHub.authenticator_class = 'oauthenticator.HydroShareOAuthenticator'
c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

#c.extra_static_paths = ['../static/javascript/custom.js']
#js = abspath(join(basename(__file__), '../../static/js'))
#css = abspath(join(basename(__file__), '../../static/css'))
static = abspath(join(basename(__file__), '../../static/custom'))

#print(js, ' Path Exists: ', exists(js))
#print(css, ' Path Exists: ', exists(css))
print(static, ' Path Exists: ', exists(static))

# mount the userspace directory
print('USERSPACE: ',userspace)
print('MOUNTING USERSPACE: %s -> /home/jovyan/work' % userspace)
c.DockerSpawner.volumes = {
    userspace: '/home/jovyan/work',
    static: '/home/jovyan/work/notebooks/.jupyter/custom',
}

#c.NotebookApp.extra_static_paths = ['/home/jovyan/work/notebooks/.ipython/profile_default/static']

