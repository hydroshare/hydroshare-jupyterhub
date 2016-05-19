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

MAINTAINER Project Jupyter <jupyter@googlegroups.com>

EXPOSE 8888


USER root

# update package lists
RUN apt-get update && apt-get install -y \
    libgeos-dev  # RHESYSS dependency

# fetch juptyerhub-singleuser entrypoint
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser && \
    chmod 755 /usr/local/bin/jupyterhub-singleuser

ADD singleuser.sh /srv/singleuser/singleuser.sh

RUN ln -s /opt/conda/envs/python2/bin/python2 /usr/bin/python22

USER jovyan 

# setup base python 
#RUN conda install -y conda-build

# prepare python environments
RUN pip install --upgrade pip

# INSTALL RHESYSS LIBS
RUN cd .. && \
mkdir tmp && \
cd tmp && \
git clone https://github.com/selimnairb/EcohydroLib.git && \
cd EcohydroLib && \
python22 setup.py install

RUN conda install -y -n python2 gdal 

env PATH /opt/conda/envs/python2/bin:$PATH
#RUN export PATH=$PATH:/opt/conda/envs/python2/bin


#  /bin/bash -c "source /opt/conda/bin/activate python2" && \
#    /bin/bash -c "python setup.py install"



# get rhesyss
#RUN git clone https://github.com/RHESSys/RHESSys_docker.git $HOME/rhesyss
#RUN cd $HOME/rhesyss && git submodule init && git submodule update


# smoke test that it's importable at least
#RUN sh /srv/singleuser/singleuser.sh -h
CMD ["sh", "/srv/singleuser/singleuser.sh"]


