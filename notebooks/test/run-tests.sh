#!/usr/bin/env bash

cd "$(dirname "$0")"

# run python2 tests
echo "Running Python2 Tests"
python2 $(which nosetests)


# run python3 tests
echo "Running Python3 Tests"
python $(which nosetests)


echo "Finished"

