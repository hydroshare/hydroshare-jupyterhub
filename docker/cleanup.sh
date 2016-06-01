#!/usr/bin/env bash

echo Running Cleanup
docker ps -a | grep 'Up [0-9] days' | awk '{print $1}' | xargs --no-run-if-empty docker stop
echo Finished


