FROM castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################
RUN pip install mock
RUN pip3 install mock
###################################################
## End - JupyterHub Development Image Additions ###
###################################################

CMD ["sh", "/srv/singleuser/singleuser.sh"]



