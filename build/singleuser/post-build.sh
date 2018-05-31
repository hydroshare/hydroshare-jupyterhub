#/bin/bash

##########################################
# these are tasks that should be executed 
# at the end of every build
##########################################

# register conda kernels
Rscript -e "IRkernel::installspec(name = 'ir34', displayname = 'R 3.4')"
python -m ipykernel install \
    --user \
    --name "python2" \
    --display-name "Python 2.7"


