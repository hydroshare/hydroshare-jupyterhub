#!/bin/bash
set -x
set -e



####################################################
#       INSTALL ECOHYDROLIB/RHESSysWorkflows       #
####################################################

#/opt/conda/envs/python2/bin/pip install --no-cache-dir \
#  git+https://github.com/leonard-psu/EcohydroLib.git \
#  git+https://github.com/leonard-psu/RHESSysWorkflows.git

# Install EcoHydroLib dependencies
conda install -y -n python2 \
pyproj \
numpy \
"owslib>=0.8.12" \
oset \
httplib2 \
shapely \
requests \
"hs_restclient>=1.1.0" \
clint
conda clean --all -y
# Install EcoHydroLib
/opt/conda/envs/python2/bin/pip install --no-cache-dir \
  git+https://github.com/leonard-psu/EcohydroLib.git

# Install RHESSysWorkflows dependencies
conda install -y -n python2 \
"numpy>=1.7" \
"matplotlib>=1.1" \
pandas \
scipy \
patsy \
statsmodels \
requests
conda clean --all -y
# Install RHESSysWorkflows 
/opt/conda/envs/python2/bin/pip install --no-cache-dir \
  git+https://github.com/leonard-psu/RHESSysWorkflows.git

#/opt/conda/envs/python2/bin/pip install --no-cache-dir EcohydroLib
#/opt/conda/envs/python2/bin/pip install --no-cache-dir  RHESSysWorkflows

# load the rhessys configuration file and modify for the current user
sed -i -e 's|^ETC.*|ETC = /home/jovyan/libs/RHESSysWorkflows/etc|g' /home/jovyan/.ecohydro.cfg 
sed -i -e 's|^MODULE_PATH.*|MODULE_PATH = /home/jovyan/work/notebooks/.grass6/addons|g' /home/jovyan/.ecohydro.cfg
sed -i -e 's|^MODULE_ETC.*|MODULE_ETC = /home/jovyan/libs/RHESSysWorkflows/etc/r.soils.texture|g' /home/jovyan/.ecohydro.cfg


