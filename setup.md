This repository contains files for setting up and testing the HydroShare-Jupyterhub integration.  The project is subdivided into the following folders:

1. docker - Dockerfile and associated scripts for setting up the HydroShare container
2. jupyterhub - the jupyterhub run and configuration directory
3. notebooks - sample ipynbs that are copied into Jupyter userspace
4. test - test scripts, test website that envokes the rest endpoint

## Installation Instructions  
Note: *These steps have only been tested on CentOS7*  


**set environment vars**  
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




### Build Docker Image  

**start the docker service**  
`sudo service docker start`  

**build the docker file**  
`cd [project_root]/docker`  
`docker build -t jupyterhub/singleuser  . `

### Run the server

*Create a screen session*  
`screen -S jupyter`  
`cd [project_root]/jupyterhub`  
`sudo ./run.sh`
`CTRL A+D`


### Run the REST server  
*Create a screen session*    
`screen -S rest`    
`cd [project_root]/rest`    
`sudo python3 jupyterhub_server.py`
`CTRL A+D`
