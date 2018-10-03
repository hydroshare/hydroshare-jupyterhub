#!/usr/bin/env bash

git clone https://github.com/sstephenson/bats.git
cd bats
./install.sh /usr/local

git clone https://github.com/ztombol/bats-support /tmp/bats-support
git clone https://github.com/ztombol/bats-assert /tmp/bats-assert
git clone https://github.com/ztombol/bats-file /tmp/bats-file

#echo "PATH=/home/jovyan/bin:$PATH" > ~/.env


