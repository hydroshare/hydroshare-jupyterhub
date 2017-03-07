#!/usr/bin/env bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

# move jupyterhub config files
echo "installing jupyterhub service"
JH=/etc/jupyterhub
mkdir -p $JH
cp env $JH
cp config-dev.py $JH
cp jupyterhub.service /lib/systemd/system

# move jupyterhub rest server files
echo "installing jupyterhub rest server service"
JHRS=/etc/jupyterhub_restserver/redirect
mkdir -p $JHRS
cp env $JHRS
cp jupyterhub_rest_server_start.py $JHRS
cp jupyterhubrestserver.service /lib/systemd/system



systemctl daemon-reload

