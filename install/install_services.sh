#!/usr/bin/env bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

####################################### 
# Install Environment File (Base Dir) #
####################################### 

echo "installing jupyterhub common files"
JH=/etc/jupyterhub
mkdir -p $JH

# jupyterhub server dir
JH=/etc/jupyterhub
mkdir -p $JH
cp env $JH
cp -r static $JH

# server dir
JHS=/etc/jupyterhub/server
mkdir -p /etc/jupyterhub/server/redirect

# rest dir
JHR=/etc/jupyterhub/rest
mkdir -p $JHR

# cull dir
JHC=/etc/jupyterhub/cull
mkdir -p $JHC

####################################### 
# Install Jupyterhub Server           #
####################################### 

echo "installing jupyterhub service"
cp config.py $JHS
cp jupyterhub.service /lib/systemd/system

####################################### 
# Install JupyterHub Rest Server      #
####################################### 

echo "installing jupyterhub rest server service"
cp jupyterhub_rest_server_start.py $JHR
cp jupyterhubrestserver.service /lib/systemd/system

####################################### 
# Install JupyterHub Culling          #
####################################### 

echo "installing jupyterhub culling service"
cp cull_idle_servers.py $JHC


####################################### 
# Enable The Services                 #
#######################################
 
systemctl daemon-reload
#systemctl enable jupyterhub
#systemctl enable jupyterhubrestserver
#systemctl enable jupyterhubculling
