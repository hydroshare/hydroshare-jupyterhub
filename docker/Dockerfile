#FROM castrona/hydroshare-jupyterhub:latest
FROM docker.io/castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################

USER jovyan
RUN pip install mock
RUN pip3 install mock
RUN conda update -n root --all -y
RUN conda update -n python2 --all -y

###################################################
## End - JupyterHub Development Image Additions ###
###################################################

CMD ["sh", "/srv/singleuser/singleuser.sh"]



