#!/bin/bash
set -x
set -e

####################################
#         INSTALL  IRODS           #
####################################

chmod +x /home/jovyan/libs/icommands.sh 
echo "/home/jovyan/libs" | /home/jovyan/libs/icommands.sh

