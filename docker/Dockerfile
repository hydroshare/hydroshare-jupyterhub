FROM castrona/hydroshare-jupyterhub:latest
MAINTAINER Tony Castronova <acastronova@cuahsi.org>

######################################################
### Begin - JupyterHub Development Image Additions ###
######################################################

USER root

RUN apt-get update -y
RUN apt-get install -y libx11-dev

# NBExtensions
RUN git clone https://github.com/Castronova/jupyter_contrib_nbextensions.git /home/jovyan/libs/jupyter_contrib_nbextensions
RUN pip3 install -e /home/jovyan/libs/jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --system
RUN jupyter nbextension enable recursivedelete/main --user --section=tree
RUN jupyter nbextensions_configurator disable --user
RUN chown -R jovyan:users /home/jovyan/.jupyter

ENV NOTEBOOK_HOME=/home/jovyan/work/notebooks
ENV PATH=$PATH:/home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode

USER jovyan

RUN pip install wget
RUN pip3 install wget 
RUN pip install ulmo

# patch hs_restclient v1.2.6 
ADD docker/hs_restclient.patch /home/jovyan/libs/hs_restclient/hs_restclient/hs_restclient.patch
RUN cd /home/jovyan/libs/hs_restclient/hs_restclient && patch < hs_restclient.patch

# install DHSVM (need to modify UFconfig.mk for linux)
RUN git clone -b glacier https://github.com/pnnl/DHSVM-PNNL.git /home/jovyan/libs/DHSVM-PNNL
RUN sed -i '/# CC = gcc/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk
RUN sed -i '/# CFLAGS = -O3 -fexceptions/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk
RUN sed -i '/# BLAS = -lgoto -lfrtbegin -lg2c $(XERBLA) -lpthread/s/^# //' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk
RUN sed -i 's/F77 = gfortran/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk
RUN sed -i 's/CFLAGS = -O3 -fno-common -no-cpp-precomp -fexception/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk
RUN sed -i 's/BLAS = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk
RUN sed -i 's/LAPACK = -framework Accelerate/# &/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/UFconfig/UFconfig.mk
RUN sed -i 's/DEFS =  -DHAVE_X11 -DHAVE_GLACIER/DEFS =  -DHAVE_X11/' /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode/makefile
RUN rm /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib/libcxsparse.a
RUN cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/Lib && make
RUN cd /home/jovyan/libs/DHSVM-PNNL/DHSVM/sourcecode && make 

# install Boost and Dakota
RUN wget -O /home/jovyan/libs/boost.tar.gz https://sourceforge.net/projects/boost/files/boost/1.53.0/boost_1_53_0.tar.gz/download
RUN mkdir /home/jovyan/libs/boost && tar xzfv /home/jovyan/libs/boost.tar.gz -C /home/jovyan/libs/boost --strip-components 1

  ###### BEGIN ROOT #######
  USER root
  
  RUN cd /home/jovyan/libs/boost && ./bootstrap.sh --prefix=/usr/local
  RUN echo "using mpi ;" >> /home/jovyan/libs/boost/tools/build/v2/user-config.jam
  RUN cd /home/jovyan/libs/boost && ./b2 --with=all -j 4 install; exit 0
  RUN sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf'
  RUN ldconfig
  RUN apt-get install -y libblas-dev liblapack-dev cmake
  
  USER jovyan
  ####### END ROOT ########

RUN wget https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.5-public.src.tar.gz -P /home/jovyan/libs
RUN tar xzf /home/jovyan/libs/dakota-6.5-public.src.tar.gz -C /home/jovyan/libs
RUN mkdir /home/jovyan/libs/dakota-6.5.0.src/build
ADD docker/dakota_template.cmake /home/jovyan/libs/dakota-6.5.0.src/build/BuildDakota.cmake
RUN cd /home/jovyan/libs/dakota*.src/build && cmake -C BuildDakota.cmake /home/jovyan/libs/dakota*.src

  ###### BEGIN ROOT #######
  USER root
  RUN cd /home/jovyan/libs/dakota*.src/build && make clean
  RUN cd /home/jovyan/libs/dakota*.src/build && make
  RUN cd /home/jovyan/libs/dakota*.src/build && make install
  ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
  USER jovyan
  ####### END ROOT ########

ADD docker/icommands.sh /home/jovyan/libs/icommands.sh 
USER root
RUN chmod +x /home/jovyan/libs/icommands.sh
RUN echo "/home/jovyan/libs" | /home/jovyan/libs/icommands.sh
USER jovyan

ENV \
PATH=/home/jovyan/libs/icommands:$PATH \
IRODS_PLUGINS_HOME=/home/jovyan/libs/icommands/plugins/ \
IRODS_ENVIRONMENT_FILE=/home/jovyan/work/notebooks/data/.irods/irods_environment.json \ 
IRODS_AUTHENTICATION_FILE=/home/jovyan/work/notebooks/data/.irods/.irodsA

RUN pip install git+https://github.com/cybergis/jupyterlib.git
RUN pip3 install git+https://github.com/cybergis/jupyterlib.git

  ###### BEGIN ROOT #######
  USER root

  # register the kernel in the current R installation
  RUN sh -c 'echo "deb http://cran.rstudio.com/bin/linux/debian jessie-cran3/" >> /etc/apt/sources.list'
  RUN gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
  RUN gpg -a --export E084DAB9 | apt-key add -
  RUN apt-key update
  RUN apt-get update
  
  # required libs for installing R packages
  RUN apt-get -y install \
      libcurl4-openssl-dev \
      libssl-dev \
      make \
      gcc \
      g++
  
  # install R-base packages (including IRKernel)
  RUN apt-get install --allow-unauthenticated --no-install-recommends -y r-base=3.3*
  RUN Rscript -e "install.packages('devtools', repos='http://archive.linux.duke.edu/cran')"
  RUN Rscript -e "devtools::install_github('IRkernel/IRkernel')"
  USER jovyan
  ####### END ROOT ########

RUN Rscript -e "IRkernel::installspec(name = 'ir33', displayname = 'R 3.3')"

RUN pip install geopandas
RUN pip3 install geopandas

RUN pip install graphviz
RUN pip3 install graphviz

###################################################
## End - JupyterHub Development Image Additions ###
###################################################
USER jovyan
CMD ["sh", "/srv/singleuser/singleuser.sh"]



