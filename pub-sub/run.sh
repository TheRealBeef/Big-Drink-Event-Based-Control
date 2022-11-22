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

docker run -it --rm \
  -v $WS_PATH:/root/ws \
  --env="DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  osrf/ros:humble-desktop \
  /bin/bash

# docker run -it --rm \
#   -v /tmp/.X11-unix:/tmp/.X11-unix \
#   -v $WS_PATH:/root/ws \
#   --net=host \
#   -e DISPLAY=$DISPLAY \
#   osrf/ros:humble-desktop \
#   /bin/bash