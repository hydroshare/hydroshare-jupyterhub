FROM castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################


USER jovyan
RUN conda update -n root --all -y
RUN conda update -n python2 --all -y
RUN pip3 install ulmo 

# install nbextensions
RUN git clone https://github.com/Castronova/jupyter_contrib_nbextensions.git /home/jovyan/libs/jupyter_contrib_nbextensions
USER root
RUN pip3 install -e /home/jovyan/libs/jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --system
RUN jupyter nbextensions_configurator disable --user
RUN jupyter nbextension enable recursivedelete/main
RUN chown -R jovyan:users /home/jovyan/work/notebooks

###################################################
## End - JupyterHub Development Image Additions ###
###################################################
USER root
RUN conda clean --all -y
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
USER jovyan
CMD ["sh", "/srv/singleuser/singleuser.sh"]



