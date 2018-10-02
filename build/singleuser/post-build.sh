#/bin/bash

##########################################
# these are tasks that should be executed 
# at the end of every build
##########################################

Rscript -e "IRkernel::installspec(name = 'ir34', displayname = 'R 3.4', user=FALSE)"

# register conda kernels
/opt/conda/envs/python2/bin/python -m ipykernel install \
    --prefix=/usr/local \
    --name "python2" \
    --display-name "Python 2.7"

