#!/usr/bin/env python3
import os
from jupyterhub_rest_server import server

# check that all the required envvars exist
args = ['HYDRPSHARE_REDIRECT_COOKIE', 'JUPYTER_HUB_IP',
        'JUPYTER_REST_IP', 'JUPYTER_PORT', 'JUPYTER_REST_PORT',
        'JUPYTER_USERSPACE_DIR', 'JUPYTER_USER', 'JUPYTER_NOTEBOOK_DIR']
for a in args:
    try:
        v = os.environ[a]
    except:
        print('Missing required EnvVar: %s' % a)

# check that the notebook path exists
dirs = ['JUPYTER_NOTEBOOK_DIR', 'JUPYTER_USERSPACE_DIR']
for d in dirs:
    p = os.environ[d]
    if not os.path.exists(p):
        print('Path does not exist: %s:%s' % (d, p))

# start the server
server.main()
