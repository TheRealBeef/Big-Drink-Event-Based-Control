# Big Drink Project

## ROS Melodic

Create a docker image, its name will be `osrf/ros:melodic-rpe`. You can have any other name, just be sure to change it in `run` and `attach` scripts.

```bash
  docker build -t osrf/ros:melodic-rpe .
  . run .
```

It is a good practice to run a `roscore` command on this terminal, open a new one, attach it to the container and do not touch the one running a roscore. Although it is not necessery. `open.launch` file is used in a project, if there is no roscore running it will run it automatically.

```bash
  roscore
```

To work on a different terminaluse `attach` script.

```bash
  . attach
```

## Running a restaurant

To start a restaurant must be open. Just run an `open` script.

```bash
  . open
```

After tou are done close a restaurant with a `close` script.

```bash
  . close
```

## Designing a node

All nodes should be run from a `open.launch` file.

## Customer

A customer is a user and can order a drink executing an `order` script. They can check this order status by subscribing an `order_status` topic

```bash
rosropic echo order_status
```

## Drink Mixer

### Description

Drink mixer is a ros node that uses following topics:

- Subscribes:
  - /order - String,
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

It takes any order from `/order` topic and puts it into a list which size is defined in an `open.launch` file (1 in this commit). If possible it serves the order and updates its state in `/drink_mixer` topic. Four states are defined. In a meantime it keeps a customer updated and publishes string messages in `/order_status` topic.

## Stationary Robotic Arm

### Dependencies from a Drink Mixer

- Check valid `/glass_state` messages. If invalid message was sent, drink mixer will raise `ValueError` exception.
- Make sure that a topic `/glass_state` is always updated.
- Drink Ready is a message from a `/drink_mixer_topic` and not from a `/glass_state`.

### Simulated topics

Before a node of this component is created every importnat from a point of view of drink mixer features provided by an arm are simulated with scripts:

- `pubEGR` - publishes "Empty Glass Ready" message, mxier waits for it while received an order.
- `pubNG` - publishes "No Glass" message, when a drink is ready a robotic arm must take it, so there is no glass until it puts another one.
