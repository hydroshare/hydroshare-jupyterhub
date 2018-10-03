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
"ogh=0.1.11" \
basemap-data-hires \
ulmo \
celery \
geopandas \
graphviz \
python-wget
 
# install hs_restclient
conda install -y -n root \
requests \
requests-toolbelt \
requests-oauthlib 
/opt/conda/bin/pip install --no-cache-dir hs_restclient 

# install jupyterlib
conda install -y -n root \
 ipywidgets \
 ipython \
 paramiko
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

# install pysumma (pure python)
/opt/conda/bin/pip install --no-cache-dir git+https://github.com/uva-hydroinformatics/pysumma/tree/develop@e273369ecae6d0209716c35cde20ffde3877332c

# cleanup
conda clean -all -y

