#!/bin/bash
set -x
set -e

# grab envs from file
#source ./env

## install cmake for TauDEM v5.3.8
#cd /tmp
#wget https://cmake.org/files/v3.11/cmake-3.11.0.tar.gz
#tar xf cmake-3.11.0.tar.gz
#cd cmake-3.11.0
#./configure
#make

##curl -sSL https://cmake.org/files/v3.5/cmake-3.5.2-Linux-x86_64.tar.gz | sudo tar -xzC /tmp
##mv /tmp/cmake-3.5.2-Linux-x86_64/bin/* /usr/local/bin/

# apt update
# apt-get install -y cmake
# source ~/.bashrc
#cd ~/libs/TauDEM/src
# mkdir build
# cd build

#################
# INSTALL GCC 7 #
#################

# Use gdal 2.1, libgdal-dev and gdal-bin.a
# apt-get install gdal-bin libgdal-dev
# apt-get install gdal-bin=2.1.3+dfsg-1~xenial2
# might need to uninstall previous versions of gdal
# gdal-config --version should show 2.1.3


#sudo apt update
#sudo apt-get install -y software-properties-common python-software-properties
#sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
#sudo apt update
#sudo apt install -y gcc-7 g++-7
#
#sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-7 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-7 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-7
#
#sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-5 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-5 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-5
#
#sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 10
#sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 10
#
#Now, gcc-7 is the default compiler. To change back to gcc-5, you need to run :
#sudo update-alternatives --config gcc
#Then select gcc-5.
# e.g. 
# echo 1 | update-alternatives --config gcc
# echo 2 | update-alternatives --config gcc
###################################
#          INSTALL TAUDEM         #
###################################

# switch to gcc, g++ 7
#echo $GCC7 | update-alternatives --config gcc
#echo $GPP7 | update-alternatives --config g++ 

# TAUDEM v5.3.8 - build and install taudem (must happen before rhesyss b/c of gdal conflicts)
#git clone --branch v5.3.8 https://github.com/dtarb/TauDEM.git /home/jovyan/libs/TauDEM

# TAUDEM v5.3.9 (Develop_
git clone --branch Develop https://github.com/dtarb/TauDEM.git /home/jovyan/libs/TauDEM
cd /home/jovyan/libs/TauDEM
git checkout bceeef2f6a399aa23749a7c7cae7fed521ea910f
cd /home/jovyan/libs/TauDEM/src
sed -i 's#\.\.#/usr/local/bin#g' makefile
make 
rm -rf /home/jovyan/libs/TauDEM

## test the installation
#cd /home/jovyan/libs
#git clone https://github.com/dtarb/TauDEM-Test-Data.git /home/jovyan/libs/TauDEM-Test-Data
#cd /home/jovyan/libs/TauDEM-Test-Data/Input/
#
## replace windows bat commands with bash
#cp testall.bat testall.sh
#sed -i 's/[rR]em /#/g' testall.sh
#for i in `cat testall.sh | grep ^mpie | cut -f 4 -d' ' | sort  | uniq | tail -n +2`; do low=`echo -n $i | tr [A-Z] [a-z]`; sed -i s/$i\ /$low\ /g testall.sh; done
#
#chmod +x testall.sh
#
#./testall.sh
#
