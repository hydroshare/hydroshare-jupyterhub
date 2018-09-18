#!/bin/bash 

# This is a script for preparing and running Python tests
# get input argument: image name
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Must provide an image name to test against."
    exit 1
fi
IMAGE=$1

# run tests inside singleuser container
docker run --rm -u root -ti \
-v $(pwd)/python3-tests.sh:/tmp/python3-tests.sh \
$IMAGE \
/bin/bash -c "cd /tmp; ./python3-tests.sh"


