#!/usr/bin/env bash

while :
do 
  # stop old containers
#  TOTAL_CONTAINERS=$(docker ps -a -q | wc -l)
#  echo Found $TOTAL_CONTAINERS Total Containers 
  
  OLD_CONTAINERS=$(docker ps -a -q | grep 'Up [0-9] days' | wc -l | bc)
  if [ $OLD_CONTAINERS -ne 0 ] ; then
    echo STOPPING OLD CONTAINERS
    docker ps -a | grep 'Up [0-9] days' | awk '{print $1}' | xargs --no-run-if-empty docker stop
  fi

  # remove exited containers 
  EXITED_CONTAINERS=$(docker ps -a -q -f status=exited | wc -l | bc)
  if [ $EXITED_CONTAINERS -ne 0 ] ; then
    REM_NAMES=$(docker ps -a | awk '{if(NR>1) print $NF}')
    REM_ARRAY=(${REM_NAMES//:/ })
    for i in `seq 0 $(expr $EXITED_CONTAINERS - 1)`
    do 
      msg=$(echo $(date +"%c"):  Removing Container ${REM_ARRAY[i]})
      echo $msg >> docker.log
      echo $msg
      docker rm ${REM_ARRAY[i]}
    done
  fi

  # sleep for an hour
  sleep 3600

done



