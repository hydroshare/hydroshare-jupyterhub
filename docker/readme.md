

start the docker service 

`sudo service docker start`


build the docker file, assuming that the Dockerfile resides in the current directory

`cd docker`

`docker build -t jupyterhub/singleuser  . `


Connect to container as root (for maintenance)

`docker exec -ti -u root [container name] /bin/bash`


Run image as container  
`docker run -i -t [image id] /bin/bash`  

Remove all docker containers and images

```
# Delete all containers
docker rm $(docker ps -a -q)

# Delete all images
docker rmi $(docker images -q)
```

To update the volume mounts for a container, it just needs to be stopped, hen let jupyterhub restart it at next login.

`docker stop [container id]`


