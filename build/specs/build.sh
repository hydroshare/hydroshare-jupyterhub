#!/bin/bash 

docker build -f rabbit.dockerfile -t cuahsi/specs-rabbit .
docker build -f celery.dockerfile -t cuahsi/specs-worker .
