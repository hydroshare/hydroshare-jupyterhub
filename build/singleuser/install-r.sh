#!/bin/bash
set -x
set -e

####################################
#          INSTALL R KERNEL        #
####################################

mkdir $HOME/.userRLib
echo "options(repos=structure(c(CRAN=\"http://archive.linux.duke.edu/cran\")))" >> $HOME/.Rprofile
conda config --add channels r

conda install -n R -c r \
    r-base=3.4.1 \
    r-irkernel \
    r-essentials \
    r-devtools \
    r-xml \
    r-rjsonio \
    r-ncdf4 \
    r-sf

Rscript -e "install.packages('WaterML')" 
Rscript -e "install.packages('dplyr')" 
Rscript -e "install.packages('dataRetrieval',repos='https://owi.usgs.gov/R')"
Rscript -e "install.packages('stringi')"
Rscript -e "IRkernel::installspec(name = 'ir34', displayname = 'R 3.4')" 

conda clean --all -y
