import os

# Configuration file for Jupyter Hub
c = get_config()

# spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.confirm_no_ssl = True
c.JupyterHub.port = 80
c.DockerSpawner.hub_ip_connect = '129.123.51.34'
c.JupyterHub.hub_ip = '129.123.51.34'
c.JupyterHub.extra_log_file = './jupyterhub.log'


# OAuth with HydroShare
c.JupyterHub.authenticator_class = 'oauthenticator.HydroShareOAuthenticator'
c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# mount the userspace directory
c.DockerSpawner.volumes = {
    '/home/castro/userspace/{username}': '/home/jovyan/work',
}


