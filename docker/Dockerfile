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


# install rhesyss library requirements
#RUN apt-get install -y build-essential git

# fetch juptyerhub-singleuser entrypoint
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser && \
    chmod 755 /usr/local/bin/jupyterhub-singleuser

ADD singleuser.sh /srv/singleuser/singleuser.sh

USER jovyan 

# setup base python 
#RUN conda install -y conda-build

# build rhesyss environment
#RUN conda create -yn rhesyss python=2.7 pip requests && conda clean -yilts

# get rhesyss
RUN git clone https://github.com/RHESSys/RHESSys_docker.git $HOME/rhesyss
RUN cd $HOME/rhesyss && git submodule init && git submodule update


#RUN conda create -yn test python=3 pip requests && conda clean -yilts

# smoke test that it's importable at least
RUN sh /srv/singleuser/singleuser.sh -h
CMD ["sh", "/srv/singleuser/singleuser.sh"]


