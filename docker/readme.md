

start the docker service 

`sudo service docker start`


build the docker file, assuming that the Dockerfile resides in the current directory

`cd docker`

`docker build -t jupyterhub/singleuser  . `


Connect to container as root (for maintenance)

`docker exec -ti -u root [image name] /bin/bash`


Remove all docker containers and images

```
# Delete all containers
docker rm $(docker ps -a -q)

# Delete all images
docker rmi $(docker images -q)
```

