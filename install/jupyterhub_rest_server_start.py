#!/usr/bin python3
import os
from jupyterhub_rest_server import server

print('HYDROSHARE_REDIRECT_COOKIE_PATH: %s' % os.environ['HYDROSHARE_REDIRECT_COOKIE_PATH'])
print('JUPYTER_HUB_IP: %s' %os.environ['JUPYTER_HUB_IP'])
print('JUPYTER_REST_IP: %s' % os.environ['JUPYTER_REST_IP'])
print('JUPYTER_PORT: %s' % os.environ['JUPYTER_PORT'])
print('JUPYTER_REST_PORT: %s' % os.environ['JUPYTER_REST_PORT'])
print('JUPYTER_USERSPACE_DIR: %s' % os.environ['JUPYTER_USERSPACE_DIR'])
print('JUPYTER_USER: %s' % os.environ['JUPYTER_USER'])
print('JUPYTER_NOTEBOOK_DIR: %s' % os.environ['JUPYTER_NOTEBOOK_DIR'])
server.main()
