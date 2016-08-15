# Build as jupyterhub/singleuser
# Run with the DockerSpawner in JupyterHub

# Minimal Jupyter Notebook Stack comes with: 
# Jupyter Notebook 4.2.x
# Conda Python 3.x
# No preinstalled scientific computing packages
# Unprivileged user jovyan (uid=1000, configurable, see options) in group users (gid=100) with ownership over /home/jovyan and /opt/conda
# tini as the container entrypoint and start-notebook.sh as the default command
# A start-singleuser.sh script for use as an alternate command that runs a single-user instance of the Notebook server, as required by JupyterHub
# Options for HTTPS, password auth, and passwordless sudo


FROM jupyter/scipy-notebook

MAINTAINER Tony Castronova <tony.castronova@usu.edu>

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

RUN apt-get install -y libgeos-dev mpic++ libproj-dev    

# install irods fuse
RUN apt-get install -y fuse libfuse2 libfuse-dev
RUN wget -q ftp://ftp.renci.org/pub/irods/releases/4.1.8/ubuntu12/irods-icommands-4.1.8-ubuntu12-x86_64.deb -O /tmp/irods-icommands-4.1.8-ubuntu12-x86_64.deb
RUN dpkg -i /tmp/irods-icommands-4.1.8-ubuntu12-x86_64.deb
RUN groupadd fuse && usermod -aG fuse jovyan
RUN chmod g+rw /dev/fuse && chgrp fuse /dev/fuse

# install rhessys workflows
RUN apt-get install -y build-essential git subversion p7zip-full python python-dev python-pip python-scipy libxml2-dev libxslt-dev libgdal-dev libgdal-doc gdal-bin python-gdal grass grass-dev libbsd-dev vlc 
#ffmpeg

###############################
# SETUP JUPYTERHUB ENTRYPOINT #
###############################

# fetch juptyerhub-singleuser entrypoint
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser && \
    chmod 755 /usr/local/bin/jupyterhub-singleuser

ADD singleuser.sh /srv/singleuser/singleuser.sh

##################
# PREPARE TAUDEM #
##################

# create build/lib space for taudem and rhesyss
RUN mkdir ../libs && chown -R jovyan:users ../libs

# install taudem (must happend before rhesyss b/c of gdal conflicts)
RUN git clone https://github.com/dtarb/TauDEM.git ../libs/TauDEM && \
cd ../libs/TauDEM/src && make 


#ADD taudem_env /taudem_env
#RUN /bin/bash -c "source /taudem_env" && \

# link conda python2 (used by jupyterhub) to python22
RUN ln -s /opt/conda/envs/python2/bin/python2 /usr/bin/python22

# prepare grass
COPY create_grass_loc.sh /home/jovyan/libs/create_grass_loc.sh
RUN chown jovyan:users /home/jovyan/libs/create_grass_loc.sh && \
chmod +x /home/jovyan/libs/create_grass_loc.sh

RUN /bin/sh /home/jovyan/libs/create_grass_loc.sh jupyter

#sh /home/jovyan/libs/create_grass_loc.sh jupyter

# load the rhessys configuration file
ADD https://raw.github.com/selimnairb/RHESSysWorkflows/master/docs/config/ecohydro-Linux.cfg /home/jovyan/.ecohydro.cfg  
RUN chown jovyan:users /home/jovyan/.ecohydro.cfg  && \
sed -i -e 's|.*ETC.*|ETC = /home/jovyan/libs/RHESSysWorkflows/etc|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|.*MODULE_PATHC.*|MODULE_PATH = /home/jovyan/libs/notebooks/.grass6/addons|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|.*MODULE_PATHC.*|MODULE_ETC = /home/jovyan/libs/RHESSysWorkflows/etc/r.soils.texture|g' /home/jovyan/.ecohydro.cfg

#RUN sed -i -e 's/<myusername>/jovyan/g' /home/jovyan/.ecohydro.cfg  

#########################
# SWITCH TO JOVYAN USER #
#########################
USER jovyan 

# prepare python environments
RUN pip install --upgrade pip

# install ecohydrolib
RUN git clone https://github.com/leonard-psu/EcohydroLib.git ../libs/EcohydroLib && \
cd ../libs/EcohydroLib && \
python22 setup.py install

# install RHESSysWorkflows
RUN git clone https://github.com/selimnairb/RHESSysWorkflows.git ../libs/RHESSysWorkflows && \
cd ../libs/RHESSysWorkflows && \
python22 setup.py install

# install RHESSys
RUN git clone https://github.com/RHESSys/RHESSys.git ../libs/RHESSys && \
cd ../libs/RHESSys && \
GISBASE=/usr/lib/grass64 make 2>&1 | grep warning | wc -l

# install EcoHydroLib
#RUN cd ../libs && \
#git clone https://github.com/leonard-psu/EcohydroLib.git ../libs/EcohydroLib && \
#cd ../libs/EcohydroLib && \
#python22 setup.py install

# install RHESSys Workflows 
#RUN pip2 install rhessysworkflows


###############################
# PREPARE PYTHON ENVIRONMENTS #
###############################

# Python 3
RUN conda install -y -n root \
gdal \
basemap \
landlab -c landlab

#RUN pip3 install \ 
#hs_restclient
RUN pip3 install git+https://github.com/hydroshare/hs_restclient.git@2_and_3

# Python 2
# install gdal into python2 conda env
RUN conda install -y -n python2 \
gdal \
basemap \
landlab -c landlab

RUN /bin/bash -c "source /opt/conda/bin/activate python2" &&  \
pip install hs_restclient

######################
# SET PATH VARIABLES #
######################

# add taudem binaries to system path
ENV PATH /home/jovyan/libs/TauDEM:$PATH

# set rhesyss and ecohydrolib environment variables
ENV PATH=/opt/conda/envs/python2/bin:$PATH PYTHONPATH=/home/jovyan/work/notebooks/utilities:$PYTHONPATH DOCUMENTS=/home/jovyan/work/notebooks/documents DATA=/home/jovyan/work/notebooks/data HOME=/home/jovyan/work/notebooks ECOHYDROLIB_CFG=/home/jovyan/.ecohydro.cfg LD_LIBRARY_PATH=/usr/lib/grass64/lib

# get rhesyss
#RUN git clone https://github.com/RHESSys/RHESSys_docker.git $HOME/rhesyss
#RUN cd $HOME/rhesyss && git submodule init && git submodule update


# smoke test that it's importable at least
#RUN sh /srv/singleuser/singleuser.sh -h
CMD ["sh", "/srv/singleuser/singleuser.sh"]


ADD ./create_grass_loc.sh /home/jovyan/libs/create_grass_loc.sh
