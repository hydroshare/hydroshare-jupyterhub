#!/bin/bash 

# This is a script for running the taudem tests

# get input argument: image name
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Must provide an image name to test against."
    exit 1
fi
IMAGE=$1

# exit early if git is not installed
if ! [ -x "$(command -v git)" ]; then
  echo 'Error: git is not installed.' >&2
  exit 1
fi

# get the taudem test data from github
git clone https://github.com/dtarb/TauDEM-Test-Data.git; git pull

# move the custom test cases into this directory
cp taudem-tests.sh TauDEM-Test-Data/Input/taudem-tests.sh
chmod +x TauDEM-Test-Data/Input/taudem-tests.sh


docker run --rm -u root -ti -v $(pwd)/TauDEM-Test-Data:/tmp -v $(pwd)/prepare-test-env.sh:/tmp/prepare-test-env.sh $IMAGE \
/bin/bash -c "cd /tmp; ./prepare-test-env.sh; cd /tmp/Input; ./taudem-tests.sh"

# remove Testdata
rm -rf $(pwd)/TauDEM-Test-Data


