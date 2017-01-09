#FROM castrona/hydroshare-jupyterhub:latest
FROM docker.io/castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################
USER root
ADD tests /home/jovyan/tests
RUN chown -R jovyan:users /home/jovyan/tests

USER jovyan
RUN pip install mock
RUN pip3 install mock

###################################################
## End - JupyterHub Development Image Additions ###
###################################################

CMD ["sh", "/srv/singleuser/singleuser.sh"]



