#!/bin/bash
set -x
set -e

# update anaconda
conda update -n base conda

## define variable shortcuts for conda env installations
#PIP3=/opt/conda/bin/pip
#PIP2=/opt/conda/envs/python2/bin/pip


# set anaconda channels
conda config --add channels conda-forge 
conda config --add channels landlab 
conda config --add channels odm2

###################################
#   INSTALL PYTHON 3 LIBRARIES    #
###################################


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
python-wget \
ipykernel 
 
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

#/opt/conda/bin/pip install --no-cache-dir \
#   hs_restclient \
#   wget \
#   git+https://github.com/cybergis/jupyterlib.git 


###################################
#   INSTALL PYTHON 2 LIBRARIES    #
###################################

conda install -y -n python2 \
    "pandas=0.21.0" \
    gdal \
    ipykernel \
    ulmo \
    celery \
    geopandas \
    graphviz  \
    "statsmodels=0.8.0" \
    "odm2api=0.6.0.a0" \
    "landlab=1.4.0" \
    ogh \
    basemap-data-hires \
    bsddb \
    python-wget

##basemap \

# install hs_restclient dependencies
conda install -y -n python2 \
requests \
requests-toolbelt \
requests-oauthlib 
# install hs_restclient
/opt/conda/envs/python2/bin/pip install --no-cache-dir hs_restclient 

# install sciunit2 dependencies
conda install -y -n python2 \
 backports.tempfile \
 backports.weakref \
 configobj \
 contextlib2 \
 humanfriendly \
 monotonic \
 poster \
 tqdm \
 tzlocal
# install sciunit2
/opt/conda/envs/python2/bin/pip install --no-cache-dir sciunit2
sciunit post-install 

# install jupyterlib dependencies
conda install -y -n python2 \
 ipywidgets \
 ipython \
 paramiko
# install jupyterlib
/opt/conda/envs/python2/bin/pip install --no-cache-dir git+https://github.com/cybergis/jupyterlib.git 

# install pyemu uncertainty analysis library (pure python so using pip)
/opt/conda/envs/python2/bin/pip install --no-cache-dir pyemu 

# register the python 2.7 kernel
python -m ipykernel install \
    --user \
    --name "python2" \
    --display-name "Python 2.7" 

#/opt/conda/envs/python2/bin/python \
# && pip install --no-cache-dir \
#    hs_restclient \
##    wget==3.2 \
##    git+https://github.com/cybergis/jupyterlib.git 
#    sciunit2 \
#sciunit post-install 
#

####################################
##      INSTALL NBExtensions       #
####################################
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
#/opt/conda/bin/pip install --no-cache-dir git+https://github.com/Castronova/jupyter_contrib_nbextensions.git
jupyter contrib nbextension install --user 
jupyter nbextension enable recursivedelete/main --user --section=tree 
jupyter nbextensions_configurator disable --user 
chown -R jovyan:users /home/jovyan/.jupyter


####################
#      CLEAN       #
####################

conda clean --all

