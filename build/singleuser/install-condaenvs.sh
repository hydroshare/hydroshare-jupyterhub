#!/bin/bash
set -x
set -e



## upgrade andaconda
conda update conda -y 
#conda clean --all -y

# create anaconda environments as jovyan so that users can install packages
#sudo -u jovyan conda create -y -n python2 python=2
#sudo -u jovyan conda create -y -n R
#sudo -u jovyan conda clean --all -y
conda create -y -n python2 python=2
conda create -y -n R
conda clean --all -y

# fix conda directory permissions
#chown -R jovyan:users /opt/conda

# link environments to bin
#ln -sf /opt/conda/bin/python /usr/bin/python3 
#ln -sf /opt/conda/bin/pip /usr/bin/pip3 
#ln -sf /opt/conda/envs/python2/bin/python2 /usr/bin/python22
#ln -sf /opt/conda/envs/python2/bin/pip /usr/bin/pip2
#ln -s /opt/conda/envs/R/bin/R /usr/bin/R
#ln -s /opt/conda/envs/R/bin/Rscript /usr/bin/Rscript
