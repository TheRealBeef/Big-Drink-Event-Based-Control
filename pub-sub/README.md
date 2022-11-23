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

* (?) Create a ROS Workspace

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

  * make sure you are in `~/ws` directory, source the overlay

  ```bash
    . install/local_setup.bash
  ```

* test if you can run turtlesim

  * source the overlay
  
  ``` bash
    source /opt/ros/humble/setup.bash
  ```

  * run the `turtlesim` package

  ```bash
    ros2 run turtlesim turtlesim_node
  ```

  * If you run docker from run.sh script it should work, however some problems with Qt or X server may occur...

* Attatch VS Code to a docker container (Optional)

  * Download a Docker extention

  * Go to Docker -> Containers -> right click on osrf/ros... -> Attatch Visual Studio Code

  * Wait until it sets up

## 2. Publisher Subscriber example ( [link to the tutorial](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html) )

### 2.1 Setting up

* Make sure you're in a `~/ws/src/` directory

  ```bash
    cd ~/ws/src/
  ```

* Create a package

  ```bash
    ros2 pkg create --build-type ament_python py_pubsub
  ```

* Write a publisher node

  * Go to pub-sub directory

    ```bash
      cd py_pubsub/py_pubsub/
    ```

  * Download an example talker (`apt update && apt upgrade -y` may be required)
  
    ```bash
      apt install wget
      wget https://raw.githubusercontent.com/ros2/examples/foxy/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py
    ```

  * Add dependencies

    * (Optional but a good practice) Go to one level back directory with `cd ..` and open `package.xml` file in any text editor (e.g. VS Code), solve all TODOs

    * Add additional lines in `package.xml`

      ```bash
        <exec_depend>rclpy</exec_depend>
        <exec_depend>std_msgs</exec_depend>
      ```

    * (Optional but a good practice) Open the `setup.py` file, match the `maintainer`, `maintainer_email`, `description` and `license` fields to your package.xml:
      
      ```bash
        maintainer='YourName',
        maintainer_email='you@email.com',
        description='Examples of minimal publisher/subscriber using rclpy',
        license='Apache License 2.0',
      ```
    
* Write a subscriber node

  * Go to ~/ws/src/py_pubsub/py_pubsub directory and create the next node:
    
    ```bash
      wget https://raw.githubusercontent.com/ros2/examples/foxy/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py
    ```

    * Add the following line within the console_scripts brackets of the entry_points field:
      ```python
        enry_points={
          'console_scripts': [
            'talker = py_pubsub.publisher_member_function:main',
            'listener = py_pubsub.subscriber_member_function:main',
          ],
        },

### 2.2 Running publisher-subscriber

* Go to `~/ws/` directory
  
  ```bash
    cd ~/ws/
  ```

* (Optional) Check for missing dependencies
  
  ```bash
    rosdep install -i --from-path src --rosdistro humble -y
  ```

* Build your new package:

  ```bash
    colcon build --packages-select py_pubsub
  ```

* Open a new terminal, navigate to ros2_ws, source the setup files and run the talker node:

  ```bash
    . install/setup.bash
    ros2 run py_pubsub talker
  ```

* Open another terminal, navigate to ros2_ws, source the setup files and run the listener node:

  ```bash
    . install/setup.bash
    ros2 run py_pubsub listener
  ```
