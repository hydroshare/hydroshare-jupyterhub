FROM castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################


###################################################
## End - JupyterHub Development Image Additions ###
###################################################


# prepare grass environment
ADD rhessys_wf.py /home/jovyan/libs/rhessys_wf.py
ADD run.py /home/jovyan/libs/run.py

ENV PYTHONPATH=/home/jovyan/work/notebooks:$PYTHONPATH

CMD ["sh", "/srv/singleuser/singleuser.sh"]



