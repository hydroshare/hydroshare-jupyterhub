FROM jupyter/scipy-notebook
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

EXPOSE 8888

USER root

############################
# ROOT - INSTALL LIBRARIES #
############################

RUN apt-get clean && apt-get update --fix-missing

RUN apt-get install --fix-missing -y \ 
    libgeos-dev \
    mpic++ \
    libproj-dev \   
    libfuse2 \
    libfuse-dev \
    build-essential \ 
    git \ 
    subversion \
    p7zip-full \
    python \
    python-dev \
    python-pip \
    python-scipy \
    libxml2-dev \
    libxslt-dev \
    libgdal-dev \  
    libgdal-doc \
    gdal-bin \
    python-gdal \
    grass \
    grass-dev \
    libbsd-dev \
    vlc  \
    libx11-dev \
&& rm -rf /var/lib/apt/lists/*

###################################
#          SYSTEM PREP            #
###################################

# upgrade andaconda
RUN conda update conda -y

# create directories
RUN mkdir /home/jovyan/libs && chown -R jovyan:users /home/jovyan/libs
RUN mkdir /home/jovyan/work/notebooks && chown -R jovyan:users /home/jovyan/work/notebooks

# fetch juptyerhub-singleuser entrypoint
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser && \
    chmod 755 /usr/local/bin/jupyterhub-singleuser
ADD singleuser.sh /srv/singleuser/singleuser.sh

# link conda python2 (used by jupyterhub) to python22
RUN ln -s /opt/conda/envs/python2/bin/python2 /usr/bin/python22

# fetch the ecohydro config file
ADD https://raw.github.com/selimnairb/RHESSysWorkflows/master/docs/config/ecohydro-Linux.cfg /home/jovyan/.ecohydro.cfg
RUN chown jovyan:users /home/jovyan/.ecohydro.cfg

# Prepare celery and add celery tasks
RUN mkdir /home/jovyan/libs/celeryworker
ADD docker/celery/celeryworker  /home/jovyan/libs/celeryworker/

USER jovyan

###################################
#          INSTALL TAUDEM         #
###################################

# TAUDEM v5.3.7 - build and install taudem (must happen before rhesyss b/c of gdal conflicts)
RUN git clone https://github.com/dtarb/TauDEM.git /home/jovyan/libs/TauDEM
RUN cd /home/jovyan/libs/TauDEM && git checkout tags/v5.3.7
RUN cd /home/jovyan/libs/TauDEM/src && make

###################################
#       INSTALL ECOHYDROLIB       #
###################################

RUN git clone https://github.com/leonard-psu/EcohydroLib.git /home/jovyan/libs/EcohydroLib
RUN /bin/bash -c "source /opt/conda/bin/activate python2  \
&& cd ../libs/EcohydroLib \
&& python setup.py install "

###################################
#     INSTALL RHESSysWorkflows    #
###################################

RUN git clone https://github.com/leonard-psu/RHESSysWorkflows.git /home/jovyan/libs/RHESSysWorkflows
RUN /bin/bash -c "source /opt/conda/bin/activate python2 \
&& cd ../libs/RHESSysWorkflows \
&& python setup.py install"

# load the rhessys configuration file and modify for the current user
RUN sed -i -e 's|^ETC.*|ETC = /home/jovyan/libs/RHESSysWorkflows/etc|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|^MODULE_PATH.*|MODULE_PATH = /home/jovyan/work/notebooks/.grass6/addons|g' /home/jovyan/.ecohydro.cfg &&\
sed -i -e 's|^MODULE_ETC.*|MODULE_ETC = /home/jovyan/libs/RHESSysWorkflows/etc/r.soils.texture|g' /home/jovyan/.ecohydro.cfg

# prepare grass environment
ADD ./rhessys_wf.py /home/jovyan/libs/rhessys_wf.py
ADD ./run.py /home/jovyan/libs/run.py

###################################
#     INSTALL BOOST AND DAKOTA    #
###################################

RUN wget -O /home/jovyan/libs/boost.tar.gz https://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.gz/download \
 && mkdir /home/jovyan/libs/boost \
 && tar xzfv /home/jovyan/libs/boost.tar.gz -C /home/jovyan/libs/boost --strip-components 1

  ###### BEGIN ROOT #######
  USER root
  RUN apt-get install -y libblas-dev liblapack-dev cmake \
   && cd /home/jovyan/libs/boost && ./bootstrap.sh --prefix=/usr/local \
   && echo "using mpi ;" >> /home/jovyan/libs/boost/tools/build/v2/user-config.jam \
   && cd /home/jovyan/libs/boost && ./b2 --with=all -j 4 install; exit 0 \
   && sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf' \
   && ldconfig
  USER jovyan
  ####### END ROOT ########

RUN wget https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.5-public.src.tar.gz -P /home/jovyan/libs \
 && tar xzf /home/jovyan/libs/dakota-6.5-public.src.tar.gz -C /home/jovyan/libs \
 && mkdir /home/jovyan/libs/dakota-6.5.0.src/build 
ADD docker/dakota_template.cmake /home/jovyan/libs/dakota-6.5.0.src/build/BuildDakota.cmake
RUN cd /home/jovyan/libs/dakota*.src/build \
 && cmake -C BuildDakota.cmake /home/jovyan/libs/dakota*.src

  ###### BEGIN ROOT #######
  USER root
  ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
  RUN cd /home/jovyan/libs/dakota*.src/build \
   && make clean \
   && make \
   && make install
  USER jovyan
  ####### END ROOT ########

###################################
#         INSTALL DHSVM           #
###################################

RUN git clone -b glacier https://github.com/pnnl/DHSVM-PNNL.git /home/jovyan/libs/DHSVM-PNNL
RUN sed -i '/# CC = gcc/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i '/# CFLAGS = -O3 -fexceptions/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i '/# BLAS = -lgoto -lfrtbegin -lg2c $(XERBLA) -lpthread/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/F77 = gfortran/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/CFLAGS = -O3 -fno-common -no-cpp-precomp -fexception/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/BLAS = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/LAPACK = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/DEFS =  -DHAVE_X11 -DHAVE_GLACIER/DEFS =  -DHAVE_X11/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode/makefile \
  && rm /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib/libcxsparse.a \
  && cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib && make \
  && cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode && make 

###################################
#      INSTALL NBExtensions       #
###################################

RUN git clone https://github.com/Castronova/jupyter_contrib_nbextensions.git /home/jovyan/libs/jupyter_contrib_nbextensions
RUN pip3 install -e /home/jovyan/libs/jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --system
RUN jupyter nbextension enable recursivedelete/main --user --section=tree
RUN jupyter nbextensions_configurator disable --user
RUN chown -R jovyan:users /home/jovyan/.jupyter

###################################
#   INSTALL PYTHON 3 LIBRARIES    #
###################################

# update environment
RUN pip3 install --upgrade pip
RUN conda update -n root --all -y

# Install Python 3 Modules
RUN conda install -y -n root \
  gdal \
  basemap \
  landlab -c landlab

RUN pip3 install \
  ulmo \
  wget \
  celery \ 
  geopandas \ 
  graphviz \
  hs_restclient

RUN pip3 install git+https://github.com/cybergis/jupyterlib.git 
# && pip3 install -e /home/jovyan/libs/hs_restclient --user


RUN git clone -b master https://github.com/hydroshare/hs_restclient.git /home/jovyan/libs/hs_restclient
#RUN cd /home/jovyan/libs/hs_restclient && git checkout tags/1.2.6

###################################
#   INSTALL PYTHON 2 LIBRARIES    #
###################################

# update environment
RUN pip install --upgrade pip
RUN conda update -n python2 --all -y

# Install Python 2 Modules
RUN pip install \ 
  ulmo \
  wget \
  celery \ 
  geopandas \ 
  graphviz \
  hs_restclient

RUN pip install git+https://github.com/cybergis/jupyterlib.git 
#  && pip install -e /home/jovyan/libs/hs_restclient --user

RUN conda install -y -n python2 \
  gdal \
  basemap \
  landlab -c landlab 

#RUN pip install ulmo
RUN conda install -y -n python2 -c odm2 odm2api

####################################
# USER JOVYAN - SET PATH VARIABLES #
####################################

ENV \
  PATH=/opt/conda/envs/python2/bin:/home/jovyan/libs/TauDEM:$PATH \
  PYTHONPATH=/home/jovyan/work/notebooks:$PYTHONPATH \
  DOCUMENTS=/home/jovyan/work/notebooks/documents \
  DATA=/home/jovyan/work/notebooks/data \
  HOME=/home/jovyan \
  ECOHYDROLIB_CFG=/home/jovyan/.ecohydro.cfg \
  LD_LIBRARY_PATH=/usr/lib/grass64/lib:$LD_LIBRARY_PATH \
  NOTEBOOK_HOME=/home/jovyan/work/notebooks \
  PATH=$PATH:/home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode \
  PATH=/home/jovyan/libs:$PATH \
  PYTHONPATH=/home/jovyan/libs:$PYTHONPATH \
  R_LIBS_SITE=/home/jovyan/.userRLib \ 
  PATH=/home/jovyan/libs/icommands:$PATH \
  IRODS_PLUGINS_HOME=/home/jovyan/libs/icommands/plugins/ \
  IRODS_ENVIRONMENT_FILE=/home/jovyan/work/notebooks/data/.irods/irods_environment.json \ 
  IRODS_AUTHENTICATION_FILE=/home/jovyan/work/notebooks/data/.irods/.irodsA

####################################
#          INSTALL R KERNEL        #
####################################

RUN mkdir /home/jovyan/.userRLib

RUN conda create -y -n R \
  && conda install -n R -c r \
  r-essentials \
  r-xml \
  r-rjsonio

#  ###### BEGIN ROOT #######
   USER root
    RUN ln -s /opt/conda/envs/R/bin/R /usr/bin/R
    RUN ln -s /opt/conda/envs/R/bin/Rscript /usr/bin/Rscript
   USER jovyan
#  ####### END ROOT ########

RUN echo "options(repos=structure(c(CRAN=\"http://archive.linux.duke.edu/cran\")))" >> /home/jovyan/.Rprofile \
  && Rscript -e "install.packages('devtools', repos='http://archive.linux.duke.edu/cran')" \
  && Rscript -e "IRkernel::installspec(name = 'ir33', displayname = 'R 3.3')" \
  && Rscript -e "install.packages('WaterML')" 

####################################
#         INSTALL R IRODS          #
####################################
ADD docker/icommands.sh /home/jovyan/libs/icommands.sh 

#  ###### BEGIN ROOT #######
   USER root
    RUN chmod +x /home/jovyan/libs/icommands.sh \
     && echo "/home/jovyan/libs" | /home/jovyan/libs/icommands.sh
   USER jovyan
#  ####### END ROOT ########

#############################
# ROOT - CLEANUP            #
#############################
USER root
RUN conda clean --all -y
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

########################################
# SWITCH BACK TO JOVYAN BEFORE LEAVING #
########################################
USER jovyan
