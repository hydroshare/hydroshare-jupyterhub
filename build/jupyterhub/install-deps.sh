#!/bin/bash
set -x
set -e

export PATH=/opt/conda/bin:$PATH

apt-get update 
apt-get install --fix-missing -y --no-install-recommends wget git vim


# Install dockerspawner, oauth, postgres
/opt/conda/bin/conda install -yq psycopg2=2.7
/opt/conda/bin/conda clean -tipsy

cd /srv

git clone -b upstream-pull https://github.com/hydroshare/dockerspawner.git
(cd dockerspawner && pip install .)

git clone -b upstream-pull https://github.com/hydroshare/oauthenticator.git
pip install -e oauthenticator
#(cd oauthenticator && python3 setup.py install)
 
git clone https://github.com/hydroshare/hydroshare-jupyterhub.git 
(cd hydroshare-jupyterhub/jupyterhub_rest_server; git pull;  python3 setup.py install)

# add docker-cli
cd /tmp
wget https://download.docker.com/linux/static/stable/x86_64/docker-17.09.0-ce.tgz
tar -xf docker-17.09.0-ce.tgz 
cp /tmp/docker/docker /usr/bin/docker

# make sure we're using jupyterhub v0.8.1
pip install -U jupyterhub==0.8.1

rm -rf /tmp/*
