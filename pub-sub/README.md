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

* Create a ROS Workspace

  * Create a new directory

  ```bash
    mkdir -p ~/ws/src
    cd ~/ws/src
  ```

  * Clone a sample repo
  
  ```bash
    git clone https://github.com/ros/ros_tutorials.git -b humble-devel
  ```

  * Resolve dependencies

  ```bash
    cd ..
    rosdep install -i --from-path src --rosdistro humble -y
  ```

  * Build a workspace with colon (it took me about 30s)
  
  ```bash
    colcon build
  ```

  * source the overlay
  
  ``` bash
    source /opt/ros/humble/setup.bash
  ```

  * make sure you are in `~/ws` directory, source the overlay

  ```bash
    . install/local_setup.bash
  ```

  * run the `turtlesim` package

  ```bash
    ros2 run turtlesim turtlesim_node
  ```

* Attatch VS Code to a docker container (Optional)

  * Download a Docker extention

  * Go to Docker -> Containers -> right click on osrf/ros... -> Attatch Visual Studio Code

  * Wait until it sets up

## 2. Publisher Subscriber example

* Create a package

  ```bash
    ros2 pkg create --build-type ament_python py_pubsub
  ```

* Write a publisher node

  * Go to pub-sub directory

    ```bash
      cd py_pubsub/py_pubsub/
    ```

  * Download an example talker
  
    ```bash
      wget https://raw.githubusercontent.com/ros2/examples/foxy/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py
    ```

