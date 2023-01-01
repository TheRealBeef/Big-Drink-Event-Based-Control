# ROS 2 Humble + Gazebo

After following intructions you will have ROS2 up and running and Gazebo environement ready to go.

## Set up ROS2 with Gazebo

Only one step here. The command put below will build ROS2 image with a Dockerfile, which will take care of setting it up. It can take a while since it will execute ```apt update``` command and download Gazebo.

```bash
  docker build -t osrf/ros:humble-gazebo .
```

## Run your docker container

After using a `run` script your ros2 is ready to use.

```bash
  . run .
```

In my opinion a good practice is to run a roscore command on this terminal, open a new one, attach it to the container and do not touch the one running a roscore.

```bash
  roscore
```

Open a new terminal.

```bash
  . attach
```

To start a restaurant must be open.

```bash
  . open
```

## Designing a node

All nodes should be run from a `open.launch` file.

## Customer

A customer is a user and can order a drink executing an `order` script.

## Drink Mixer

### Description

Drink mixer is a ros node that uses following topics:

- Subscribes:
  - /order - String,
    - TO DO
  - /glass_state - String:
    - Empty Glass Ready,
    - No Glass
  - /close - Bool
- Publishes to:
  - /drink_mixer_state - String:
    - Idle,
    - Drink Pouring,
    - Drink Ready,
    - No Glass,
  - /order_status - String,

It takes any order from `/order` topic and puts it into a FIFO `queue` which maximum size is defined in a `open.launch` file. While it is possible it serves the order and updates its state in `/drink_mixer` topic. Four states are defined. In a meantime it keeps a customer updated and publishes string messages in `/order_status` topic.

## Stationary Robotic Arm

### Dependencies from a Drink Mixer

- Check valid `/glass_state` messages. If invalid message was sent, drink mixer will raise `ValueError` exception.
- Make sure that a topic `/glass_state` is always updated.
- Drink Ready is a message from a `/drink_mixer_topic` and not from a `/glass_state`.
