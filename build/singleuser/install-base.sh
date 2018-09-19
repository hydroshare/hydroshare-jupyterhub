#!/bin/bash
set -x
set -e

############################
# ROOT - INSTALL LIBRARIES #
############################
apt update
apt-get install -y software-properties-common
add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
add-apt-repository -y ppa:ubuntu-toolchain-r/test

apt-get update && apt-get install --fix-missing -y --no-install-recommends \
  gcc-7 \
  g++-7 \
  autoconf \
  automake \
  libtool \
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
  gfortran \
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


###################################
#          SYSTEM PREP            #
###################################

# create directories
chown -R jovyan:users /home/jovyan/libs 
mkdir /home/jovyan/work/notebooks 
chown -R jovyan:users /home/jovyan/work/notebooks

# fetch juptyerhub-singleuser entrypoint
chmod 755 /srv/singleuser/singleuser.sh

# fetch the ecohydro config file
chown jovyan:users /home/jovyan/.ecohydro.cfg

