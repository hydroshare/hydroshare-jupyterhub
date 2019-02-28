
## System Setup

*These instructions were tested on CentOS 7*
All images referenced below can be found at: https://hub.docker.com/u/cuahsi 

### 1. Install Docker

    $ sudo yum install -y docker-ce
    $ curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    $ chmod +x /usr/local/bin/docker-compose

### 2. Adjust docker base image size

    $ vi /etc/sysconfig/docker-storage

      DOCKER_STORAGE_OPTIONS="--storage-opt dm.basesize=25G"

    $ systemctl restart docker


### 3. Create Userspace for JupyterHub

Make a directory to store user data  

    $ mkdir -p /[path to data on host]/userspace/_global/jupyterhub
   
Collect the default notebooks and static files, and move them into the userspace directory.

    $ git clone https://github.com/hydroshare/hydroshare-jupyterhub.git /tmp/hydroshare-jupyterhub
    $ cp -r /tmp/hydroshare-jupyterhub/notebooks/ /[path to data on host]/userspace/_global/notebooks
    $ cp -r /tmp/hydroshare-jupyterhub/static/ /[path to data on host]/userspace/_global/static
        

### 4. Configure the Environment
    
Create secrets directory that will be used docker-compose

    $ mkdir secrets 
    
Add ssl cert and key

    $ cp /[path to ssl]/*.crt secrets/jupyterhub.crt
    $ cp /[path to ssl]/*.key secrets/jupyterhub.key

Create OAuth environment file 

    $ cat > secrets/oauth.env 

     HYDROSHARE_CLIENT_ID=[oauth id]
     HYDROSHARE_CLIENT_SECRET=[oauth secret]
     HYDROSHARE_REDIRECT_COOKIE_PATH=/[path to data on host]/userspace/_global/jupyterhub/redirect
     OAUTH_CALLBACK_URL=https://[server url]/hub/oauth_callback
     <CTRL-D>
    
Create Postgres environment file  

    $ echo POSTGRES_PASSWORD=$(openssl rand -hex 32) > secrets/postgres.env
   
Create specs environment file. This should be ':' separated list of images that are installed on the host machine *(Optional)*

    $ echo IMAGES=specs/summa: > secrets/specs.env
    
Create JupyterHub Environment File. After copying this file, you'll need to edit the variables defined within.

    $ cp deploy/env.template .env


### Prepare JupyterHub volumes and network
    
    $ docker volume create --name jupyterhub-data
    $ docker volume create --name jupyterhub-db-data
    $ docker network create jupyterhub-network

### Pull docker images and run tests

    $ docker pull cuahsi/singleuser:latest  

Run the tests  

    $ cd ../cuahsi/singleuser/test  
    $ ./run-taudem-tests.sh  
    $ ./run-modflow-tests.sh  

### Pull Specs Images *(Optional)*

*Note*: if this step is skipped, celery and rabbit elements must be commented in docker-compose.yml

    $ docker pull cuahsi/specs-worker:[tag]
    $ docker pull cuahsi/specs-rabbit:[tag]

Collect specs model images  

    $ docker pull cuahsi/summa:sopron
    $ docker pull ...

### Scale the celery workers

    $ cd deploy
    $ docker-compose scale worker=5

### Start the JH server

    $ docker-compose up -d

### View logs

    $ docker logs jupyterhub
    $ docker logs jupyterhub-db
    $ docker logs jupyterhub-rest

