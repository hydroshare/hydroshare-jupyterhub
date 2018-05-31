#!/bin/bash
set -x
set -e

#################
#     SETUP     #
#################

#export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
#export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python3.5m"

#mkdir /home/jovyan/libs/boost 

#buildDeps='liblapack-dev python3-dev cmake'
#apt-get update && apt-get install -y libopenblas-dev $buildDeps --no-install-recommends

# change to gnu 5
echo 1 | update-alternatives --config gcc
echo 1 | update-alternatives --config g++

echo $(gcc --version)
echo $(g++ --version)

# download dakota 6.5 and extract
#wget -O /home/jovyan/libs/boost.tar.gz https://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.gz/download

dakota=dakota-6.5-public.src

wget https://dakota.sandia.gov/sites/default/files/distributions/public/$dakota.tar.gz -P /tmp

#tar xzfv /home/jovyan/libs/boost.tar.gz -C /home/jovyan/libs/boost --strip-components 1
mkdir /tmp/$dakota && tar xfz /tmp/$dakota.tar.gz -C /tmp/$dakota --strip-components 1


#cd /home/jovyan/libs/boost 
#./bootstrap.sh --prefix=/usr/local 
#echo "using mpi ;" >> /home/jovyan/libs/boost/tools/build/v2/user-config.jam 
#./b2 --with=all -j 4 install || echo "Errors in boost installation" 
#sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf'
#export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

ldconfig 

# compile dakota
mkdir -p /tmp/$dakota/build 
cd /tmp/$dakota/build 
cp /home/jovyan/libs/dakota*/build/BuildDakota.cmake .
cmake -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python -C BuildDakota.cmake /tmp/$dakota 
make clean 
make
make install

###################
#     CLEANUP     #
###################

#rm -rf /home/jovyan/libs/boost* 
rm -rf /tmp/*
rm -rf /var/lib/apt/lists/* 
buildDeps='liblapack-dev python3-dev cmake'
apt-get purge -y --auto-remove $buildDeps


