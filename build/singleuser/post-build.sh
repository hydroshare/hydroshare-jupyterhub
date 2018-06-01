#/bin/bash

##########################################
# these are tasks that should be executed 
# at the end of every build
##########################################

#Rscript -e "IRkernel::installspec(name = 'ir34', displayname = 'R 3.4')"

# register conda kernels
python3 -m ipykernel install \
    --user \
    --name "python2" \
    --display-name "Python 2.7"

python3 -m ipykernel install \
    --user \
    --name "R" \
    --display-name "R 3.4"

