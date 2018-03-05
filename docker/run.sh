#!/usr/bin/bash

docker rm -fv $(docker ps -a -q)
sh sync.sh
docker-compose build
docker-compose up
