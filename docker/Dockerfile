FROM castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################

# install taudem (must happen before rhesyss b/c of gdal conflicts)
RUN git clone https://github.com/dtarb/TauDEM.git /home/jovyan/libs/TauDEM && \
cd /home/jovyan/libs/TauDEM/src && make

# install ecohydrolib
RUN git clone https://github.com/leonard-psu/EcohydroLib.git ../libs/EcohydroLib
RUN /bin/bash -c "source /opt/conda/bin/activate python2  \
&& cd ../libs/EcohydroLib \
&& python setup.py install "

# fetch the ecohydro config file
ADD https://raw.github.com/selimnairb/RHESSysWorkflows/master/docs/config/ecohydro-Linux.cfg /home/jovyan/.ecohydro.cfg
RUN chown jovyan:users /home/jovyan/.ecohydro.cfg

# install RHESSysWorkflows
RUN git clone https://github.com/leonard-psu/RHESSysWorkflows.git ../libs/RHESSysWorkflows
RUN /bin/bash -c "source /opt/conda/bin/activate python2 \
&& cd ../libs/RHESSysWorkflows \
&& python setup.py install"

# install odm2api
RUN conda install -y -n python2 -c odm2 odm2api


# load the rhessys configuration file and modify for the current user
RUN sed -i -e 's|^ETC.*|ETC = /home/jovyan/libs/RHESSysWorkflows/etc|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|^MODULE_PATH.*|MODULE_PATH = /home/jovyan/work/notebooks/.grass6/addons|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|^MODULE_ETC.*|MODULE_ETC = /home/jovyan/libs/RHESSysWorkflows/etc/r.soils.texture|g' /home/jovyan/.ecohydro.cfg

####################################################
### End - JupyterHub Development Image Additions ###
####################################################


## prepare grass environment
#ADD rhessys_wf.py /home/jovyan/libs/rhessys_wf.py
#ADD run.py /home/jovyan/libs/run.py

ENV PYTHONPATH=/home/jovyan/work/notebooks:$PYTHONPATH

CMD ["sh", "/srv/singleuser/singleuser.sh"]



