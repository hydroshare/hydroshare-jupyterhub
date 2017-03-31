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

RUN echo "after apt-get ...." >> /tmp/disk_usage
RUN date >> /tmp/disk_usage
RUN df -h >> /tmp/disk_usage

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

# create directories
RUN mkdir /home/jovyan/libs && chown -R jovyan:users /home/jovyan/libs
RUN mkdir /home/jovyan/work/notebooks && chown -R jovyan:users /home/jovyan/work/notebooks

# fetch juptyerhub-singleuser entrypoint
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser && \
    chmod 755 /usr/local/bin/jupyterhub-singleuser
ADD singleuser.sh /srv/singleuser/singleuser.sh

# link conda python2 (used by jupyterhub) to python22
RUN ln -s /opt/conda/envs/python2/bin/python2 /usr/bin/python22

# fetch the ecohydro config file
ADD https://raw.github.com/selimnairb/RHESSysWorkflows/master/docs/config/ecohydro-Linux.cfg /home/jovyan/.ecohydro.cfg
RUN chown jovyan:users /home/jovyan/.ecohydro.cfg

#########################
# SWITCH TO JOVYAN USER #
#########################
USER jovyan 

# TAUDEM v5.3.7 - build and install taudem (must happen before rhesyss b/c of gdal conflicts)
RUN git clone https://github.com/dtarb/TauDEM.git /home/jovyan/libs/TauDEM
RUN cd /home/jovyan/libs/TauDEM && git checkout tags/v5.3.7
RUN cd /home/jovyan/libs/TauDEM/src && make

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

RUN git clone -b master https://github.com/hydroshare/hs_restclient.git /home/jovyan/libs/hs_restclient
RUN /bin/bash -c "source /opt/conda/bin/activate root && cd /home/jovyan/libs/hs_restclient && python setup.py install "

# Python 2
RUN /bin/bash -c "source /opt/conda/bin/activate python2 && pip install --upgrade pip && pip install wget "

RUN conda install -y -n python2 \
gdal \
basemap \
landlab -c landlab 

# install ecohydrolib
RUN git clone https://github.com/leonard-psu/EcohydroLib.git /home/jovyan/libs/EcohydroLib
RUN /bin/bash -c "source /opt/conda/bin/activate python2  \
&& cd ../libs/EcohydroLib \
&& python setup.py install "

# install RHESSysWorkflows
RUN git clone https://github.com/leonard-psu/RHESSysWorkflows.git /home/jovyan/libs/RHESSysWorkflows
RUN /bin/bash -c "source /opt/conda/bin/activate python2 \
&& cd ../libs/RHESSysWorkflows \
&& python setup.py install"

# install odm2api
RUN conda install -y -n python2 -c odm2 odm2api

# load the rhessys configuration file and modify for the current user
RUN sed -i -e 's|^ETC.*|ETC = /home/jovyan/libs/RHESSysWorkflows/etc|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|^MODULE_PATH.*|MODULE_PATH = /home/jovyan/work/notebooks/.grass6/addons|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|^MODULE_ETC.*|MODULE_ETC = /home/jovyan/libs/RHESSysWorkflows/etc/r.soils.texture|g' /home/jovyan/.ecohydro.cfg

# prepare grass environment
ADD ./rhessys_wf.py /home/jovyan/libs/rhessys_wf.py
ADD ./run.py /home/jovyan/libs/run.py

######################
# SET PATH VARIABLES #
######################

ENV PATH=/opt/conda/envs/python2/bin:/home/jovyan/libs/TauDEM:$PATH PYTHONPATH=/home/jovyan/work/notebooks:$PYTHONPATH DOCUMENTS=/home/jovyan/work/notebooks/documents DATA=/home/jovyan/work/notebooks/data HOME=/home/jovyan/work/notebooks ECOHYDROLIB_CFG=/home/jovyan/.ecohydro.cfg LD_LIBRARY_PATH=/usr/lib/grass64/lib
ENV PYTHONPATH=/home/jovyan/work/notebooks:$PYTHONPATH


