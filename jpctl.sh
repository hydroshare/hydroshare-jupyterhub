#!/usr/bin/env bash



set -eu
set -o pipefail
sudo ls > /dev/null # get sudo rights before user walks away


# start jupyterhub in individual screens  
REST_PATH="$(pwd)/rest"
JUPYTER_PATH="$(pwd)/jupyterhub"
ERR_PATH="$(pwd)"
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
       
       # remove dangline images 
       echo -e "--> removing dangling images"
       docker rmi $(docker images -q -f dangling=true) 2> /dev/null || true

       # remove the jupyterhub/singleuser image
       echo -e "--> removing the \"jupyterhub/singleuser\" image"
       docker rmi jupyterhub/singleuser 2> /dev/null || true

    fi
  fi

  
  if [[ "$(docker images -q jupyterhub/singleuser 2> /dev/null)" != "" ]]; then
    echo "Docker image \"jupyterhub/singleuser\" alread exists.  Use --clean option to force rebuild"
    return 1
  else
    # remove the jupyterhub/singleuser image
    echo -e "--> rebuilding the \"jupyterhub/singleuser\" image"
    cd ./docker && docker build -t jupyterhub/singleuser . 
  fi
}

start_services() {
    

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
  
  echo -e "\nRestarting screen instances"
  echo -n "--> starting rest..."
  sudo screen -dmS rest sh -c "cd $REST_PATH &&  ./run.sh >$ERR_PATH/rest.out 2> $ERR_PATH/rest.err"
  sleep 1 # give the session time to spin up
  if ! sudo screen -list | grep -q "rest"; then
    echo -e "\n**********************"
    echo -e "\nFailed to start rest"
    echo "**********************"
    cat rest.err
    return -1
  fi
  echo "done"

  echo -n "--> starting jupyter..."
  sudo screen -dmS jupyter sh -c "cd $JUPYTER_PATH && ./run.sh start > $ERR_PATH/jupyter.out > $ERR_PATH/jupyter.err"
  sleep 1 # give the session time to spin up
  if ! sudo screen -list | grep -q "jupyter"; then
    echo -e "\n**********************"
    echo -e "\nFailed to start jupyter"
    echo "**********************"
    cat jupyter.err
    return -1
  fi
  echo "done"


  echo -n "--> starting collector..."
  sudo screen -dmS collector sh -c "cd $JUPYTER_PATH && ./run_cull.sh > $ERR_PATH/cull.out 2> $ERR_PATH/cull.err"
  sleep 1 # give the session time to spin up
  if ! sudo screen -list | grep -q "collector"; then
    echo -e "\n**********************"
    echo -e "\nFailed to start collector"
    echo "**********************"
    cat cull.err
    return -1
  fi
  echo "done"


  echo -e "\nRunning Screens"
  sudo screen -list 



}

clean() {
  # remove error files
  sudo rm $ERR_PATH/*.err 2> /dev/null || true
  
  # remove jupyterhub files
  sudo rm $JUPYTER_PATH/jupyter.sqlite 2> /dev/null || true
  sudo rm $JUPYTER_PATH/jupyter.log 2> /dev/null || true
  sudo rm $JUPYTER_PATH/jupyterhub_cookie_secret 2> /dev/null || true

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
   echo "usage: $0 install       # installs required software and build jupyterhub docker containers"
   echo "usage: $0 start         # starts the jupyterhub screens"
   echo "usage: $0 clean         # cleans all jupyterhub screen instances and removes docker containers"
   echo "***"
}

### Display usage if exactly one argument is not provided ###
#if [  $# -ne 1 ]; then
#    display_usage
#    exit 1
#fi

echo $1 ${2:-} 

case "$1" in
    install) install $1
        ;;
    start) start_services "$1"
        ;;
    clean) clean $1
        ;;
    build) build_docker ${2:-}
        ;;
    *) display_usage
        ;;
esac

exit 0;


