FROM castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################

# install ecohydrolib
RUN git clone https://github.com/leonard-psu/EcohydroLib.git ../libs/EcohydroLib
RUN /bin/bash -c "source /opt/conda/bin/activate python2  \
&& cd ../libs/EcohydroLib \
&& python setup.py install "

# install RHESSysWorkflows
RUN git clone https://github.com/leonard-psu/RHESSysWorkflows.git ../libs/RHESSysWorkflows
RUN /bin/bash -c "source /opt/conda/bin/activate python2 \
&& cd ../libs/RHESSysWorkflows \
&& python setup.py install"

# install odm2api
RUN conda install -y -n python2 -c odm2 odm2api

####################################################
### End - JupyterHub Development Image Additions ###
####################################################

ENV PYTHONPATH=/home/jovyan/work/notebooks:$PYTHONPATH

CMD ["sh", "/srv/singleuser/singleuser.sh"]



