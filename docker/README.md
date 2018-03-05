# JH Deployment Procedure

### System Requirements
- Linux CentOS 7
- Docker version 17.10.0-ce, build f4ffd25
- docker-compose v

### Build/Installation

1. Create jupyterhub overlay network
   `docker network create -d overlay jhub`

2. Build the docker containers
   `docker-compose build`

3. Build or Pull the cuahsi singleuser container
   Pull: 
       `docker build -t cuahsi/singleuser -f singleuser.dockerfile . `
   Build:
       `docker pull cuahsi/singluser`

4. Test the services
   `docker-compose up`

5. Initialize the swarm (necessary for stack deploy)
   `docker-compose down`  
   `docker swarm init`  

6. Deploy the services
   `docker stack deploy --compose-file docker-compose.yml jhstack`

7. Helpful commands
   list   : `docker stack ls`
   remove : `docker stack rm [stack name]`
   ps     : `docker stack ps jhstack`
