#!/bin/bash


#export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
#export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python3.5m"

# install prerequisites 
buildDeps='liblapack-dev python3-dev cmake'
apt-get update && apt-get install -y libopenblas-dev $buildDeps --no-install-recommends

# get boost 1.53 and extact
mkdir /home/jovyan/libs/boost
wget -O /home/jovyan/libs/boost.tar.gz https://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.gz/download
tar xzfv /home/jovyan/libs/boost.tar.gz -C /home/jovyan/libs/boost --strip-components 1

# change to gnu 5
echo 1 | update-alternatives --config gcc
echo 1 | update-alternatives --config g++

echo $(gcc --version)
echo $(g++ --version)

cd /home/jovyan/libs/boost
./bootstrap.sh --prefix=/usr/local
echo "using mpi ;" >> /home/jovyan/libs/boost/tools/build/v2/user-config.jam
./b2 --with=all -j 4 install || echo "Errors in boost installation"
sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf'
sh -c 'echo "/usr/local/lib/x86_64-linux-gnu" >> /etc/ld.so.conf.d/local.conf'
ldconfig


rm -rf /home/jovyan/libs/boost*
