#!/bin/bash
set -x
set -e


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
    "ogh=0.1.11" \
    basemap-data-hires \
    bsddb \
    python-wget


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
