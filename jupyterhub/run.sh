#!/usr/bin/env bash


set -eu
set -o pipefail
sudo ls > /dev/null # get sudo rights before user walks away

run() {

    here="$(dirname $0)"

    # load github auth from env
    source $here/env

    echo "Starting Jupyterhub with the following args: ${@:2}"
    # $@ passes input args to the jupyterhub command (i.e. -f myconfig --log-file=mylog.log --port=8000)
    sudo -E jupyterhub ${@:2}
    #jupyterhub ${@:2}

}

run-debug() {

    echo "RUNNING JUPYTERHUB IN DEBUG MODE"

    # remove all docker containers
    docker rm -f $(docker ps -a -q) 2> /dev/null || true

    # start the jupyterhub server as usual
    run "$@"

}

usage() {

    echo -e "\n*** General Usage ***"
    echo -e "$0 start -f myconfig.py --log-file=mylog.log --port=8000"
    echo -e "*** *** *** *** *** ***\n"
    echo "usage: $0 start           # starts the jupyterhub server with any combination of jupyter args"
}

if [  $# -lt 1 ]
then
    usage
    exit 1
fi

case "$1" in
    start) run "$@"
        ;;
    start-debug) run-debug "$@"
        ;;
    *) usage
        ;;
esac

exit 0;
