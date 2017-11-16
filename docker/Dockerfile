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

# install Boost and Dakota
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

ADD docker/icommands.sh /home/jovyan/libs/icommands.sh 
USER root
RUN chmod +x /home/jovyan/libs/icommands.sh \
 && echo "/home/jovyan/libs" | /home/jovyan/libs/icommands.sh
USER jovyan

ENV \
PATH=/home/jovyan/libs/icommands:$PATH \
IRODS_PLUGINS_HOME=/home/jovyan/libs/icommands/plugins/ \
IRODS_ENVIRONMENT_FILE=/home/jovyan/work/notebooks/data/.irods/irods_environment.json \ 
IRODS_AUTHENTICATION_FILE=/home/jovyan/work/notebooks/data/.irods/.irodsA

RUN pip install git+https://github.com/cybergis/jupyterlib.git \
 && pip3 install git+https://github.com/cybergis/jupyterlib.git


#RUN Rscript -e "IRkernel::installspec(name = 'ir33', displayname = 'R 3.3')" \
ENV R_LIBS_SITE=/home/jovyan/.userRLib
RUN mkdir /home/jovyan/.userRLib

RUN conda create -y -n R
RUN conda update conda -y  #(conda update --all)

RUN conda install -n R -c r \
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

RUN pip install geopandas graphviz \
 && pip3 install geopandas graphviz

# celery
ENV PATH=/home/jovyan/libs:$PATH
RUN pip install celery \
 && pip3 install celery

RUN mkdir /home/jovyan/libs/celeryworker
ADD docker/celery/celeryworker  /home/jovyan/libs/celeryworker/
ENV PYTHONPATH=/home/jovyan/libs:$PYTHONPATH

###################################################
## End - JupyterHub Development Image Additions ###
###################################################
USER jovyan
CMD ["sh", "/srv/singleuser/singleuser.sh"]



