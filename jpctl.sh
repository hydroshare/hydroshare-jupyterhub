#!/usr/bin/env bash



set -eu
set -o pipefail
sudo ls > /dev/null # get sudo rights before user walks away


# start jupyterhub in individual screens
REST_PATH="$(pwd)/rest"
JUPYTER_PATH="$(pwd)/jupyterhub"
LOG_PATH="$(pwd)/log"
DOCKERSPAWNER_PATH="$(pwd)/dockerspawner"
OAUTHENTICATOR_PATH="$(pwd)/oauthenticator"
JUPYTERHUBRESTSERVER="$(pwd)/jupyterhub_rest_server"
INSTALL_TMP_DIR="$(pwd)/install"

clean() {
  
  # remove containers
  echo -n "--> removing containers..."
  sudo docker rm -fv $(docker ps -a -q) 2> /dev/null || true
  echo "done"
       
  # remove dangling images
  echo -n "--> removing dangling images..."
  docker rmi $(docker images -q -f dangling=true) 2> /dev/null || true
  echo "done" 

  # parse args if they are provided
  if [[ $# -ne 0 ]] ;  then
    if [[ $1 == "--systemd" ]]; then
       clean_systemd
    elif [[ $1 == "--screen" ]]; then
       clean_screen
    else
       echo -e "--> [Error] invalid argument: $1\nSee help for vaild start arguments\n"
    fi
  else
     echo -e "--> no 'clean' argument was provided, so I will attempt to clean both screen and systemd processes."
     clean_screen
     clean_systemd
  fi

}

clean_screen(){
  # remove error files
  echo -n "--> removing error logs..."
  sudo rm $LOG_PATH/*.err 2> /dev/null || true
  sudo rm $JUPYTER_PATH/jupyter.log 2> /dev/null || true
  echo "done"

  # remove jupyterhub files
  echo -n "--> removing database..."
  sudo rm $JUPYTER_PATH/jupyter.sqlite 2> /dev/null || true
  echo "done"

  echo -n "--> removing cookies..."
  sudo rm $JUPYTER_PATH/jupyterhub_cookie_secret 2> /dev/null || true
  echo "done"
 
}

clean_systemd(){

  # remove error files
  echo -n "--> removing error logs..."
  sudo rm /etc/jupyterhub/server/*.err 2> /dev/null || true
  sudo rm /etc/jupyterhub/server/*.log 2> /dev/null || true
  echo "done"

  # remove jupyterhub files
  echo -n "--> removing database..."
  sudo rm /etc/jupyterhub/server/*.sqlite 2> /dev/null || true
  echo "done"

  echo -n "--> removing cookies..."
  sudo rm /etc/jupyterhub/server/*cookie_secret 2> /dev/null || true
  echo "done"
}

install_base_ubuntu() {
    # install jupyterhub dependencies
    echo -e "--> installing system requirements"
    sudo apt-get clean  
    sudo apt-get update --fix-missing  
    sudo apt-get install -y openssh-server wget screen docker python3-dateutil

    # install node and configurable proxy
    echo -e "--> installing nodejs and configurable-http-proxy"
    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
    sudo apt-get install -y nodejs 
    sudo npm install -g configurable-http-proxy



}

install_base_rhel() {
    # install jupyterhub dependencies
    echo -e "--> installing system requirements"
    sudo yum clean all
    sudo yum update update
    sudo yum install -y openssh-server wget screen docker python3-dateutil

    # install node and configurable proxy
    echo -e "--> installing nodejs and configurable-http-proxy"
    curl --silent --location https://rpm.nodesource.com/setup_6.x | bash -
    sudo yum -y install nodejs
    sudo npm install -g configurable-http-proxy
}

install() {

    # parse args
    if [[ $# -ne 0 ]] ;  then
	if [[ $1 == "--ubuntu" ]]; then
	    install_base_ubuntu
	elif [[ $1 == "--rhel" ]]; then
	    install_base_rhel
        else
	    echo -e "--> [Error] invalid installation platform argument: $1\nSee help for valid arguments\n"
	    return -1
	fi
    else
	echo -e "--> [Error] missing installation platform argument: $1\nSee help for valid arguments\n"
	return -1
    fi


#    # install jupyterhub dependencies
#    echo -e "--> installing system requirements"
#    sudo apt-get clean  
#    sudo apt-get update --fix-missing  
#    sudo apt-get install -y openssh-server wget screen docker python3-dateutil

    # activate and enable docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # install pip, ipgetter, and jupyterhub
    echo -e "--> installing pip3, ipgetter, jupyterHub"
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    sudo pip3 install ipgetter
    sudo pip3 install "ipython[notebook]" jupyterhub
    rm get-pip.py

#    # install node and configurable proxy
#    echo -e "--> installing nodejs and configurable-http-proxy"
#    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
#    sudo apt-get install -y nodejs 
#    sudo npm install -g configurable-http-proxy

    # build the jupyterhub docker image  
    echo -e "--> building the jupyterhub docker image"
    cd ./docker && docker build -t jupyterhub/singleuser .

    # install dockerspawner 
    echo -e "--> installing dockerspawner"
    sudo pip3 install -e $DOCKERSPAWNER_PATH

    # install oauthenticator 
    echo -e "--> installing oauthenticator"
    sudo pip3 install -e $OAUTHENTICATOR_PATH

    # install JupyterHub rest server
    echo -e "--> installing jupyterhub rest server"
    sudo -H pip3 install -e $JUPYTERHUBRESTSERVER

    # install jupyterhub services
    echo -e "--> installing jupyterhub services"
    echo -e "----> copying config-prod to install directory"
    cp $JUPYTER_PATH/config.py $INSTALL_TMP_DIR/config.py
    echo -e "----> copying env to install directory"
    cp $JUPYTER_PATH/env $INSTALL_TMP_DIR/env
    sudo $INSTALL_TMP_DIR/install-services.sh

}

uninstall() {
   # todo: finish this function
   printf "Uninstalling DockerSpawner\n"
   cat dockerspawner_install_files.txt | sudo xargs rm -rf
   
   printf "Uninstalling  OAuthenticator\n"
   cat oauthenticator_install_files.txt | sudo xargs rm -rf

   echo -3 "--> removing jupyterhub systemd services"
   sudo rm -rf /etc/jupyterhub
   sudo rm /lib/systemd/system/jupyterhub.service
   sudo rm /lib/systemd/system/jupyterhubrestserver.service
}

build_docker() {

  # parse args if they are provided
  if [[ $# -ne 0 ]] ;  then

    # clean the jupyterhub/single user image
    if [[ $1 == "--clean" ]]; then
       
       # stop all the containers
       echo -e "--> stopping all containers"
       docker stop $(docker ps -a -q) 2> /dev/null || true
      
       # clean dangling images and old jupyterhub files
       clean
 
       echo -e "--> removing all docker images"
       docker rmi $(docker images -q) 2> /dev/null || true


    fi
  fi


  if [[ "$(docker images -q docker.io/castrona/hydroshare-jupyterhub 2> /dev/null)" != "" ]]; then
    echo -e "--> reusing existing base image.  Use --clean option to force rebuild of base image"
  else
    # pull the latest base image
    echo -e "--> pulling the latest \"hydroshare-jupyterhub\" base image"
    docker pull castrona/hydroshare-jupyterhub:latest
  fi
  
  # remove the jupyterhub/singleuser image
  echo -e "--> building the \"jupyterhub/singleuser\" image"
  docker build -f ./docker/Dockerfile -t jupyterhub/singleuser .
}

update_docker_images() {
  #
  # Updates the docker base-image without shutting down the server to minimize downtime
  #

  # pull the latest base image
  echo -e "--> pulling the latest \"hydroshare-jupyterhub\" base image"
  docker pull castrona/hydroshare-jupyterhub:latest

  # remove the jupyterhub/singleuser image
  echo -e "--> building the \"jupyterhub/singleuser\" image"
  docker build -f ./docker/Dockerfile -t jupyterhub/singleuser .

  # clean dangling images and old jupyterhub files
  clean

}
stop_services() {

  # parse args if they are provided
  if [[ $# -ne 0 ]] ;  then
    if [[ $1 == "--systemd" ]]; then
       stop_systemctl
    else
       stop_screen
    fi
  fi

}

stop_screen() {

  echo "Shutting screen instances"

  echo -n "--> killing rest..."
  if sudo screen -list | grep -q "rest"; then
    sudo screen -S rest -X at "#" stuff $'\003'
    sudo screen -X -S rest quit > /dev/null
    sleep 1
  fi
  echo "done"

  echo -n "--> killing jupyter..."
  if sudo screen -list | grep -q "jupyter"; then
    sudo screen -S jupyter -X at "#" stuff $'\003'
    sudo screen -X -S jupyter quit > /dev/null
    sleep 1
  fi
  echo "done"

  echo -n "--> killing collector..."
  if sudo screen -list | grep -q "collector"; then
    sudo screen -S collector -X at "#" stuff $'\003'
    sudo screen -X -S collector quit > /dev/null
    sleep 1
  fi
  echo "done"

}

start_services() {

  # parse args if they are provided
  if [[ $# -ne 0 ]] ;  then
    if [[ $1 == "--debug" ]]; then
        restart_screen $1
    elif [[ $1 == "--systemd" ]]; then
       start_systemctl
    else
       echo -e "invalid argument: $1\nSee help for vaild start arguments\n"
    fi
  fi
}

restart_screen() {

  JUPYTER_CMD="start"
  RUN_CULL=true
  if [[ $# -ne 0 ]] ;  then
    if [[ $1 == "--debug" ]]; then
       JUPYTER_CMD="start-debug"
       RUN_CULL=false
    fi
  fi

  stop_services 
  
  # remove the error logs before attempting restart 
  if ls | grep -q "rest.err"; then
      sudo rm rest.err > /dev/null
  fi

  if ls | grep -q "jupyter.err"; then
      sudo rm jupyter.err > /dev/null
  fi

  if ls | grep -q "cull.err"; then
      sudo rm cull.err > /dev/null
  fi

  # make output dir
  mkdir -p ./log

  echo -e "\nRestarting screen instances"
  echo -n "--> starting rest..."
  sudo screen -dmS rest sh -c "cd $REST_PATH &&  ./run.sh >$LOG_PATH/rest.out 2> $LOG_PATH/rest.err"
  sleep 1 # give the session time to spin up
  if ! sudo screen -list | grep -q "rest"; then
    echo -e "\n\n**********************"
    echo -e "Failed to start rest"
    echo "**********************"
    cat $LOG_PATH/rest.err
    return -1
  fi
  echo "done"

  echo -n "--> starting jupyter..."
  sudo screen -dmS jupyter sh -c "cd $JUPYTER_PATH && ./run.sh $JUPYTER_CMD > $LOG_PATH/jupyter.out 2> $LOG_PATH/jupyter.err"
  sleep 1 # give the session time to spin up
  if ! sudo screen -list | grep -q "jupyter"; then
    echo -e "\n\n**********************"
    echo -e "Failed to start jupyter"
    echo "**********************"
    cat $LOG_PATH/jupyter.err
    return -1
  fi
  echo "done"
  
  if "$RUN_CULL" = true; then
    echo -n "--> starting collector..."
    sudo screen -dmS collector sh -c "cd $JUPYTER_PATH && ./run_cull.sh > $LOG_PATH/cull.out 2> $LOG_PATH/cull.err"
    sleep 1 # give the session time to spin up
    if ! sudo screen -list | grep -q "collector"; then
      echo -e "\n\n**********************"
      echo -e "Failed to start collector"
      echo "**********************"
      cat $LOG_PATH/cull.err
      return -1
    fi
    echo "done"
  else 
    echo "--> skipping collector startup because you are running in debug mode" 
  fi

  echo -e "\nRunning Screens"
  sudo screen -list 
}

start_systemctl(){
   echo -e "--> starting jupyterhub..."
   sudo systemctl start jupyterhub
   sleep 3
   isactive jupyterhub
   
   echo -e "--> starting jupyterhub rest server..."
   sudo systemctl start jupyterhubrestserver
   sleep 3
   isactive jupyterhubrestserver

   echo -e "To view systemd logs:\n  journalctl -f -u jupyterhub\n"

}

stop_systemctl(){
   echo -e "--> stopping jupyterhub..."
   sudo systemctl stop jupyterhub
   isactive jupyterhub
   
   echo -e "--> stopping jupyterhub rest server..."
   sudo systemctl stop jupyterhubrestserver
   isactive jupyterhubrestserver
}

isactive() {
  RED='\033[0;31m'
  GRN='\033[0;32m'
  NC='\033[0m' # No Color

  if [ "`sudo systemctl is-active ${1}`" != "active" ]; then
    echo -e "${RED} [-] ${1} is not running${NC}\n"
  else  
    echo -e "${GRN} [+] ${1} is running${NC}\n" 
  fi
}

run_tests(){

   docker run --rm -it -u root -v $(pwd)/notebooks:/home/jovyan/work jupyterhub/singleuser sh test/run-tests.sh
    
}

display_usage() {
   echo "*** JupyterHub Control Script ***"
   echo "usage: $0 install --ubuntu            # install required software and build jupyterhub docker containers (ubuntu)"
   echo "usage: $0 install --rhel            # install required software and build jupyterhub docker containers (RHEL)"
   echo "usage: $0 build              # build the jupyter docker images"
   echo "usage: $0 build --clean      # force a clean build the jupyter docker images"
   echo "usage: $0 update             # update the base docker image on a production server (designed to minimize server downtime)"
   echo "usage: $0 start              # start the jupyterhub in production mode (using screen)"
   echo "usage: $0 start --systemd    # start the jupyterhub services (using systemd)"
   echo "usage: $0 start --debug      # start the jupyterhub in debug mode, necessary for development (using screen)"
   echo "usage: $0 stop               # stop all jupyterhub services (using screen)"
   echo "usage: $0 stop --systemd     # stop all jupyterhub services (using systemd)"
   echo "usage: $0 clean --systemd    # clean all jupyterhub images, containers, and system files (using systemd)"
   echo "usage: $0 clean --screen     # clean all jupyterhub images, containers, and system files (using screen)"
   echo "usage: $0 test               # run unittests"
   echo "***"
}

#echo $1 ${2:-}
if [ $# -eq 0 ] ; then
    display_usage
    exit 1
fi

case "$1" in
    install) install ${2:-}
        ;;
    start) start_services ${2:-}
        ;;
    stop) stop_services ${2:-}
        ;;
    clean) clean ${2:-}
        ;;
    build) build_docker ${2:-}
        ;;
    update) update_docker_images $1
        ;;
    test) run_tests $1
	;;
    *) display_usage
        ;;
esac

exit 0;
