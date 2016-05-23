# Configuration file for Jupyter Hub


c = get_config()

# spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
#c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'
c.JupyterHub.confirm_no_ssl = True
c.JupyterHub.port = 80
c.DockerSpawner.hub_ip_connect = '129.123.51.34'
c.JupyterHub.hub_ip = '129.123.51.34'
c.JupyterHub.extra_log_file = './jupyterhub.log'


# OAuth with GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.HydroShareOAuthenticator'
#c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = set()
#c.Authenticator.admin_users = admin = set()

import os

join = os.path.join
here = os.path.dirname(__file__)
with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
#c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

#c.Spawner.notebook_dir = '/home/tony'
#c.Spawner.args = ['--NotebookApp.default_url=/notebooks/Welcome.ipynb']

# mount the userspace directory
c.DockerSpawner.volumes = {
    '/home/castro/userspace/{username}': '/home/jovyan/work',
}


