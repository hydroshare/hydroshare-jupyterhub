#!/bin/bash
set -x
set -e

# change to gnu 5
echo 1 | update-alternatives --config gcc
echo 1 | update-alternatives --config g++

cd /tmp
wget https://water.usgs.gov/ogw/modflow/mf6.0.2.zip
unzip -x mf6.0.2.zip
cp /tmp/makefile /tmp/mf6.0.2/make
cd /tmp/mf6.0.2/make
make
cp /tmp/mf6.0.2/make/mf6.0.2 /usr/local/bin/mf6.0.2

# install mplleaf
conda install -n root -y mplleaflet

# install FloPy from the development branch
/opt/conda/bin/pip install git+https://github.com/modflowpy/flopy.git

## compile MODFLOW 2005
#cd /tmp
#wget https://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.12.00/MF2005.1_12u.zip
#unzip -x MF2005.1_12u.zip
#cd MF2005.1_12u/make
#sed -i '/F90FLAGS/c\F90FLAGS = -fno-second-underscore' makefile
#sed -i '/CC =*/c\CC = gcc' makefile
##sed -i '/F90FLAGS*/F90FLAGS = -fno-second-underscore/'
##sed -i '/CC =*/CC = gcc/'
#make
#cp mf2005 /usr/local/bin/mf2005

rm -rf /tmp/*
