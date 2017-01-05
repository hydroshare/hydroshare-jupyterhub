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


install() {
    # install jupyterhub dependencies
    printf "Installing system requirements\n"
    sudo apt-get clean  
    sudo apt-get update --fix-missing  
    sudo apt-get install -y openssh-server wget screen docker python3-dateutil

    # install pip, ipgetter, and jupyterhub
    printf "Installing Pip3, Ipgetter, JupyterHub\n"
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    sudo pip3 install ipgetter
    sudo pip3 install "ipython[notebook]" jupyterhub

    # install node and configurable proxy
    printf "Installing NodeJS and configurable-http-proxy\n"
    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
    sudo apt-get install -y nodejs 
    sudo npm install -g configurable-http-proxy

    # build the jupyterhub docker image  
    printf "Building the JupyterHub Docker image\n"
    cd ./docker && docker build -t jupyterhub/singleuser .

    # install dockerspawner dependencies
    sudo pip3 install -r $DOCKERSPAWNER_PATH/requirements.txt

    # install oauthenticator dependencies
    sudo pip3 install -r $OAUTHENTICATOR_PATH/requirements.txt
}


build_docker() {

  # parse args if they are provided
  if [[ $# -ne 0 ]] ;  then

    # clean the jupyterhub/single user image
    if [[ $1 == "--clean" ]]; then
       
       # stop all the containers
       echo -e "--> stopping all containers"
       docker stop $(docker ps -a -q) 2> /dev/null || true
       
       # remove all containers  
       echo -e "--> removing all containers"
       docker rm -fv $(docker ps -a -q) 2> /dev/null || true
       
       # remove dangling images
       echo -e "--> removing dangling images"
       docker rmi $(docker images -q -f dangling=true) 2> /dev/null || true

       echo -e "--> removing all docker images"
       docker rmi $(docker images -q) 2> /dev/null || true
    fi
  fi


#  if [[ "$(docker images -q jupyterhub/singleuser 2> /dev/null)" != "" ]]; then
#    echo "Docker image \"jupyterhub/singleuser\" alread exists.  Use --clean option to force rebuild"
#    return 1
#  else
    # remove the jupyterhub/singleuser image
    echo -e "--> building the \"jupyterhub/singleuser\" image"
    docker build -f ./docker/Dockerfile -t jupyterhub/singleuser .
#  fi
}

start_services() {

  JUPYTER_CMD="start"
  RUN_CULL=true
  # parse args if they are provided
  if [[ $# -ne 0 ]] ;  then
    if [[ $1 == "--debug" ]]; then
       JUPYTER_CMD="start-debug"
       RUN_CULL=false
    fi
  fi
 
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

clean() {
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

  echo -n "--> removing containers..."
  sudo docker rm -fv $(docker ps -a -q) 2> /dev/null || true
  echo "done"
       
  # remove dangling images
  echo -n "--> removing dangling images..."
  docker rmi $(docker images -q -f dangling=true) 2> /dev/null || true
  echo "done"
}

old() {
    # start jupyterhub in individual screens  
    REST_PATH="$(pwd)/rest"
    JUPYTER_PATH="$(pwd)/jupyterhub"

    printf "Starting the REST Server in Screen\n"
    sudo screen -dmS rest sh -c "cd $REST_PATH && sh run.sh 2> rest.err"

    printf "Starting the JupyterHub Server in Screen\n"
    sudo screen -dmS jupyter sh -c "cd $JUPYTER_PATH && sh run.sh 2> jupyter.err"

    printf "Starting the Docker Image Collector in Screen\n"
    sudo screen -dmS collector sh -c "cd $JUPYTER_PATH && sh run_cull.sh 2> cull.err"

    printf "List of Screen Instances\n"
    sudo screen -list 
}

display_usage() {
   echo "*** JupyterHub Control Script ***"
   echo "usage: $0 install            # install required software and build jupyterhub docker containers"
   echo "usage: $0 build              # build the jupyter docker images"
   echo "usage: $0 build --clean      # force a clean build the jupyter docker images"
   echo "usage: $0 start              # start the jupyterhub in production mode"
   echo "usage: $0 start --debug      # start the jupyterhub in debug mode, necessary for development"
   echo "usage: $0 clean              # clean all jupyterhub screen instances and removes docker containers"
   echo "***"
}

#echo $1 ${2:-}
if [ $# -eq 0 ] ; then
    display_usage
    exit 1
fi

case "$1" in
    install) install $1
        ;;
    start) start_services ${2:-}
        ;;
    clean) clean $1
        ;;
    build) build_docker ${2:-}
        ;;
    *) display_usage
        ;;
esac

exit 0;
