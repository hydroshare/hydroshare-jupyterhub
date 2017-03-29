#!/usr/bin/env bash


if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

PWD=$( dirname $( readlink -f ${BASH_SOURCE[0]} ) )

####################################### 
# Install Environment File (Base Dir) #
####################################### 

echo "installing jupyterhub common files"
JH=/etc/jupyterhub
mkdir -p $JH

# jupyterhub server dir
JH=/etc/jupyterhub
mkdir -p $JH
cp $PWD/env $JH
cp -r $PWD/static $JH

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
cp $PWD/config.py $JHS

# write the unit file since the ExecStart path will change based on the system (i.e. LUbuntu vs CentOS) 
JSERVICE=$PWD/jupyterhub.service
echo "[Unit]" > $JSERVICE
echo "Description=JupterHub" >> $JSERVICE
echo -e "\n[Service]" >> $JSERVICE
echo "EnvironmentFile=/etc/jupyterhub/env" >> $JSERVICE
echo "WorkingDirectory=/etc/jupyterhub/server" >> $JSERVICE
echo "ExecStart=$(which jupyterhub) -f $JHS/config.py" >> $JSERVICE
cp $JSERVICE /lib/systemd/system

####################################### 
# Install JupyterHub Rest Server      #
####################################### 

echo "installing jupyterhub rest server service"
cp $PWD/jupyterhub_rest_server_start.py $JHR
# write the unit file since the ExecStart path will change based on the system (i.e. LUbuntu vs CentOS) 
RSERVICE=$PWD/jupyterhubrestserver.service
echo "[Unit]" > $RSERVICE
echo "Description=JupterHubRestServer" >> $RSERVICE
echo -e "\n[Service]" >> $RSERVICE
echo "EnvironmentFile=/etc/jupyterhub/env" >> $RSERVICE
echo "WorkingDirectory=/etc/jupyterhub/rest" >> $RSERVICE
echo "ExecStart=$(which python3) $JHR/jupyterhub_rest_server_start.py" >> $RSERVICE
cp $JSERVICE /lib/systemd/system

####################################### 
# Install JupyterHub Culling          #
####################################### 

echo "installing jupyterhub culling service"
cp $PWD/cull_idle_servers.py $JHC


####################################### 
# Enable The Services                 #
#######################################
 
systemctl daemon-reload
systemctl enable jupyterhub
systemctl enable jupyterhubrestserver

####################################### 
# Print Success                       #
#######################################

echo "JupyterHub and JupyterHubRest services installed successfully" 
echo "JupyterHub working directory: /etc/jupyterhub"
sudo tree /etc/jupyterhub
