FROM jupyter/scipy-notebook
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

EXPOSE 8888

USER jovyan

ADD singleuser.sh /srv/singleuser/singleuser.sh
ADD ecohydro-Linux.cfg /home/jovyan/.ecohydro.cfg
ADD rhessys_wf.py /home/jovyan/libs/rhessys_wf.py
ADD run.py /home/jovyan/libs/run.py
ADD dakota_template.cmake /home/jovyan/libs/dakota-6.5.0.src/build/BuildDakota.cmake
ADD icommands.sh /home/jovyan/libs/icommands.sh 

ENV PATH="/opt/conda/envs/python2/bin:/home/jovyan/libs:/home/jovyan/libs/icommands":$PATH \
    PYTHONPATH="/home/jovyan/work/notebooks:/home/jovyan/libs":$PYTHONPATH \
    DOCUMENTS="/home/jovyan/work/notebooks/documents" \
    DATA="/home/jovyan/work/notebooks/data" \
    HOME="/home/jovyan/work" \
    ECOHYDROLIB_CFG="/home/jovyan/.ecohydro.cfg" \
    LD_LIBRARY_PATH="/usr/lib/grass72/lib:$LD_LIBRARY_PATH" \
    NOTEBOOK_HOME="/home/jovyan/work/notebooks" \
    R_LIBS_SITE="/home/jovyan/.userRLib" \
    IRODS_PLUGINS_HOME="/home/jovyan/libs/icommands/plugins/" \
    IRODS_ENVIRONMENT_FILE="/home/jovyan/work/notebooks/data/.irods/irods_environment.json" \
    IRODS_AUTHENTICATION_FILE="/home/jovyan/work/notebooks/data/.irods/.irodsA" 

#ENV HOME=/home/jovyan/work
WORKDIR $HOME

USER root
ADD install-base.sh /home/install-base.sh
RUN sh /home/install-base.sh

ADD install-mpi.sh /home/install-mpi.sh
RUN sh /home/install-mpi.sh

ADD install-gnu.sh /home/install-gnu.sh
RUN sh /home/install-gnu.sh

ADD install-taudem.sh /home/install-taudem.sh
RUN sh /home/install-taudem.sh

USER jovyan
  ADD install-condaenvs.sh /home/install-condaenvs.sh
  RUN sh /home/install-condaenvs.sh
USER root

RUN ln -sf /opt/conda/envs/python2/bin/python2 /usr/bin/python22 &&\
ln -sf /opt/conda/envs/python2/bin/pip /usr/bin/pip2 &&\
ln -s /opt/conda/envs/R/bin/R /usr/bin/R &&\
ln -s /opt/conda/envs/R/bin/Rscript /usr/bin/Rscript

ADD install-irods.sh /home/install-irods.sh
RUN sh /home/install-irods.sh

USER jovyan

  ADD install-python3.sh /home/install-python3.sh
  RUN sh /home/install-python3.sh
  
  ADD install-python2.sh /home/install-python2.sh
  RUN sh /home/install-python2.sh

  ADD install-r.sh /home/install-r.sh
  RUN sh /home/install-r.sh
  
  ADD install-rhessys.sh /home/install-rhessys.sh
  RUN sh /home/install-rhessys.sh
USER root

ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH" \
    CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python3.5m"

ADD install-boost.sh /home/install-boost.sh
RUN sh /home/install-boost.sh

ADD install-dakota.sh /home/install-dakota.sh
RUN sh /home/install-dakota.sh

ADD install-dhsvm.sh /home/install-dhsvm.sh
RUN sh /home/install-dhsvm.sh

ADD install-modflow.sh /home/install-modflow.sh
ADD modflow.6.0.2-makefile-ubuntu /tmp/makefile
RUN sh /home/install-modflow.sh

ADD install-nbextensions.sh /home/install-nbextensions.sh
RUN sh /home/install-nbextensions.sh

ADD modify-permissions.sh /home/modify-permissions.sh
RUN sh /home/modify-permissions.sh

ADD install-cleanup.sh /home/install-cleanup.sh
RUN sh /home/install-cleanup.sh

#USER root
RUN /opt/conda/envs/python2/bin/python -m ipykernel install \
    --prefix=/usr/local \
    --name "python2" \
    --display-name "Python 2.7"

RUN Rscript -e "IRkernel::installspec(name = 'ir34', displayname = 'R 3.4', user=FALSE)"

RUN apt-get update \
&& apt-get install -y tzdata \
&& dpkg-reconfigure tzdata

# create the cache directory so that user installations won't fail the first time
USER jovyan
RUN mkdir -p /opt/conda/pkgs/cache

RUN conda install -n root -y holoviews rasterio xlsxwriter

# install modflow dev for SI
RUN cd /tmp \
&& /bin/bash -c "wget http://public.cuahsi.org/jupyter/mf6.0.2.32.zip" \
&& unzip mf6.0.2.32.zip \
&& cd make \
&& make 
USER root
RUN mv /tmp/make/mf6.0.2.32 /usr/local/bin
RUN rm -rf /tmp/*
USER jovyan


## install jupyter_contrib_nbextensions
#RUN jupyter contrib nbextension install --system \
#&& jupyter nbextension enable recursivedelete/main --system --section=tree \
#&& jupyter nbextensions_configurator disable --system
