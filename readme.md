
This repository contains files for setting up and testing the HydroShare-Jupyterhub integration.  The project is subdivided into the following folders:

1. docker - Dockerfile and associated scripts for setting up the HydroShare container
2. jupyterhub - the jupyterhub run and configuration directory
3. notebooks - sample ipynbs that are copied into Jupyter userspace
4. oauthenticator - an oauth2 plugin for hydroshare authentication
4. rest - a rest interface for accessing Jupyter notebooks from HydroShare
4. test - test scripts, test website that envokes the rest endpoint


## Server Setup

Note: *These steps have only been tested on CentOS7*

### System Setup

**Update the system**  
`yum check-update`  
`yum update`  

**Install SSH, GIT, VIM, and WGET**  
`yum install openssh-server`  
`yum install git`  
`yum install vim`  
`yum install wget`

**Install Python 3**  
`yum install epel-release`  
`yum install python34`  (`yum search python3`)  
`yum install python34-devel`  

**Install pip3**  
`wget https://bootstrap.pypa.io/get-pip.py`  
`python3 get-pip.py`  

**install node**  
`yum install nodejs`  
`yum install npm`  
`npm install -g configurable-http-proxy`  

**install jupyterhub**  
`pip3 install "ipython[notebook]"`  
`pip3 install jupyterhub`   

### Web Server Setup

**open firewall ports**  
`firewall-cmd --zone=public --add-port=80/tcp --permanent`  
`firewall-cmd --reload`  

**check that the port was opened successfully**
`firewall-cmd --zone=public --list-ports`  

**Create a group for notebook users**
`groupadd jupyterhub`  
 
**Create shadow group**  
`groupadd shadow`  
`chown root.shadow /etc/shadow` 

**Modify shadow folder permissions**
`chmod 640 /etc/shadow`  

**Give node permission to port 80**
`sudo setcap 'cap_net_bind_service=+ep' /usr/bin/node`

