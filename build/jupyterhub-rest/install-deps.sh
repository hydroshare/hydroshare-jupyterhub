#!/bin/bash 
set -x
set -e

apt-get update
apt-get install --fix-missing -y --no-install-recommends \
 git \
 vim \
 ca-certificates \
 python3 \
 python3-pip

pip3 install setuptools wheel

cd /srv
git clone https://github.com/hydroshare/hydroshare-jupyterhub.git
#rm hydroshare-jupyterhub/jupyterhub_rest_server/jupyterhub_rest_server/utilities.py
#cp utilities.py hydroshare-jupyterhub/jupyterhub_rest_server/jupyterhub_rest_server/utilities.py
(cd hydroshare-jupyterhub; git pull; pip3 install -e jupyterhub_rest_server)
