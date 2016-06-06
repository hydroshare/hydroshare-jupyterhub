import os

# Configuration file for Jupyter Hub
c = get_config()

try:
    # spawn with Docker
    c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
    c.JupyterHub.confirm_no_ssl = True
    c.JupyterHub.port = int(os.environ['JUPYTER_PORT'])
    c.DockerSpawner.hub_ip_connect = os.environ['JUPYTER_IP']
    c.JupyterHub.hub_ip = os.environ['JUPYTER_IP']
    c.JupyterHub.extra_log_file = os.environ['JUPYTER_LOG']
    userspace = os.path.join(os.environ['JUPYTER_USERSPACE_DIR'], '{username}')
except Exception as e:
    print('Error setting JupyterHub settings from environment variables.  Please make sure that the following environment variables are set properly in ./env:\n  JUPYER_PORT\n  JUPYTER_IP\n  JUPYTER_LOG\n  JUPYTER_USERSPACE_DIR\n\n%s' % e)

#c.JupyterHub.port = 80
#c.DockerSpawner.hub_ip_connect = '129.123.51.34'
#c.JupyterHub.hub_ip = '129.123.51.34'
#c.JupyterHub.extra_log_file = './jupyterhub.log'


# OAuth with HydroShare
c.JupyterHub.authenticator_class = 'oauthenticator.HydroShareOAuthenticator'
c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# mount the userspace directory
print('USERSPACE: ',userspace)
c.DockerSpawner.volumes = {
    userspace: '/home/jovyan/work',
#    '/home/castro/userspace/{username}': '/home/jovyan/work',
}


