#!/bin/bash 

# This is a script for preparing and running modflow tests

# get input argument: image name
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Must provide an image name to test against."
    exit 1
fi
IMAGE=$1

# exit early if unzip is not installed
if ! [ -x "$(command -v unzip)" ]; then
  echo 'Error: unzip is not installed.' >&2
  exit 1
fi

# get the modflow examples
wget https://water.usgs.gov/ogw/modflow/mf6.0.2.zip
unzip -x mf6.0.2.zip

# move the custom test cases into this directory
cp modflow-tests.sh mf6.0.2/examples/modflow-tests.sh
chmod +x mf6.0.2/examples/modflow-tests.sh

# run tests inside singleuser container
docker run --rm -u root -ti -v $(pwd)/mf6.0.2:/tmp/mf6.0.2 -v $(pwd)/prepare-test-env.sh:/tmp/prepare-test-env.sh $IMAGE \
/bin/bash -c "cd /tmp; ./prepare-test-env.sh; cd /tmp/mf6.0.2/examples; ./modflow-tests.sh"

#cuahsi/singleuser \

# remove Testdata
rm -rf $(pwd)/mf6.0.2 $(pwd)/mf6.0.2.zip


