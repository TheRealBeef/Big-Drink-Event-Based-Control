# Big-Drink-Event-Based-Control
Uses ROS to manage a User Interface, Drink Mixer, Robotic Arm, and Mobile Robot

## Set up ROS2
### 0. Prerequisites
* Python3,
* VS Code (Optional but recommended)
### 1. Set up ROS2 wrorkspace

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




## Software
- ROS/OROCOS?
- Framework
  - Drink Mixer
  - Stationary Robotic Arm
  - Mobile robot
  - User Interface
  - Environment
  - Customer
- Items simulated
  - Drink in glass
  - State of glass
## Drink Mixer
- States
   - Idle
   - Empty glass ready
   - Drink order received
   - Drink pouring
   - Drink full
   - Drink Ready
   - No Glass
- Assumptions
   - Drinks come from infinite containers
   - Drink mixes are predefined
   - Abstract the motor output away (make it black box for now)
   - All glasses are same size / same volume
- Control System
   - communicate with stationary arm once glass is filled
   - Prevent further action until glass is once again in position
Physical System
   - pumps to mix drinks
   - sensor to know when drink full
   - sensor to know that glass is loaded in position
## Stationary Robotic Arm
- States
   - Idle
   - Drink ready
   - Mobile robot ready
   - Pick up drink
   - Transferring drink
   - Drink set down
   - Transitioning to idle state
- Assumptions
   - The location of drink and mobile robot are known
   - The robot arm never drops the drink
   - The size of glass is known or we have sensors to adjust clamping tension
   - When receive input from drink mixer, and mobile robot is ready, move drink from mixer to mobile robot
   - Arm path prevents drink from spilling / mobile robot location is known
   - Once glass is loaded onto robot, send signal to MR that glass has been transferred and arm has moved out of the way
- Constraints/checks
   - Robot arm can reach both mixer and mobile robot
- Control system
   - communicate with drink mixer and mobile robot
- Physical system
   - sensor to know when mobile robot is at base station
   - signal to know when drink is mixed and ready
## Mobile robot
- States
   - Idle
   - At home, orientation correct
   - Drink placed on robot
   - Traveling base station to destination
   - At destination
   - Drink removed
   - Traveling destination to base station
   - Empty glass placed on robot
- Assumptions
   - Mobile robot has clear path from one station to another
   - Position of home and position of destination are known
   - Mobile robot has infinite battery and/or charges sufficiently on base station
   - There is only one mobile robot
   - Wait at home station with same position/orientation
- Constraints/checks
- Control System
   - Check to ensure glass has been transferred
   - Receive signal from Arm that glass has been transferred
   - When drink is loaded and static arm is moved away, move from home to destination
   - Sense when drink has been removed
   - Wait in some location (home? destination?) until command from UI to return drink has been given
   - Inform Arm that empty drink has been transferred back to home and is ready for return
- Physical System
   - Sensor to know when robot is at base station
   - sensor to know when robot is at customer station
   - sensor to know when drink is loaded/unloaded
## User interface
- States
   - Idle
   - Order placed
   - Glass is not at mixer (lockout)
   - Glass has been returned (allow new order)
- Assumptions
   - Buttons provide true/false output to “command”
   - Once command send, latch the output and wait until confirmation that it’s completed to allow next action
   - Do not allow incorrect actions (e.g. return drink when drink not taken, or not placed on robot)
   - glass is presenRt on the machine
- Constraints/checks
   - System doesn’t allow double-orders
   - Only one drink is allowed at a time (simplifies return)
- Control system
   - communicate with mixer and mobile robot
- Physical system
   - button 1 - order drink A
   - button 2 - order drink B
   - button 3 - return drink
