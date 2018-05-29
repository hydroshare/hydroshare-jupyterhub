FROM jupyter/scipy-notebook
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

EXPOSE 8888

USER root

############################
# ROOT - INSTALL LIBRARIES #
############################
RUN apt update \
    && apt-get install -y software-properties-common python-software-properties \
    && add-apt-repository -y ppa:ubuntugis/ppa \
    && add-apt-repository -y ppa:ubuntu-toolchain-r/test

RUN apt-get update && apt-get install --fix-missing -y --no-install-recommends \ 
  gcc-7 \
  g++-7 \
  autoconf=2.69-9 \
  automake=1:1.15-4ubuntu1 \
  libtool=2.4.6-0.1 \
  libgeos-dev \
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
  gdal-bin \
  python-gdal \
  grass \
  grass-dev \
  libbsd-dev \
  vlc  \
  libx11-dev \
  man-db \
  wget \
  bash-completion \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/

###################################
#          SYSTEM PREP            #
###################################

# create directories
RUN mkdir /home/jovyan/libs \
  && chown -R jovyan:users /home/jovyan/libs \
  && mkdir /home/jovyan/work/notebooks \
  && chown -R jovyan:users /home/jovyan/work/notebooks

# fetch juptyerhub-singleuser entrypoint
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/scripts/jupyterhub-singleuser -O /usr/local/bin/jupyterhub-singleuser \
  && chmod 755 /usr/local/bin/jupyterhub-singleuser
ADD singleuser.sh /srv/singleuser/singleuser.sh

## Prepare celery and add celery tasks
#RUN mkdir /home/jovyan/libs/celeryworker 
#ADD celery/celeryworker  /home/jovyan/libs/celeryworker/
#RUN chown -R jovyan:users /home/jovyan/libs/celeryworker  

# fetch the ecohydro config file
ADD https://raw.github.com/selimnairb/RHESSysWorkflows/master/docs/config/ecohydro-Linux.cfg /home/jovyan/.ecohydro.cfg
RUN chown jovyan:users /home/jovyan/.ecohydro.cfg


USER root


###################################
#              MPICH              #
###################################
# build mpich from source (gcc 7)
RUN git clone git://git.mpich.org/mpich.git /tmp/mpich \
    && cd /tmp/mpich \
    && git submodule update --init \
    && ./autogen.sh \
    && ./configure --prefix=/usr \
    && make -j8 \
    && make -j8 install \
    && rm -rf /tmp/mpich

###################################
#    DUAL INSTALL GCC/G++ 5/7     #
###################################

# dual install gcc, g++ 5 and 7
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-7 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-7 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-7 \
    && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/gcc-ar gcc-ar /usr/bin/gcc-ar-5 --slave /usr/bin/gcc-nm gcc-nm /usr/bin/gcc-nm-5 --slave /usr/bin/gcc-ranlib gcc-ranlib /usr/bin/gcc-ranlib-5 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 10 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5 10

###################################
#          INSTALL TAUDEM         #
###################################

# TAUDEM v5.3.9 (Develop)
RUN git clone --branch Develop https://github.com/dtarb/TauDEM.git /home/jovyan/libs/TauDEM \
    && cd /home/jovyan/libs/TauDEM \
    && git checkout bceeef2f6a399aa23749a7c7cae7fed521ea910f \
    && cd /home/jovyan/libs/TauDEM/src \
    && sed -i 's#\.\.#/usr/local/bin#g' makefile \
    && make \
    && rm -rf /home/jovyan/libs/TauDEM
USER jovyan

## TAUDEM v5.3.7 - build and install taudem (must happen before rhesyss b/c of gdal conflicts)
#RUN git clone --branch v5.3.7 https://github.com/dtarb/TauDEM.git /home/jovyan/libs/TauDEM \
#  && cd /home/jovyan/libs/TauDEM/src \
#  && sed -i 's#\.\.#/usr/local/bin#g' makefile \
#  && make \
#  && rm -rf /home/jovyan/libs/TauDEM
#USER jovyan

####################################
#      SETUP CONDA ENVIRONMENTS    #
####################################

# upgrade andaconda
# create python2 and R envs
#RUN conda update conda -y \
RUN conda create -y -n python2 python=2 \
    && conda create -y -n R \
    && conda clean --all -y

# link environments to bin
#   && ln -sf /opt/conda/bin/python /usr/bin/python3 \
#   && ln -sf /opt/conda/bin/pip /usr/bin/pip3 \
USER root
 RUN ln -sf /opt/conda/envs/python2/bin/python2 /usr/bin/python22 \
   && ln -sf /opt/conda/envs/python2/bin/pip /usr/bin/pip2 \
   && ln -s /opt/conda/envs/R/bin/R /usr/bin/R \
   && ln -s /opt/conda/envs/R/bin/Rscript /usr/bin/Rscript
USER jovyan
#
## update pip environments
##RUN pip3 install --no-cache-dir --upgrade pip \
##  && pip2 install --no-cache-dir --upgrade pip


####################################################
#       INSTALL ECOHYDROLIB/RHESSysWorkflows       #
####################################################

RUN /opt/conda/envs/python2/bin/pip install --no-cache-dir \
 git+https://github.com/leonard-psu/EcohydroLib.git \
 git+https://github.com/leonard-psu/RHESSysWorkflows.git

#pip2 install git+https://github.com/leonard-psu/EcohydroLib.git


###################################
#     INSTALL RHESSysWorkflows    #
###################################

##RUN /bin/bash -c "source activate python2" \ 
##    && pip install git+https://github.com/leonard-psu/RHESSysWorkflows.git
###RUN pip2 install git+https://github.com/leonard-psu/RHESSysWorkflows.git

# load the rhessys configuration file and modify for the current user
RUN sed -i -e 's|^ETC.*|ETC = /home/jovyan/libs/RHESSysWorkflows/etc|g' /home/jovyan/.ecohydro.cfg \
 && sed -i -e 's|^MODULE_PATH.*|MODULE_PATH = /home/jovyan/work/notebooks/.grass6/addons|g' /home/jovyan/.ecohydro.cfg \
 && sed -i -e 's|^MODULE_ETC.*|MODULE_ETC = /home/jovyan/libs/RHESSysWorkflows/etc/r.soils.texture|g' /home/jovyan/.ecohydro.cfg

# prepare grass environment
ADD rhessys_wf.py /home/jovyan/libs/rhessys_wf.py
ADD run.py /home/jovyan/libs/run.py

###################################
#     INSTALL BOOST AND DAKOTA    #
###################################

RUN wget -O /home/jovyan/libs/boost.tar.gz https://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.gz/download \
 && mkdir /home/jovyan/libs/boost \
 && tar xzfv /home/jovyan/libs/boost.tar.gz -C /home/jovyan/libs/boost --strip-components 1
RUN wget https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.5-public.src.tar.gz -P /home/jovyan/libs \
 && tar xzf /home/jovyan/libs/dakota-6.5-public.src.tar.gz -C /home/jovyan/libs \
 && mkdir /home/jovyan/libs/dakota-6.5.0.src/build 
ADD dakota_template.cmake /home/jovyan/libs/dakota-6.5.0.src/build/BuildDakota.cmake
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

  ###### BEGIN ROOT #######
  USER root
  RUN buildDeps='liblapack-dev python3-dev cmake' \
   && apt-get update && apt-get install -y libopenblas-dev $buildDeps --no-install-recommends \
   && rm -rf /var/lib/apt/lists/* \
   && echo 1 | update-alternatives --config gcc \
   && echo 1 | update-alternatives --config g++ \
   # build and install boost
   && echo $(gcc --version) \
   && echo $(g++ --version) \
   && cd /home/jovyan/libs/boost && ./bootstrap.sh --prefix=/usr/local \
   && echo "using mpi ;" >> /home/jovyan/libs/boost/tools/build/v2/user-config.jam \
   && export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python3.5m" \
   && cd /home/jovyan/libs/boost && ./b2 --with=all -j 4 install || echo "Errors in boost installation" \
   && sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf' \
   && ldconfig \
   # build and install dakota
   && echo $(gcc --version) \
   && echo $(g++ --version) \
   && cd /home/jovyan/libs/dakota*.src/build \
   && cmake -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python -C BuildDakota.cmake /home/jovyan/libs/dakota*.src \
   && make clean \
   && make \
   && make install \
   # remove boost and dakota source
   && rm -rf /home/jovyan/libs/boost* /home/jovyan/libs/dakota* \
   # remove build dependencies
   && apt-get purge -y --auto-remove $buildDeps
  USER jovyan
  ####### END ROOT ########

###################################
#         INSTALL DHSVM           #
###################################

USER root
RUN buildDeps='liblapack-dev python3-dev cmake flex' \
  && git clone -b glacier https://github.com/pnnl/DHSVM-PNNL.git /home/jovyan/libs/DHSVM-PNNL \
  && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
  && sed -i '/# CC = gcc/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i '/# CFLAGS = -O3 -fexceptions/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i '/# BLAS = -lgoto -lfrtbegin -lg2c $(XERBLA) -lpthread/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/F77 = gfortran/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/CFLAGS = -O3 -fno-common -no-cpp-precomp -fexception/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/BLAS = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/LAPACK = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
  && sed -i 's/DEFS =  -DHAVE_X11 -DHAVE_GLACIER/DEFS =  -DHAVE_X11/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode/makefile \
  && rm /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib/libcxsparse.a \
  && cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib \
  && make \
  && cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode \
  && make \
  && mv /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode/DHSVM3.1.3 /usr/local/bin \
  # remove DHSVM source 
  && rm -rf /home/jovyan/libs/DHSVM* \
  # remove build dependencies
  && apt-get purge -y --auto-remove $buildDeps
USER jovyan

####################################
#         INSTALL  IRODS           #
####################################
ADD icommands.sh /home/jovyan/libs/icommands.sh 

#  ###### BEGIN ROOT #######
   USER root
    RUN chmod +x /home/jovyan/libs/icommands.sh \
     && echo "/home/jovyan/libs" | /home/jovyan/libs/icommands.sh
   USER jovyan
#  ####### END ROOT ########

####################################
# USER JOVYAN - SET PATH VARIABLES #
####################################
ENV \
  PATH="/opt/conda/envs/python2/bin:/home/jovyan/libs:/home/jovyan/libs/icommands":$PATH \
  PYTHONPATH="/home/jovyan/work/notebooks:/home/jovyan/libs":$PYTHONPATH \
  DOCUMENTS="/home/jovyan/work/notebooks/documents" \
  DATA="/home/jovyan/work/notebooks/data" \
  HOME="/home/jovyan" \
  ECOHYDROLIB_CFG="/home/jovyan/.ecohydro.cfg" \
  LD_LIBRARY_PATH="/usr/lib/grass64/lib:$LD_LIBRARY_PATH" \
  NOTEBOOK_HOME="/home/jovyan/work/notebooks" \
  R_LIBS_SITE="/home/jovyan/.userRLib" \
  IRODS_PLUGINS_HOME="/home/jovyan/libs/icommands/plugins/" \
  IRODS_ENVIRONMENT_FILE="/home/jovyan/work/notebooks/data/.irods/irods_environment.json" \
  IRODS_AUTHENTICATION_FILE="/home/jovyan/work/notebooks/data/.irods/.irodsA"


####################################
#          INSTALL R KERNEL        #
####################################

# core R libraries (R 3.4.1)
RUN mkdir /home/jovyan/.userRLib \
 && conda install -n R -c r \
    r-base=3.4.3 \
    r-essentials=3.4.3 \
    r-devtools=1.13.4 \
    r-xml=3.98_1.9 \
    r-rjsonio=1.3_0 \
 && conda clean --all -y

# this is necessary to prevent the following error when running installspec
#RUN conda install -n R -c r r-base

# install waterML library
RUN echo "options(repos=structure(c(CRAN=\"http://archive.linux.duke.edu/cran\")))" >> /home/jovyan/.Rprofile \
  && Rscript -e "IRkernel::installspec(name = 'ir34', displayname = 'R 3.4')" \
  && Rscript -e "install.packages('WaterML')" 
#  && Rscript -e "install.packages('devtools', repos='http://archive.linux.duke.edu/cran')" \

##################################
#   INSTALL PYTHON 3 LIBRARIES    #
###################################

RUN conda config --add channels conda-forge \
 && conda config --add channels landlab \
 && conda config --add channels odm2

RUN conda install -y -n root \
       gdal \
       basemap \
       jupyterhub=0.7.2 \
       landlab \
       ulmo \
       celery \
       geopandas \
       graphviz \
    && conda clean --all -y 

# need bsddb-dev for bsddb3
# this should be moved to top of Dockerfile.
USER root
RUN apt-get update \
 && apt-get install -y libdb-dev
USER jovyan

RUN /opt/conda/bin/pip install --no-cache-dir \
    hs_restclient \
    wget \
    git+https://github.com/cybergis/jupyterlib.git

#    sciunit \
#    bsddb3 \
# && sciunit post-install 

###################################
#   INSTALL PYTHON 2 LIBRARIES    #
###################################

## PYTHON2 LEGACY
##RUN conda create --name py2legacy --clone python2
##RUN conda create --name py2legacy python=2.7
#
##RUN conda install -y -n py2legacy \
##    pandas=0.19 \
##    gdal \
##    basemap \
##    ipykernel \
##    ulmo \
##    geopandas \
##    graphviz \
##    wget \
###=1.19.1=he4ec0ba_0 \
##    celery \
## && conda clean --all -y
##
##RUN /opt/conda/envs/py2legacy/bin/pip install --no-cache-dir \ 
##    hs_restclient 
###    git+https://github.com/cybergis/jupyterlib.git
##
##RUN /opt/conda/envs/py2legacy/bin/python -m ipykernel install \ 
##    --prefix=/opt/conda/envs/py2legacy \
##    --display-name "Python 2 - Legacy"
##
##

# PYTHON 2
RUN conda install -y -n python2 \
    pandas=0.21.0 \
    gdal \
    basemap \
    ipykernel \
    ulmo \
    celery \
    geopandas \
    graphviz \
    statsmodels=0.8.0 \
    odm2api=0.6.0.a0 \
    landlab \
    bsddb \
 && conda clean --all -y

#RUN /opt/conda/envs/python2/bin/python \
# && pip install --no-cache-dir \ 
RUN /opt/conda/envs/python2/bin/pip install --no-cache-dir \
    hs_restclient \
    wget==3.2 \
    sciunit2 \
    git+https://github.com/cybergis/jupyterlib.git \
 && sciunit post-install 

# register the kernels
RUN python -m ipykernel install \
    --user \
    --name "python2" \
    --display-name "Python 2.7" 

# PYTHON 2 - SciUnit
RUN conda create -y -n sciunit python=2 \
  && conda clean --all -y

RUN conda install -y -n sciunit \
    pandas \
    gdal \
    basemap \
    ipykernel \
    ulmo \
    celery \
    geopandas \
    graphviz \
    statsmodels \
    odm2api=0.6.0.a0 \
    bsddb \
 && conda clean --all -y

#RUN /opt/conda/envs/sciunit/bin/python \
# && pip install --no-cache-dir \ 
RUN /opt/conda/envs/sciunit/bin/pip install --no-cache-dir \
    hs_restclient \
    wget \
    sciunit2 \
    git+https://github.com/cybergis/jupyterlib.git \
 && sciunit post-install 

# register the kernels
RUN python -m ipykernel install \
    --user \
    --name "sciunit" \
    --display-name "Sciunit - Python 2.7" 

###################################
#      INSTALL NBExtensions       #
###################################

RUN /opt/conda/bin/pip install --no-cache-dir \
 git+https://github.com/Castronova/jupyter_contrib_nbextensions.git \
 && jupyter contrib nbextension install --user \
 && jupyter nbextension enable recursivedelete/main --user --section=tree \
 && jupyter nbextensions_configurator disable --user \
 && chown -R jovyan:users /home/jovyan/.jupyter

####################################
##     INSTALL BOOST AND DAKOTA    #
####################################
#
#RUN wget -O /home/jovyan/libs/boost.tar.gz https://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.gz/download \
# && mkdir /home/jovyan/libs/boost \
# && tar xzfv /home/jovyan/libs/boost.tar.gz -C /home/jovyan/libs/boost --strip-components 1
#RUN wget https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.5-public.src.tar.gz -P /home/jovyan/libs \
# && tar xzf /home/jovyan/libs/dakota-6.5-public.src.tar.gz -C /home/jovyan/libs \
# && mkdir /home/jovyan/libs/dakota-6.5.0.src/build 
#ADD dakota_template.cmake /home/jovyan/libs/dakota-6.5.0.src/build/BuildDakota.cmake
#ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
#
#  ###### BEGIN ROOT #######
#  USER root
#  RUN buildDeps='liblapack-dev python3-dev cmake' \
#   && apt-get update && apt-get install -y libopenblas-dev $buildDeps --no-install-recommends \
#   && rm -rf /var/lib/apt/lists/* \
#   && echo 1 | update-alternatives --config gcc \
#   && echo 1 | update-alternatives --config g++ \
#   # build and install boost
#   && echo $(gcc --version) \
#   && echo $(g++ --version) \
#   && cd /home/jovyan/libs/boost && ./bootstrap.sh --prefix=/usr/local \
#   && echo "using mpi ;" >> /home/jovyan/libs/boost/tools/build/v2/user-config.jam \
#   && export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python3.5m" \
#   && cd /home/jovyan/libs/boost && ./b2 --with=all -j 4 install || echo "Errors in boost installation" \
#   && sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf' \
#   && ldconfig \
#   # build and install dakota
#   && echo $(gcc --version) \
#   && echo $(g++ --version) \
#   && cd /home/jovyan/libs/dakota*.src/build \
#   && cmake -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python -C BuildDakota.cmake /home/jovyan/libs/dakota*.src \
#   && make clean \
#   && make \
#   && make install \
#   # remove boost and dakota source
#   && rm -rf /home/jovyan/libs/boost* /home/jovyan/libs/dakota* \
#   # remove build dependencies
#   && apt-get purge -y --auto-remove $buildDeps
#  USER jovyan
#  ####### END ROOT ########
#
####################################
##         INSTALL DHSVM           #
####################################
#
#USER root
#RUN buildDeps='liblapack-dev python3-dev cmake flex' \
#  && git clone -b glacier https://github.com/pnnl/DHSVM-PNNL.git /home/jovyan/libs/DHSVM-PNNL \
#  && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
#  && sed -i '/# CC = gcc/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
#  && sed -i '/# CFLAGS = -O3 -fexceptions/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
#  && sed -i '/# BLAS = -lgoto -lfrtbegin -lg2c $(XERBLA) -lpthread/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
#  && sed -i 's/F77 = gfortran/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
#  && sed -i 's/CFLAGS = -O3 -fno-common -no-cpp-precomp -fexception/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
#  && sed -i 's/BLAS = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
#  && sed -i 's/LAPACK = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk \
#  && sed -i 's/DEFS =  -DHAVE_X11 -DHAVE_GLACIER/DEFS =  -DHAVE_X11/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode/makefile \
#  && rm /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib/libcxsparse.a \
#  && cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib \
#  && make \
#  && cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode \
#  && make \
#  && mv /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode/DHSVM3.1.3 /usr/local/bin \
#  # remove DHSVM source 
#  && rm -rf /home/jovyan/libs/DHSVM* \
#  # remove build dependencies
#  && apt-get purge -y --auto-remove $buildDeps
#USER jovyan
#
#####################################
##         INSTALL  IRODS           #
#####################################
#ADD icommands.sh /home/jovyan/libs/icommands.sh 
#
##  ###### BEGIN ROOT #######
#   USER root
#    RUN chmod +x /home/jovyan/libs/icommands.sh \
#     && echo "/home/jovyan/libs" | /home/jovyan/libs/icommands.sh
#   USER jovyan
##  ####### END ROOT ########


#############################
# ROOT - CLEANUP            #
#############################
USER root
RUN conda clean --all -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /tmp/*

########################################
# SWITCH BACK TO JOVYAN BEFORE LEAVING #
########################################
USER jovyan
