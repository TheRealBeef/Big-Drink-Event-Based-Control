# ROS 2 publisher subscriber example

## This document shows step by step how to setup ros2 with a docker and how to use publisher-subscriber nodes

## 0. Prerequisits

* python3,

* VS Code (Optional but recommended)

## 1. Set up ros2 wrorkspace

* Pull ros 2 image:

  ```bash
    docker pull osrf/ros:humble-desktop
  ```

* Execute run.sh script:

  ```bash
    ./run.sh .
  ```

* source setup files:

  ```bash
    source /opt/ros/humble/setup.bash
  ```

* Create a ROS Workspace

  * Create a new directory

  ```bash
    mkdir -p ~/ws/src
    cd ~/ws/src
  ```

  * Clone a sample

* Attatch VS Code to a docker container (Optional)

  * Download a Docker extention

  * Go to Docker -> Containers -> right click on osrf/ros... -> Attatch Visual Studio Code

  * Wait until it sets up
