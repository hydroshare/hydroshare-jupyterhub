#!/bin/bash
set -x
set -e

############################
# ROOT - INSTALL LIBRARIES #
############################

apt-get update && apt-get install --fix-missing -y --no-install-recommends \
    npm nodejs nodejs-legacy wget locales git &&\
    /usr/sbin/update-locale LANG=C.UTF-8 && \
    locale-gen C.UTF-8 && \
    apt-get remove -y locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

export LANG=C.UTF-8
export PATH=/opt/conda/bin:$PATH

# install js dependencies
npm install -g configurable-http-proxy
#npm install -g strftime
npm install -g commander

git clone https://github.com/jupyterhub/jupyterhub.git /srv/jupyterhub

cd /srv/jupyterhub
python3 setup.py js
pip3 install .



git clone https://github.com/hydroshare/hydroshare-jupyterhub.git /srv/hydroshare-jupyterhub
cd /srv/hydroshare-jupyterhub
git submodule init
git submodule update
pip3 install -e dockerspawner
pip3 install -e oauthenticator

# cleanup
rm -rf node_modules ~/.cache ~/.npm


