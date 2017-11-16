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

  clean_systemd
}

clean_systemd(){

  echo -e '\nCLEANING SYSTEMD FILES\n'

  # remove error files
  echo -n "--> removing systemd error logs..."
  sudo rm /etc/jupyterhub/server/*.err 2> /dev/null || true
  sudo rm /etc/jupyterhub/server/*.log 2> /dev/null || true
  echo "done"

  # remove jupyterhub files
  echo -n "--> removing systemd database..."
  sudo rm /etc/jupyterhub/server/*.sqlite 2> /dev/null || true
  echo "done"

  echo -n "--> removing systemd cookies..."
  sudo rm /etc/jupyterhub/server/*cookie_secret 2> /dev/null || true
  echo "done"
}

install_base_ubuntu() {
    # install jupyterhub dependencies
    echo -e "--> installing system requirements"
    sudo apt-get clean  
    sudo apt-get update --fix-missing  
    sudo apt-get install -y openssh-server wget screen docker python3-dateutil, tree

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
    sudo yum install -y openssh-server wget screen docker tree gcc-c++ make

    if ( ! which python3 ); then
        sudo rpm -Uvh https://centos7.iuscommunity.org/ius-release.rpm || true
        sudo yum install -y python35u python35u-libs python35u-devel python35u-pip
        sudo ln -sf /usr/bin/python3.5 /usr/bin/python3
        sudo ln -sf /usr/bin/pip3.5 /usr/bin/pip3
    fi
    sudo pip3 install python-dateutil

    # install epel
    sudo yum install -y epel-release

    # install node and configurable proxy
    echo -e "--> installing nodejs and configurable-http-proxy"
    sudo yum install -y nodejs
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
	echo -e "--> [Error] missing installation platform argument: \nSee help for valid arguments\n"
	return -1
    fi

    # activate and enable docker
    sudo systemctl enable docker
    sudo systemctl start docker
    
    # install pip, ipgetter, and jupyterhub
    echo -e "--> installing pip3, ipgetter, jupyterHub"
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    sudo pip3 install ipgetter
    sudo pip3 install "ipython[notebook]" jupyterhub
    rm get-pip.py

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


  if [[ "$(docker images -q castrona/hydroshare-jupyterhub 2> /dev/null)" != "" ]]; then
    echo -e "--> reusing existing base image.  Use --clean option to force rebuild of base image"
  else
    # pull the latest base image
    echo -e "--> pulling the latest \"hydroshare-jupyterhub\" base image"
    docker pull castrona/hydroshare-jupyterhub:latest
  fi
  
  # remove the jupyterhub/singleuser image
  echo -e "--> building the \"jupyterhub/singleuser\" image"
  docker build -f ./docker/Dockerfile -t jupyterhub/singleuser .

  # build celery workers
  echo -e "--> building celery workers"
  docker-compose -f docker/celery/docker-compose.yml build
  docker-compose -f docker/celery/docker-compose.yml scale worker=5
 
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

     stop_systemctl

}

start_services() {

     start_systemctl
}


start_systemctl(){

   echo -e "\nSTARTING SYSTEMD SERVICES\n"
  
   echo -e "--> starting jupyterhub..."
   sudo systemctl start jupyterhub
   sleep 3
   isactive jupyterhub
   
   echo -e "--> starting jupyterhub rest server..."
   sudo systemctl start jupyterhubrestserver
   sleep 3
   isactive jupyterhubrestserver

   echo -e "--> starting celery workers..."
   docker-compose -f docker/celery/docker-compose.yml up -d

   echo -e "To view systemd logs:\n  journalctl -f -u jupyterhub\n"

}

stop_systemctl(){

   echo -e "\nSTOPPING SYSTEMD SERVICES\n"

   echo -e "--> stopping jupyterhub..."
   sudo systemctl stop jupyterhub
   isactive jupyterhub
   
   echo -e "--> stopping jupyterhub rest server..."
   sudo systemctl stop jupyterhubrestserver
   isactive jupyterhubrestserver

   echo -e "--> stopping celery workers..."
   docker-compose -f docker/celery/docker-compose.yml stop

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

restart_services(){

  stop_services

  clean --systemd

  start_services
}

display_usage() {
   echo "*** JupyterHub Control Script ***"
   echo "usage: $0 install --ubuntu   # install required software and build jupyterhub docker containers (ubuntu)"
   echo "usage: $0 install --rhel     # install required software and build jupyterhub docker containers (RHEL)"
   echo "usage: $0 build              # build the jupyter docker images"
   echo "usage: $0 build --clean      # force a clean build the jupyter docker images"
   echo "usage: $0 update             # update the base docker image on a production server (designed to minimize server downtime)"
   echo "usage: $0 start              # start the jupyterhub services (using systemd)"
   echo "usage: $0 stop               # stop all jupyterhub services (using systemd)"
   echo "usage: $0 clean              # clean all jupyterhub images, containers, and system files (using systemd)"
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
    restart) restart_services 
        ;;
    *) display_usage
        ;;
esac

exit 0;
