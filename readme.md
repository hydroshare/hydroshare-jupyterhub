
This repository contains files for setting up and testing the HydroShare-Jupyterhub integration.  The project is subdivided into the following folders:

1. docker - Dockerfile and associated scripts for setting up the HydroShare container
2. jupyterhub - the jupyterhub run and configuration directory
3. notebooks - sample ipynbs that are copied into Jupyter userspace
4. oauthenticator - an oauth2 plugin for hydroshare authentication
4. rest - a rest interface for accessing Jupyter notebooks from HydroShare
4. test - test scripts, test website that envokes the rest endpoint

Note: *These steps have only been tested on CentOS7*

### System Setup

**Update the system**  
`yum check-update`  
`yum update`  

**Install base libraries**  
`yum install -y openssh-server git vim wget screen`  

**Install Python 3**  
`yum install -y epel-release python34 python34-devel`  

**Install pip3**  
`wget https://bootstrap.pypa.io/get-pip.py`  
`python3 get-pip.py`  

**install node**  
`yum install -y nodejs npm`  
`npm install -g configurable-http-proxy`  

**install jupyterhub**  
`pip3 install "ipython[notebook]" jupyterhub`  

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

### DockerSpawner + OAuth 

**install dockerspawner**    
`cd [project_root]`
`git clone https://github.com/jupyterhub/dockerspawner.git`  
`cd dockerspawner`  
`pip3 install -r requirements.txt`  
`python3 setup.py install`  

**install oauth library**  
`cd [project_root]/oauthenticator`  
`python3 setup.py install`  
`cd ..`

**set environment vars**  
`cd [project_root]/jupyterhub`  
`touch env`  
```
$vim env
  export HYDROSHARE_CLIENT_ID=[INSERT CLIENT ID]
  export HYDROSHARE_CLIENT_SECRET=[INSERT CLIENT SECRET]
  export OAUTH_CALLBACK_URL=http://[YOU IP ADDRESS]/hub/oauth_callback
  export HYDROSHARE_USE_WHITELIST=0
  export JUPYTER_NOTEBOOK_DIR=[PATH TO NOTEBOOKS]
  export JUPYTER_USERSPACE_DIR=[PATH TO USERSPACE]
```

### Build Docker Image  

**install docker**   
`sudo yum install docker` 

**start the docker service**  
`sudo service docker start`  

**add user to docker group**  
`sudo groupadd docker`  
`sudo usermod -aG docker [username]`  
`sudo service docker start`  

**build the docker file**  
`cd [project_root]/docker`  
`docker build -t jupyterhub/singleuser  . `

**Open the port to communicate with the docker container**  
`sudo firewall-cmd --zone=public --add-port 8081/tcp --permanent`  
`sudo firewall-cmd --reload`  

### Run the server

*Create a screen session*  
`screen -S jupyter`  
`cd [project_root]/jupyterhub`  
`sudo ./run.sh`
`CTRL A+D`

### Cleanup docker images (cron job)  
Delete docker images after they have been active for 1 day.  This will ensure that the users environment is rebuilt with the latest notebooks periodically.  

**make the cleanup script executable**  
`cd [prject_root]/docker`  
`chmod +x cleanup.sh`  

**load the cleanup script into crontab**  
`crontab cleanup.cron`  







