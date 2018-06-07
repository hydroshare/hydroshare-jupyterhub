#!/bin/bash
set -x
set -e

## update anaconda
conda update -n base conda

## set anaconda channels
conda config --add channels conda-forge 
conda config --add channels landlab 
conda config --add channels odm2


conda install -y -n root \
gdal \
"jupyterhub=0.8.1" \
"landlab=1.4.0" \
ogh \
basemap-data-hires \
ulmo \
celery \
geopandas \
graphviz \
python-wget
 
##  basemap \


# install hs_restclient dependencies
conda install -y -n root \
requests \
requests-toolbelt \
requests-oauthlib 
# install hs_restclient
#/opt/conda/bin/pip install --no-cache-dir hs_restclient 
/opt/conda/bin/pip install --no-cache-dir hs_restclient 

# install jupyterlib dependencies
conda install -y -n root \
 ipywidgets \
 ipython \
 paramiko
# install jupyterlib
/opt/conda/bin/pip install --no-cache-dir git+https://github.com/cybergis/jupyterlib.git 

# install pyemu uncertainty analysis library (pure python so using pip)
/opt/conda/bin/pip install --no-cache-dir pyemu 


# NBExtensions       
# install jupyter_contrib_nbextensions dependencies
conda install -y -n root \
 "jupyter_contrib_core>=0.3.3" \
 jupyter_core \
 "notebook>=4.0" \
 pyyaml \
 tornado \
 traitlets

# install jupyter_contrib_nbextensions
/opt/conda/bin/pip install --no-cache-dir git+https://github.com/Castronova/jupyter_contrib_nbextensions.git
jupyter contrib nbextension install --system
jupyter nbextension enable recursivedelete/main --system --section=tree 
jupyter nbextensions_configurator disable --system
#chown -R jovyan:users /home/jovyan/.jupyter
