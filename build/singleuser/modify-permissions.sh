#!/bin/bash
set -x
set -e

chown -R jovyan:users /home/jovyan
chown -R jovyan:users /opt/conda

chmod 755 /srv/singleuser/singleuser.sh

