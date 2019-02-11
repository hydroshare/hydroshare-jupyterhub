# Configuration file for JupyterHub
import os
from oauthenticator.hydroshare import HydroShareOAuthenticator

c = get_config()

cmd = 'python3 /srv/cull_idle_servers.py --timeout=%d --max_age=%d' % \
      (int(os.environ['CONTAINER_IDLE_TIMEOUT']), int(os.environ['CONTAINER_MAX_AGE']))
c.JupyterHub.services = [
{
    'name': 'cull-idle',
    'admin': True,
    'command': cmd.split(),
}]

c.Authenticator.admin_users = {'tonycastronova', 'pdoan'}

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Spawn containers from this image
c.DockerSpawner.container_image = os.environ['DOCKER_NOTEBOOK_IMAGE']

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
userspace = os.path.join(os.environ['JUPYTER_USERSPACE_DIR_HOST'], '{username}')
c.DockerSpawner.volumes = {
  userspace: notebook_dir,
#  os.environ['JUPYTER_STATIC_DIR_HOST']: '/home/jovyan/work/.jupyter/custom'
  os.environ['JUPYTER_STATIC_DIR_HOST']: '/opt/conda/lib/python3.6/site-packages/notebook/static/custom',
  '/root/hydroshare-jupyterhub/build/specs/specworker': '/home/jovyan/libs/specworker'
}

# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8080

# TLS config
c.JupyterHub.port = 443
c.JupyterHub.ssl_key = os.environ['SSL_KEY']
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

# Authenticate users with HydroShare OAuth
c.JupyterHub.authenticator_class = HydroShareOAuthenticator
c.HydroShareOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

# Persist hub data on volume mounted inside container
data_dir = os.environ.get('DATA_VOLUME_CONTAINER', '/data')

c.JupyterHub.cookie_secret_file = os.path.join(data_dir,
    'jupyterhub_cookie_secret')

c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host=os.environ['POSTGRES_HOST'],
    password=os.environ['POSTGRES_PASSWORD'],
    db=os.environ['POSTGRES_DB'],
)

# Spawner configuration/settings
# http://stackoverflow.com/questions/37144357/link-containers-with-the-docker-python-api
c.DockerSpawner.extra_host_config = {
    'cap_add':['SYS_PTRACE'],
    'security_opt':['apparmor:unconfined'],
    'mem_limit':os.environ['DOCKER_MEM_LIMIT'],
}

# Set spawner environment variables
c.DockerSpawner.environment = {
    'JUPYTER_DOWNLOADS': os.environ['JUPYTER_DOWNLOADS']
}

# spawner timeout
c.Spawner.start_timeout = int(os.environ['SPAWNER_START_TIMEOUT'])
c.Spawner.http_timeout = int(os.environ['SPAWNER_HTTP_TIMEOUT'])
