#!/bin/bash

#!/bin/bash

if [ $# -ne 1 ]; then
    echo
    echo "Usage: "$(basename "$0")" path_to_ros2_workspace"
    echo
    exit 1
fi

[ ! -d "$1" ] && echo "Directory '$1' DOES NOT exists"

WS_PATH=$(readlink -f $1)

docker run -it --rm -v $WS_PATH:/root/ws -p 11311:11311  osrf/ros:humble-desktop /bin/bash
