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

### System Requirements  

- Linux CentOS 7
- Docker version 17.10+.*-ce

### 1.1 Prepare Host

Upgrade host libraries

```
$ sudo yum -y update
```

Install Git 

```
$ sudo yum install git
```

Install Docker

```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce
$ docker --version
Docker version 17.12.1-ce, build 7390fc6
```


### 1.2 Get Code

```
$ git clone https://github.com/hydroshare/hydroshare-jupyterhub.git
$ cd hydroshare-jupyterhub
$ git checkout dockerized
```

### 1.2 Configure JupyterHub**  
These environment variables are loaded when the jupyterhub server is started.  To keep the code generic, several additional variables have been added which are used in `jupyter_config.py` to prepare the jupyterhub environment.   These environment variables must be properly configured in `docker-compose.yml` for the JupyterHub server to run properly.


#### 1.2.1 Authentication Settings
These parameters are necessary to enable authentication with HydroShare.  They require registering the JupyterHub url via https://www.hydroshare.org/o/applications

```
HYDROSHARE_CLIENT_ID=<client id defined by https://www.hydroshare.org/o/applications>
HYDROSHARE_CLIENT_SECRET=<client secret defined by https://www.hydroshare.org/o/applications>
OAUTH_CALLBACK_URL=<jupyterhub url>/hub/oauth_callback
```

#### 1.2.2 Server Configurations
These parameters are specific to each instance of JupyterHub.

```
HYDROSHARE_REDIRECT_COOKIE_PATH= <path to save cookies>
JUPYTER_NOTEBOOK_DIR= <path to default notebook directory where sample notebooks are created>
JUPYTER_USERSPACE_DIR= <path to save users' data>
JUPYTER_PORT= <public port of the jupyterhub server, usually 80>
JUPYTER_STATIC_DIR= <path to statics files, i.e. js and css>
```

#### 1.2.3 Docker Settings            

```
DOCKER_NETWORK= <docker network to spawn user containers in>
DOCKER_IMAGE_NAME= <name of the image to spawn for each user, usually cuahsi/singleuser>
```
   
#### 1.2.4 SSL            

```
SSL_ENABLED= <indicate of SSL is enabled, 0 or 1>
SSL_CERT=<path to SSL cert if enabled=1>
SSL_KEY=<path to SSL key of enabled=1>
```

#### Other Paths
```
PYTHON_LIBS=<path to directory extra of python libraries>
SAMPLE_DATA=<path to sample data>
JUPYTER_BASE=<base directory of jupyter installation on host>
```


### 1.3 Start the JupyterHub Service

1. Create jupyterhub overlay network  
   `docker network create -d overlay jhub`

2. Build the docker containers  
   `docker-compose build`

3. Build or Pull the cuahsi singleuser container  
   Pull (recommended):  
       `docker build -t cuahsi/singleuser -f singleuser.dockerfile . ` 

   Build (helpful if modifying base image):  
       `docker pull cuahsi/singluser`

4. Test the services
       `docker-compose up`


### 1.4 Deploy the JupyterHub Service

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
