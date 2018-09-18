Deployment Procedure

### Prepare Docker
    
    # install
    $ sudo yum install -y docker-ce

    # adjust docker base image size
    $ vi /etc/sysconfig/docker-storage
    $ DOCKER_STORAGE_OPTIONS="--storage-opt dm.basesize=25G"

    # restart docker
    $ systemctl restart docker

    # install docker-compose
    $ curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    $ chmod +x /usr/local/bin/docker-compose

### Create JH userspace

    # create the userspace and notebook directories
    $ mkdir -p /[path to data on host]/userspace/_global/jupyterhub
   
    # collect the default notebooks and static files
        $ git clone https://github.com/hydroshare/hydroshare-jupyterhub.git /tmp/hydroshare-jupyterhub
        $ cp -r /tmp/hydroshare-jupyterhub/notebooks/ /[path to data on host]/userspace/_global/notebooks
        $ cp -r /tmp/hydroshare-jupyterhub/static/ /[path to data on host]/userspace/_global/static
        

    # adjust user permissions
    Get from Phuong


### Configure Environment
    
    # create secrets directory that will be used docker-compose
    $ mkdir secrets 
    
    # add ssl cert and key
    $ cp /[path to ssl]/*.crt secrets/jupyterhub.crt
    $ cp /[path to ssl]/*.key secrets/jupyterhub.key

    # create oauth environment file
    $ cat > secrets/oauth.env 
     HYDROSHARE_CLIENT_ID=[oauth id]
     HYDROSHARE_CLIENT_SECRET=[oauth secret]
     HYDROSHARE_REDIRECT_COOKIE_PATH=/[path to data on host]/userspace/_global/jupyterhub/redirect
     OAUTH_CALLBACK_URL=https://[server url]/hub/oauth_callback
     <CTRL-D>
    
    # create postgres environment file
    $ echo POSTGRES_PASSWORD=$(openssl rand -hex 32) > secrets/postgres.env
    
    # create specs environment file. This should be ':' separated list of images that are installed on the host machine.
    $ echo IMAGES=specs/summa: > secrets/specs.env
    
    # create .env file
    $ cat > .env 
    # To override these values, set the shell environment variables.
    JUPYTERHUB_VERSION=0.8.0

    # Name of Docker machine
    DOCKER_MACHINE_NAME=jupyterhub
    
    # Name of Docker network
    DOCKER_NETWORK_NAME=jupyterhub-network
    
    # Single-user Jupyter Notebook server container image
    DOCKER_NOTEBOOK_IMAGE=cuahsi/singleuser
    
    # the JupyterHub image we want to use
    JUPYTER_NOTEBOOK_IMAGE=cuahsi/jupyterhub
    
    # Notebook directory in the container.
    # This will be /home/jovyan/work if the default
    # This directory is stored as a docker volume for each user
    DOCKER_NOTEBOOK_DIR=/home/jovyan/work
    
    # Docker run command to use when spawning single-user containers
    DOCKER_SPAWN_CMD=start-singleuser.sh
    
    # Name of JupyterHub container data volume.
    # This is a name for the host volume that docker will use
    DATA_VOLUME_HOST=jupyterhub-data
    
    
    # Data volume container mount point.
    # This is the mounting location inside th jupyterhub container
    DATA_VOLUME_CONTAINER=/data
    
    # JupyterHub container volume container mount point for userdata
    #USERDATA_VOLUME_CONTAINER=/userspace
    
    # Name of JupyterHub postgres database data volume
    DB_VOLUME_HOST=jupyterhub-db-data
    
    # Postgres volume container mount point
    DB_VOLUME_CONTAINER=/var/lib/postgresql/data
    
    # The name of the postgres database containing JupyterHub state
    POSTGRES_DB=jupyterhub
    
    # Name of the user on the jupyter container.
    # This is used to set userspace permissions.
    JUPYTER_USER=root
    
    # location of the userspace on the host machine
    JUPYTER_USERSPACE_DIR_HOST=[e.g. /remote/data/userspace]
    
    # Location of the userspace in the JupyterHub container.  
    JUPYTER_USERSPACE_DIR=[e.g. /userspace]
    
    # Location of shared default notebooks 
    # inside the JupyterHub container.
    # These are used to populate the userspace when the 
    # singleuser container is created.
    JUPYTER_NOTEBOOK_DIR=/userspace/_global/notebooks
    
    # Single user memory limit for the docker container
    DOCKER_MEM_LIMIT=16g
    
    # container culling settings
    CONTAINER_IDLE_TIMEOUT=3600
    CONTAINER_MAX_AGE=86400
    
    # docker spawner timeout settings
    SPAWNER_START_TIMEOUT=300
    SPAWNER_HTTP_TIMEOUT=300
    
    # set ssl paths inside the Notebook and REST containers
    SSL_CRT=/srv/jupyterhub/secrets/jupyterhub.crt
    SSL_KEY=/srv/jupyterhub/secrets/jupyterhub.key
    
    # set hub and rest ip addresses 
    JUPYTER_HUB_IP=[e.g. jupyter.cuahsi.org]
    JUPYTER_REST_IP=[e.g. jupyter.cuahsi.org]
    
    JUPYTER_STATIC_DIR_HOST=[e.g. /remote/data/userspace/_global/jupyterhub/static]


    # add jupyterhub api token to .env
    $ echo JUPYTERHUB_API_TOKEN=$(openssl rand -hex 32) >> .env

### Prepare JupyterHub volumes and network
    
    $ docker volume create --name jupyterhub-data
    $ docker volume create --name jupyterhub-db-data
    $ docker network create jupyterhub-network

### Pull docker images and run tests

    $ docker pull cuahsi/singleuser:latest  

    $ cd ../cuahsi/singleuser/test
        $ ./run-taudem-tests.sh
        $ ./run-modflow-tests.sh

### Build Specs
    $ cd build/specs
    $ ./build.sh

    $ cd build/models/summa
    $ ./build.sh

### Scale the celery workers

    $ cd deploy
    $ docker-compose scale worker=5

### Start the JH server

    $ docker-compose up -d

### View logs

    $ docker logs jupyterhub
    $ docker logs jupyterhub-db
    $ docker logs jupyterhub-rest

