# HydroShare Jupyterhub Notebook Server

The HydroShare Jupyterhub Notebook Server is an environment specifically designed to link HydroShare resources to user-generated web computations (e.g. Python notebooks). It extends the FOSS [JupyerHub](https://github.com/jupyterhub/jupyterhub) project to incorporate libraries designed to provided seamless interaction with HydroShare web resources and core functionality.  This project also leverages [docker](https://www.docker.com/) containers to provide users with isolated linux environments where they can build, modify, and store custom Jupyter notebooks and data.  While this software can be deployed as a stand-alone application, it is intended to interact with HydroShare resources via a REST API, e.g. [Jupyer-NCSA](https://www.hydroshare.org/resource/80d9f3b4bc914628a2d1df4ebebcc3fd/) (an instance deployed at the Resourcing Open Geo-spatial Education and Research (ROGER) supercomputer).


## Project Structure  
Note: *These steps have only been tested on CentOS7*  

The repository contains files for setting up and testing the HydroShare-Jupyterhub integration.  The project is subdivided into the following folders:

1. docker - Dockerfile and associated scripts for setting up the HydroShare container
2. jupyterhub - the jupyterhub run and configuration directory
3. notebooks - sample ipynbs that are copied into Jupyter userspace
4. test - test scripts, test website that envokes the rest endpoint


## 1. Installation 

### 1.1 System Requirements  

- Linux CentOS 7
- Docker version 17.10+.*-ce

### 1.2 Prepare Host

Upgrade host libraries

```
$ sudo yum -y update
```

Install Git 

```
$ sudo yum install git python-pip
```

Install Docker

```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce
$ docker --version
Docker version 17.12.1-ce, build 7390fc6
```

Enable docker

```
$ sudo systemctl enable docker
$ sudo systemctl start docker
```

Install docker compose

```

$ sudo pip install docker-compose
$ sudo usermod -aG docker $(whoami)
```

Logout and log back in for `usermod` to take effect.

### 1.3 Get Code

```
$ git clone https://github.com/hydroshare/hydroshare-jupyterhub.git
$ cd hydroshare-jupyterhub
$ git checkout dockerized
```

### 1.4 Configure JupyterHub  
These environment variables are loaded when the jupyterhub server is started.  To keep the code generic, several additional variables have been added which are used in `jupyter_config.py` to prepare the jupyterhub environment.   These environment variables must be properly configured in `docker-compose.yml` for the JupyterHub server to run properly.


#### 1.4.1 Authentication Settings
These parameters are necessary to enable user authentication with HydroShare.  They require registering the JupyterHub url via https://www.hydroshare.org/o/applications.  Register a new application using `client type = public`, `authorization grant type = authorization code`, and set the `redirect uris` to the values specified in `docker-compose.yml` (`<jupyterhub url>/hub/oauth_callback`).  Copy the `client id` and `client secret` tokens into the `docker-compose.yml` file and do not share these with anyone. 

```
HYDROSHARE_CLIENT_ID=<client id defined by https://www.hydroshare.org/o/applications>
HYDROSHARE_CLIENT_SECRET=<client secret defined by https://www.hydroshare.org/o/applications>
OAUTH_CALLBACK_URL=<jupyterhub url>/hub/oauth_callback
```

#### 1.4.2 Server Configurations
These parameters are specific to each instance of JupyterHub.


- `HYDROSHARE_REDIRECT_COOKIE_PATH` is the location that JupyterHub cookie will be saved.  This is a path on the host that should be accessible to both the Hub and REST containers.  
- `JUPYTER_NOTEBOOK_DIR` is the location of the sample notebooks and libraries that are provided to each user.  
- `JUPYTER_USERSPACE_DIR` is the location where all user data will be stored. Often this is a path to a mounted directory.
- `JUPYTER_PORT` is the port of the jupyterhub server, usually 80
- `JUPYTER_STATIC_DIR` is the path to static files (i.e. js and css) that will be used by the Hub.  These files initially located in `hydroshare-jupyerhub/jupyterhub/static`


#### 1.4.3 Docker Settings            


- `DOCKER_NETWORK` is the network that singleuser containers will be spawned in.  This network must already exist on the system and can be created via `docker network create -d overlay jhub`.  
- `DOCKER_IMAGE_NAME` is the name of the image that will be used to spawn each singleuser container, usually `cuahsi/singleuser` which can be obtained via `docker pull cuahsi/singluser:latest` 

   
#### 1.4.4 SSL            


- `SSL_ENABLED` indicate if SSL is enabled, 0 or 1  
- `SSL_CERT` is the path to SSL cert if enabled
- `SSL_KEY` is the path to SSL key if enabled


#### 1.4.5 Other Paths
```
PYTHON_LIBS=<path to directory extra of python libraries>
SAMPLE_DATA=<path to sample data>
JUPYTER_BASE=<base directory of jupyter installation on host>
```

#### 1.4.6 Mounting Volumes

The "global" userspace directory must be mounted into the JupyterHub container, same with the hub configuration.  This is done by sepcifiying the source and target paths in the `docker-compose.yml` file which must match those provided as environment variables (above).  Additionally, the docker socket must be mounted as well so that singleuser containers can be launched on demand.  For example, 

```
- type: bind
  source: /remote/data/userspace
  target: /remote/data/userspace
- type: bind
  source: ./jupyterhub/config
  target: /srv/jupyterhub/config
  read_only: true
- type: bind
  source: /var/run/docker.sock
  target: /var/run/docker.sock
```

### 1.5 Start the JupyterHub Service

1. Initialize the swarm.  This is necessary to use overlay networks  
   `$ docker swarm init`

2. Create jupyterhub overlay network  
   `$ docker network create -d overlay --attachable jhub`

3. Build the docker containers  
   `$ docker-compose build`

4. Pull the cuahsi singleuser container  
    `$ docker pull cuahsi/singleuser` 

5. Test the services  
   `$ docker-compose up`


### 1.6 Deploy the JupyterHub Service

1. Make sure JH is not running  
   `docker-compose down`  
 
2. Initialize the docker swarm  
   `docker swarm init`  

3. Deploy the JH services  
   `docker stack deploy --compose-file docker-compose.yml jhstack`  

## 2. Helpful commands  

   list   : `docker stack ls`  
   remove : `docker stack rm [stack name]`  
   ps     : `docker stack ps`  
