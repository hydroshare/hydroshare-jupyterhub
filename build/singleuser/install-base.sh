#!/bin/bash
set -x
set -e

############################
# ROOT - INSTALL LIBRARIES #
############################
apt update
apt-get install -y software-properties-common python-software-properties
add-apt-repository -y ppa:ubuntugis/ppa
add-apt-repository -y ppa:ubuntu-toolchain-r/test


apt-get update && apt-get install --fix-missing -y --no-install-recommends \
  gcc-7 \
  g++-7 \
  autoconf=2.69-9 \
  automake=1:1.15-4ubuntu1 \
  libtool=2.4.6-0.1 \
  libgeos-dev \
  libproj-dev \
  build-essential \
  git \
  subversion \
  p7zip-full \
  python \
  python-dev \
  python-pip \
  python-scipy \
  libxml2-dev \
  libxslt-dev \
  libgdal-dev \
  gdal-bin \
  python-gdal \
  grass \
  grass-dev \
  libbsd-dev \
  vlc  \
  libx11-dev \
  man-db \
  wget \
  bash-completion \
  libdb-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/


## build mpich from source (gcc 7)
#git clone git://git.mpich.org/mpich.git /tmp/mpich
#cd /tmp/mpich
#git submodule update --init
#./autogen.sh
#./configure --prefix=/usr
#make -j8
#make -j8 install
#rm -rf /tmp/mpich


#apt-get update && apt-get install --fix-missing -y --no-install-recommends \
#  gcc-7 \
#  g++-7 \
#  libgeos-dev \
#  mpic++ \
#  libproj-dev \
#  libfuse2 \
#  libfuse-dev \
#  build-essential \
#  git \
#  subversion \
#  p7zip-full \
#  python \
#  python-dev \
#  python-pip \
#  python-scipy \
#  libxml2-dev \
#  libxslt-dev \
#  libgdal-dev \
#  gdal-bin \
#  python-gdal \
#  grass \
#  grass-dev \
#  libbsd-dev \
#  vlc  \
#  libx11-dev \
#  man-db \
#  bash-completion \
#  && apt-get clean \
#  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/

#  libgdal-doc 

## dual install gcc, g++ 5 and 7
#update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-7 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-7 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-7 30
#update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-5 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-5 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-5 32
#update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 10
#update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 10

###################################
#          SYSTEM PREP            #
###################################

# create directories
#mkdir /home/jovyan/libs 
chown -R jovyan:users /home/jovyan/libs 
mkdir /home/jovyan/work/notebooks 
chown -R jovyan:users /home/jovyan/work/notebooks

# fetch juptyerhub-singleuser entrypoint
#wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser 
#chmod 755 /usr/local/bin/jupyterhub-singleuser
chmod 755 /srv/singleuser/singleuser.sh

# fetch the ecohydro config file
#https://raw.github.com/selimnairb/RHESSysWorkflows/master/docs/config/ecohydro-Linux.cfg /home/jovyan/.ecohydro.cfg
chown jovyan:users /home/jovyan/.ecohydro.cfg

####################################
#      SETUP CONDA ENVIRONMENTS    #
####################################

## upgrade andaconda
#conda update conda -y 
#conda clean --all -y
#
#conda update conda -y 
#conda create -y -n python2 python=2 
#conda create -y -n R 
#conda clean --all -y
#
## link environments to bin
#ln -sf /opt/conda/bin/python /usr/bin/python3 
#ln -sf /opt/conda/bin/pip /usr/bin/pip3 
#ln -sf /opt/conda/envs/python2/bin/python2 /usr/bin/python22 
#ln -sf /opt/conda/envs/python2/bin/pip /usr/bin/pip2 
#ln -s /opt/conda/envs/R/bin/R /usr/bin/R
#ln -s /opt/conda/envs/R/bin/Rscript /usr/bin/Rscript
#
#export PATH="/opt/conda/envs/python2/bin:/home/jovyan/libs:/home/jovyan/libs/icommands":$PATH
#export PYTHONPATH="/home/jovyan/work/notebooks:/home/jovyan/libs":$PYTHONPATH
#export DOCUMENTS="/home/jovyan/work/notebooks/documents"
#export DATA="/home/jovyan/work/notebooks/data"
#export HOME="/home/jovyan"
#export ECOHYDROLIB_CFG="/home/jovyan/.ecohydro.cfg"
#export LD_LIBRARY_PATH="/usr/lib/grass64/lib:$LD_LIBRARY_PATH"
#export NOTEBOOK_HOME="/home/jovyan/work/notebooks"
#export R_LIBS_SITE="/home/jovyan/.userRLib"
#export IRODS_PLUGINS_HOME="/home/jovyan/libs/icommands/plugins/"
#export IRODS_ENVIRONMENT_FILE="/home/jovyan/work/notebooks/data/.irods/irods_environment.json"
#export IRODS_AUTHENTICATION_FILE="/home/jovyan/work/notebooks/data/.irods/.irodsA"
