FROM jupyter/scipy-notebook

MAINTAINER Tony Castronova <acastronova@cuahsi.org>

EXPOSE 8888

USER root

############################
# INSTALL SYSTEM LIBRARIES #
############################

# libgeos-dev  RHESYSS dependency
# mpic++       TAUDEM dependency
# libgdal-dev  TAUDEM dependency
# libproj-dev  TAUDEM dependency
RUN apt-get clean && apt-get update --fix-missing

RUN apt-get update && apt-get install --fix-missing -y \ 
    libgeos-dev \
    mpic++ \
    libproj-dev \   
    libfuse2 \
    libfuse-dev \
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
    libgdal-doc \
    gdal-bin \
    python-gdal \
    grass \
    grass-dev \
    libbsd-dev \
    vlc  \
&& rm -rf /var/lib/apt/lists/*

# install irods 4.1.8 packages
RUN wget -q ftp://ftp.renci.org/pub/irods/releases/4.1.8/ubuntu12/irods-icommands-4.1.8-ubuntu12-x86_64.deb -O /tmp/irods-icommands-4.1.8-ubuntu12-x86_64.deb
RUN dpkg -i /tmp/irods-icommands-4.1.8-ubuntu12-x86_64.deb
RUN groupadd fuse && usermod -aG fuse jovyan
RUN chmod g+rw /dev/fuse && chgrp fuse /dev/fuse

# create directories
RUN mkdir /home/jovyan/libs && chown -R jovyan:users /home/jovyan/libs
RUN mkdir /home/jovyan/work/notebooks && chown -R jovyan:users /home/jovyan/work/notebooks

# fetch juptyerhub-singleuser entrypoint
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser && \
    chmod 755 /usr/local/bin/jupyterhub-singleuser
ADD singleuser.sh /srv/singleuser/singleuser.sh

# link conda python2 (used by jupyterhub) to python22
RUN ln -s /opt/conda/envs/python2/bin/python2 /usr/bin/python22

#########################
# SWITCH TO JOVYAN USER #
#########################
USER jovyan 

# prepare python environments
RUN pip install --upgrade pip

###############################
# PREPARE PYTHON ENVIRONMENTS #
###############################

# Python 3
RUN conda install -y -n root \
gdal \
basemap \
landlab -c landlab

RUN git clone -b 2_and_3 https://github.com/hydroshare/hs_restclient.git ../libs/hs_restclient
RUN /bin/bash -c "source /opt/conda/bin/activate root \
&& cd ../libs/hs_restclient \
&& python setup.py install "

# Python 2
RUN /bin/bash -c "source /opt/conda/bin/activate python2 \
&& pip install --upgrade pip \
&& pip install wget "

RUN conda install -y -n python2 \
gdal \
basemap \
landlab -c landlab 

######################
# SET PATH VARIABLES #
######################

ENV PATH=/opt/conda/envs/python2/bin:/home/jovyan/libs/TauDEM:$PATH PYTHONPATH=/home/jovyan/work/notebooks:$PYTHONPATH DOCUMENTS=/home/jovyan/work/notebooks/documents DATA=/home/jovyan/work/notebooks/data HOME=/home/jovyan/work/notebooks ECOHYDROLIB_CFG=/home/jovyan/.ecohydro.cfg LD_LIBRARY_PATH=/usr/lib/grass64/lib



