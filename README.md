# HydroShare Jupyterhub Notebook Server

The HydroShare Jupyterhub Notebook Server is an environment specifically designed to link HydroShare resources to user-generated web computations (e.g. Python notebooks). It extends the FOSS [JupyerHub](https://github.com/jupyterhub/jupyterhub) project to incorporate libraries designed to provided seamless interaction with HydroShare web resources and core functionality.  This project also leverages [docker](https://www.docker.com/) containers to provide users with isolated linux environments where they can build, modify, and store custom Jupyter notebooks and data.  While this software can be deployed as a stand-alone application, it is intended to interact with HydroShare resources via a REST API, e.g. [Jupyer-NCSA](https://www.hydroshare.org/resource/80d9f3b4bc914628a2d1df4ebebcc3fd/) (an instance deployed at the Resourcing Open Geo-spatial Education and Research (ROGER) supercomputer).


# Setup 

The repository contains files for setting up and testing the HydroShare-Jupyterhub integration.  The project is subdivided into the following folders:

1. docker - Dockerfile and associated scripts for setting up the HydroShare container
2. jupyterhub - the jupyterhub run and configuration directory
3. notebooks - sample ipynbs that are copied into Jupyter userspace
4. test - test scripts, test website that envokes the rest endpoint

## Installation Instructions  
Note: *These steps have only been tested on CentOS7*  


### Configure Environment Variables**  
These environment variables are loaded when the jupyterhub server is started.  To keep the code generic, several additional variables have been added which are used in `jupyter_config.py` to prepare the jupyterhub environment.   
`cd [project_root]/docker-compose.yml`   

```  
  # Authentication
  HYDROSHARE_CLIENT_ID=[INSERT CLIENT ID]
  HYDROSHARE_CLIENT_SECRET=[INSERT CLIENT SECRET]
  OAUTH_CALLBACK_URL=http://[YOUR IP ADDRESS]/hub/oauth_callback
  
  # HydroShare specific settings
  HYDROSHARE_USE_WHITELIST=0
  HYDROSHARE_REDIRECT_COOKIE_PATH=[PATH TO STORE COOKIES]
  
  # Jupyter Notebook Settings.  These env vars are used to prepare the JupyterHub server during initialization (all required)
  JUPYTER_NOTEBOOK_DIR=[PATH TO NOTEBOOKS]   
  JUPYTER_USERSPACE_DIR=[PATH TO USERSPACE]  
  HOST_USERSPACE_DIR=[PATH TO USERSPACE DIR (HOST)]
  JUPYTER_HUB_IP=[SERVER IP ADDRESS]
  JUPYTER_PORT=[PORT FOR JUPYTER TO LISTEN]
  JUPYTER_LOG=[LOG FILE LOCATION]
  JUPYTER_USER=[LINUX SYSTEM USER]
  DOCKER_SPAWNER_IP=[IP ADDRESS WHERE DOCKER WILL SPAWN CONTAINERS (usually, 8081)]
 
  # Jupyterhub REST Settings
  export JUPYTER_REST_PORT=[PORT FOR REST SERVER TO LISTEN]
  export JUPYTER_REST_IP=[REST SERVER IP ADDRESS]
  
  # name of image to spawn for users, must exist on the host system
  DOCKER_IMAGE_NAME=[DOCKER IMAGE NAME]

  # path to shared python libraries that will be mounted to /home/jovyan/libs/python
  PYTHON_LIBS=[PATH TO SHARED PYTHON LIBS]
  
  # path to sample data to mount to /home/jovyan/sample_data
  SAMPLE_DATA=[PATH TO SAMPLE DATA]
 
```


### Start the JupyterHub Service

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


### Deploy the JupyterHub Service

1. Make sure JH is not running  
   `docker-compose down`  
 
2. Initialize the docker swarm  
   `docker swarm init`  

3. Deploy the JH services  
   `docker stack deploy --compose-file docker-compose.yml jhstack`  

## Helpful commands

   list   : `docker stack ls`
   remove : `docker stack rm [stack name]`
   ps     : `docker stack ps
