#!/bin/bash

if [ $# -ne 1 ]; then
  echo
  echo "Usage: "$(basename "$0")" path_to_ros2_workspace"
  echo
  exit 1
fi

[ ! -d "$1" ] && echo "Directory '$1' DOES NOT exists"
 
WS_PATH=$(readlink -f $1)

scriptDir=$(dirname $0 | xargs -i readlink -f {})

docker run --rm \
    --privileged \
    --env DISPLAY \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $HOME/.ssh:/home/developer/.ssh \
    -v "$scriptDir/shared/:/projects" \
    -v $WS_PATH:/root/ws \
    --privileged \
    --net=host \
    --hostname $(hostname) \
    -it osrf/ros:humble-desktop /bin/bash
